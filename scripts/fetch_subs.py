#!/usr/bin/env python3
"""
fetch_subs.py — DNC VPN subscription aggregator (Iran-focused).

Produces two subscription files in the repo root:
  sub.txt       — GOLD tier: traffic-tested, Irancell-first ranked configs
                  (SS44 GOLD + Mojtaba clean Reality)  -> app group "Free"
  sub-extra.txt — EXTRA tier: GOLD tier + mahdibland Eternity (capped)
                  -> app group "Free Extra"

Both files are refreshed by .github/workflows/update-sub.yml every 5 minutes.
Pure stdlib; safe to run anywhere.
"""
import base64
import json
import re
import sys
import urllib.request

REPO = "0xAKIRAVX/DNC-VPN"
UA = "DNC-VPN-sub-bot/1.0"

GOLD_SOURCES = [
    # (tag, url) — order = priority (first = highest; kept first in output)
    ("SS44", "https://raw.githubusercontent.com/ZendanTeam/SS44-sub/main/SS44-gold.txt"),
    ("MOJTABA", "https://raw.githubusercontent.com/Mojtaba1423/My-Clean-Configs/main/m_configs.txt"),
]
EXTRA_SOURCES = GOLD_SOURCES + [
    # bigger pool for the Extra group (tested upstream every 12h), capped below
    ("ETERNITY", "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity.txt"),
]
ETERNITY_CAP = 300          # max configs taken from Eternity
MIN_CONFIGS = 20            # never write a file below this (guard vs upstream outage)

PROTO_RE = re.compile(r'^(vless|vmess|trojan|ss|hy2|hysteria2|tuic)://', re.I)


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def b64pad(s):
    s = s.strip().replace("-", "+").replace("_", "/")
    return s + "=" * (-len(s) % 4)


def vmess_endpoint(uri):
    """host:port from a vmess:// base64 URI (None if undecodable)."""
    try:
        j = json.loads(base64.b64decode(b64pad(uri[8:])).decode("utf-8", "replace"))
        return f"vmess|{str(j.get('add', '')).lower()}|{j.get('port', 0)}"
    except Exception:
        return None


def endpoint(uri):
    """Stable endpoint key for dedupe (proto|host|port)."""
    try:
        m = re.match(r'^([a-z0-9+]+)://', uri, re.I)
        proto = m.group(1).lower() if m else ""
        if proto == "vmess":
            return vmess_endpoint(uri)
        m = re.match(r'^[a-z0-9+]+://[^@]*@?(\[[0-9a-f:]+\]|[^:/?#]+):(\d+)', uri, re.I)
        if m:
            return f"{proto}|{m.group(1).strip('[]').lower()}|{m.group(2)}"
    except Exception:
        pass
    return None


def collect(sources):
    """-> (list_of_uris, stats). Deduped by exact URI and endpoint; priority order kept."""
    out, seen_uri, seen_ep, stats = [], set(), set(), []
    for tag, url in sources:
        got = 0
        try:
            body = fetch(url)
        except Exception as e:
            print(f"  [{tag}] FETCH FAILED: {e}", file=sys.stderr)
            stats.append((tag, 0, "fetch-error"))
            continue
        cap = ETERNITY_CAP if tag == "ETERNITY" else 10 ** 9
        taken = 0
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not PROTO_RE.match(line):
                continue
            if taken >= cap:
                break
            if line in seen_uri:
                continue
            ep = endpoint(line)
            if ep and ep in seen_ep:
                continue
            seen_uri.add(line)
            if ep:
                seen_ep.add(ep)
            out.append(line)
            taken += 1
            got += 1
        stats.append((tag, got, "ok"))
        print(f"  [{tag}] +{got} configs")
    return out, stats


def header(title):
    return (
        f"#profile-title: {title}\n"
        "#profile-update-interval: 1\n"
        f"#support-url: https://github.com/{REPO}\n"
        f"#profile-web-page-url: https://github.com/{REPO}\n"
    )


def write(path, title, uris):
    if len(uris) < MIN_CONFIGS:
        print(f"  !! {path}: only {len(uris)} configs (<{MIN_CONFIGS}) — keeping old file", file=sys.stderr)
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(header(title) + "\n".join(uris) + "\n")
    print(f"  -> {path}: {len(uris)} configs")
    return True


def main():
    print("== GOLD tier (sub.txt — app group 'Free') ==")
    gold, _ = collect(GOLD_SOURCES)
    print("== EXTRA tier (sub-extra.txt — app group 'Free Extra') ==")
    extra, _ = collect(EXTRA_SOURCES)  # re-collect: keeps gold order first, then Eternity
    ok1 = write("sub.txt", "DNC VPN | Free (GOLD)", gold)
    ok2 = write("sub-extra.txt", "DNC VPN | Free Extra", extra)
    if not (ok1 and ok2):
        sys.exit(1)


if __name__ == "__main__":
    main()
