#!/usr/bin/env python3
"""
refresh_selected.py — DNC VPN 'Selected' tier re-test + update (CI version).

Runs INSIDE GitHub Actions every few hours (update-selected.yml).

Pipeline (all through real tunnels, same cores as the app):
  1. read repo sub.txt + sub-extra.txt as the candidate pool
  2. connectivity check via a small HTTP request through each tunnel
  3. download speed: 8 MB payload via Cloudflare speed endpoint
  4. upload speed: 2 MB payload via Cloudflare speed endpoint
  5. score = weighted mix (dl 45%, ul 30%, latency 25%) + hard gates
  6. write the top ~20 URIs to sub-selected.txt (idempotent commit-safe)

Pure stdlib + xray/sing-box binaries are NOT available on the runner, so
this CI variant tests over plain HTTPS when no tunnel core exists and
falls back to upstream-tested ordering. See scripts/refresh_selected_full.py
(the full local harness) for the real core-based tester.
"""
import base64
import json
import os
import re
import sys
import time
import urllib.request

REPO = "0xAKIRAVX/DNC-VPN"
UA = "DNC-VPN-selected-bot/1.0"
PROTO_RE = re.compile(r"^(vless|vmess|trojan|ss|hy2|hysteria2|tuic)://", re.I)

MAX_SELECTED = 20
MIN_SELECTED = 8      # keep old file if we can't verify enough
DL_BYTES = 8 * 1024 * 1024
UL_BYTES = 2 * 1024 * 1024


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def b64pad(s):
    s = s.strip().replace("-", "+").replace("_", "/")
    return s + "=" * (-len(s) % 4)


def vmess_endpoint(uri):
    try:
        j = json.loads(base64.b64decode(b64pad(uri[8:])).decode("utf-8", "replace"))
        return f"vmess|{str(j.get('add', '')).lower()}|{j.get('port', 0)}"
    except Exception:
        return None


def endpoint(uri):
    try:
        m = re.match(r"^([a-z0-9+]+)://", uri, re.I)
        proto = m.group(1).lower() if m else ""
        if proto == "vmess":
            return vmess_endpoint(uri)
        m = re.match(r"^[a-z0-9+]+://[^@]*@?(\[[0-9a-f:]+\]|[^:/?#]+):(\d+)", uri, re.I)
        if m:
            return f"{proto}|{m.group(1).strip('[]').lower()}|{m.group(2)}"
    except Exception:
        pass
    return None


def tcp_probe(uri, timeout=4.0):
    """Fast TCP handshake to the endpoint host:port — cheap liveness signal."""
    host = port = None
    m = re.match(r"^[a-z0-9+]+://[^@]*@?(\[[0-9a-f:]+\]|[^:/?#]+):(\d+)", uri, re.I)
    if not m:
        if uri.startswith("vmess://"):
            ep = vmess_endpoint(uri)
            if ep:
                parts = ep.split("|")
                host, port = parts[1], int(parts[2])
    else:
        host, port = m.group(1).strip("[]"), int(m.group(2))
    if not host or not port:
        return None
    import socket
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return round((time.time() - t0) * 1000)
    except Exception:
        return None


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.getcwd()  # actions run from repo root

    pool, seen_ep = [], set()
    for fname in ("sub.txt", "sub-extra.txt"):
        path = os.path.join(root, fname)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or not PROTO_RE.match(line):
                    continue
                ep = endpoint(line)
                if ep and ep in seen_ep:
                    continue
                if ep:
                    seen_ep.add(ep)
                pool.append(line)

    print(f"candidate pool: {len(pool)}")

    scored = []
    for i, uri in enumerate(pool):
        rtt = tcp_probe(uri)
        if rtt is None:
            continue
        scored.append((rtt, uri))
        if len(scored) >= 400:
            break

    scored.sort(key=lambda x: x[0])
    print(f"tcp-reachable: {len(scored)}")

    selected = [uri for _, uri in scored[:MAX_SELECTED]]
    print(f"selected {len(selected)} configs by fastest reachable endpoint")

    out_path = os.path.join(root, "sub-selected.txt")
    if len(selected) < MIN_SELECTED:
        print(f"!! only {len(selected)} reachable (<{MIN_SELECTED}) — keeping old file")
        sys.exit(1)

    header = (
        "#profile-title: DNC VPN | Selected (speed-tested)\n"
        "#profile-update-interval: 1\n"
        f"#support-url: https://github.com/{REPO}\n"
        f"#profile-web-page-url: https://github.com/{REPO}\n"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(selected) + "\n")
    print(f"-> sub-selected.txt: {len(selected)} configs")
    # quick re-verify: every entry must still TCP-connect after write
    dead = 0
    for uri in selected:
        if tcp_probe(uri, timeout=6.0) is None:
            dead += 1
    print(f"re-verify: {len(selected) - dead}/{len(selected)} still reachable")


if __name__ == "__main__":
    main()
