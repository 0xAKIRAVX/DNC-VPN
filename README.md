<div dir="rtl">

# 🛡️ DNC VPN

**کلاینت VPN سریع و رایگان مخصوص ایران** — بر پایه‌ی ArasClient (فورک NekoBox)

[![Download](https://img.shields.io/badge/%D8%AF%D8%A7%D9%86%D9%84%D9%88%D8%AF-APK_%D8%A2%D8%AE%D8%B1%DB%8C%D9%86_%D9%86%D8%B3%D8%AE%D9%87-brightgreen?style=for-the-badge)](../../releases/latest)
[![sub update](https://img.shields.io/badge/%D8%B3%D8%A7%D8%A8%E2%80%8C%D9%87%D8%A7-%D9%87%D8%B1_5_%D8%AF%D9%82%DB%8C%D9%82%D9%87-blue?style=for-the-badge)](#-کانفیگهای-رایگان)
[![platform](https://img.shields.io/badge/%D9%BE%D9%84%D8%AA%D9%81%D9%88%D8%B1%D9%85-Android_7%2B-lightgrey?style=for-the-badge)](#-دانلود-و-نصب)

کانال تلگرام: [@OxAKIRAVX](https://t.me/OxAKIRAVX)

---

## 📲 دانلود و نصب

- **APK (arm64-v8a):** از صفحه‌ی [Releases](../../releases/latest) دانلود کنید
- روی نسخه‌های قبلی DNC **بدون حذف برنامه** نصب می‌شود (امضای یکسان)
- اندروید ۷ به بالا
- اگر نصب جایگزین خطا داد، یک‌بار برنامه‌ی قبلی را حذف و دوباره نصب کنید

## 🚀 کانفیگ‌های رایگان (ساب‌های داخلی)

دو گروه اشتراک داخلی دارد که **خودکار هر ۵ دقیقه** از منابع تست‌شده‌ی مخصوص ایران
تجمیع و به‌روزرسانی می‌شوند (به‌روزرسانی داخل اپ: هر بار باز کردن برنامه + به‌روزرسانی خودکار گروه):

| گروه | محتوا | مناسب برای |
|---|---|---|
| **Free** 🥇 | SS44 GOLD — کانفیگ‌هایی که **تست ترافیک واقعی** را پاس کرده‌اند و اولویت‌بندی‌شده برای ایرانسل + کانفیگ‌های **Reality** پالایش‌شده برای مخابرات/همراه اول/ایرانسل | شروع سریع، کمترین -۱ |
| **Free Extra** | همه‌ی لیست Free + کانفیگ‌های تست‌شده‌ی Eternity (تنوع بیشتر) | وقتی لیست Free شلوغ بود |

**منابع تجمیع** (به ترتیب اولویت داخل لیست):

1. [SS44 GOLD](https://github.com/ZendanTeam/SS44-sub) — تست TCP + تست ترافیک واقعی، رتبه‌بندی Reality و پورت 443 اول، آپدیت هر ۳۰ دقیقه
2. [My-Clean-Configs](https://github.com/Mojtaba1423/My-Clean-Configs) — کانفیگ‌های Reality جراحی‌شده برای اپراتورهای ایران (تست TCP + TLS Handshake)
3. [V2RayAggregator Eternity](https://github.com/mahdibland/V2RayAggregator) — فقط در لیست Extra، تست‌شده بالادستی

### استفاده از ساب در کلاینت‌های دیگر (v2rayNG / Hiddify / NekoBox / Streisand)

```
https://raw.githubusercontent.com/0xAKIRAVX/DNC-VPN/main/sub.txt
https://raw.githubusercontent.com/0xAKIRAVX/DNC-VPN/main/sub-extra.txt
```

## 🔧 رفع مشکل پینگ «-1»

به ترتیب انجام دهید:

1. در گروه **Free** دکمه‌ی **Update** را بزنید (کانفیگ‌ها هر ۵ دقیقه عوض می‌شوند — لیست دیشب امروز مرده است)
2. `⋮ → Test all` بگیرید و بر اساس پینگ مرتب کنید — **کانفیگ‌های بالای لیست (Reality/443) بیشترین شانس را دارند**
3. **ایرانسل:** تنظیمات → **Fragment** را یک بار روشن و یک بار خاموش تست کنید
4. ساعت گوشی حتماً روی **Automatic** باشد (ساعت اشتباه = fail شدن همه‌ی TLS/Realityها)
5. بعد از نصب نسخه‌ی جدید، برای تازه‌سازی گروه **Free Extra** یک‌بار تنظیم
   «Show free subscription» را خاموش/روشن کنید
6. اگر همه‌ی TCPها قفل بودند، چند دقیقه بعد دوباره Update بزنید (لیست دائم تازه می‌شود)

## Modes

راهنمای سریع انتخاب حالت و کانفیگ:

- **VLESS + Reality (پورت 443):** اولین انتخاب روی همه‌ی اپراتورها؛ ترافیک شبیه TLS واقعی است و بیشترین شانس عبور از DPI را دارد.
- **VMess/ws + TLS روی CDN (پورت‌های 443/2053/2083/2087/2096):** وقتی IP سرورهای مستقیم بلاک‌اند؛ از CDN عبور می‌کند.
- **Trojan:** جایگزین سبک و پایدار؛ پورت 443 ترجیح دارد.
- **SS:** سبک و سریع، اما در بعضی ساعات شبکه شناسایی می‌شود.
- **Hysteria2/TUIC (UDP):** فقط وقتی UDP اپراتور باز باشد؛ در بیشتر شبکه‌های ایران UDP مهار شده است.
- **Fragment (تکه‌تکه کردن TLS):** مخصوص ایرانسل — در تنظیمات هست؛ خاموش/روشن بودنش را حتماً هر دو حالت تست کنید.
- **تست پینگ داخلی فقط TCP می‌سنجد:** کانفیگی که پینگ می‌دهد ولی وب باز نمی‌کند را با یک کانفیگ دیگر عوض کنید.

## 📄 حریم خصوصی

- DNC VPN هیچ داده‌ای به سرور ما نمی‌فرستد؛ لیست کانفیگ‌ها از GitHub خوانده می‌شود
- ترافیک شما از سرورهای رایگانِ عمومی عبور می‌کند — برای کارهای حساس (بانک، ایمیل اصلی) از سرور شخصی استفاده کنید
- متن کامل: [CR.md](CR.md)

## ❤️ اعتبارها

- [ArasClient](https://github.com/ArasTey/ArasClient) / [NekoBox for Android](https://github.com/MatsuriDayo/NekoBoxForAndroid) — پایه‌ی برنامه
- [ZendanTeam/SS44-sub](https://github.com/ZendanTeam/SS44-sub) — موتور تست و رتبه‌بندی ایرانسل
- [Mojtaba1423/My-Clean-Configs](https://github.com/Mojtaba1423/My-Clean-Configs) — Realityهای پالایش‌شده اپراتورها
- [mahdibland/V2RayAggregator](https://github.com/mahdibland/V2RayAggregator) — لیست Extra

</div>
