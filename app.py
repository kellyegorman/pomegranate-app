# http://localhost:5001
# run using python app.py and then go to ^^
# to do list @ bottom, we can add more tabs to app if we have time!

from flask import Flask, render_template_string

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>(Name of our app) Women's Health Focused</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #ffd6e8 0%, #ffc0d3 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            box-shadow: 0 2px 20px rgba(255, 182, 193, 0.3);
            margin-bottom: 30px;
            border-radius: 15px;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 30px;
        }

        h1 {
            color: #ff9dbf;
            font-size: 28px;
            font-weight: 700;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        nav {
            display: flex;
            gap: 15px;
        }

        .nav-btn {
            padding: 10px 20px;
            border: none;
            background: transparent;
            color: #666;
            font-size: 16px;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .nav-btn:hover {
            background: #ffe5f0;
            color: #ff9dbf;
        }

        .nav-btn.active {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
        }

        .main-content {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(255, 182, 193, 0.2);
            min-height: 500px;
        }

        .section {
            display: none;
        }

        .section.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .section-title {
            color: #ff9dbf;
            font-size: 32px;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .section-description {
            color: #666;
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 30px;
        }

        .hero {
            text-align: center;
            padding: 40px 20px;
        }

        .hero-title {
            color: #ff9dbf;
            font-size: 48px;
            margin-bottom: 20px;
            font-weight: 700;
        }

        .hero-subtitle {
            color: #666;
            font-size: 20px;
            margin-bottom: 40px;
            line-height: 1.6;
        }

        .features-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }

        .overview-card {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe5ee 100%);
            padding: 30px;
            border-radius: 12px;
            border: 2px solid #ffd6e8;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .overview-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(255, 182, 193, 0.3);
        }

        .overview-title {
            font-size: 24px;
            font-weight: 600;
            color: #ff9dbf;
            margin-bottom: 15px;
        }

        .overview-text {
            color: #666;
            font-size: 16px;
            line-height: 1.6;
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 2px solid #ffe5f0;
            padding-bottom: 10px;
        }

        .tab-btn {
            padding: 10px 20px;
            border: none;
            background: transparent;
            color: #666;
            font-size: 16px;
            cursor: pointer;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .tab-btn:hover {
            background: #ffe5f0;
            color: #ff9dbf;
        }

        .tab-btn.active {
            background: #ffb3d9;
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        .placeholder {
            background: #fff5f8;
            border: 2px dashed #ffd6e8;
            border-radius: 12px;
            padding: 60px 40px;
            text-align: center;
            margin-top: 30px;
        }

        .placeholder-text {
            color: #ff9dbf;
            font-size: 18px;
            font-weight: 500;
        }

        .chatbot-container {
            background: #fff5f8;
            border-radius: 12px;
            padding: 20px;
            height: 500px;
            display: flex;
            flex-direction: column;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
            background: white;
            border-radius: 8px;
        }

        .chat-input-container {
            display: flex;
            gap: 10px;
        }

        .chat-input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #ffd6e8;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }

        .chat-input:focus {
            border-color: #ff9dbf;
        }

        .chat-send-btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .chat-send-btn:hover {
            transform: scale(1.05);
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
            }

            nav {
                width: 100%;
                justify-content: center;
                flex-wrap: wrap;
            }

            .nav-btn {
                flex: 1;
                min-width: 120px;
                padding: 10px 15px;
                font-size: 14px;
            }

            .main-content {
                padding: 25px;
            }

            .section-title, .hero-title {
                font-size: 28px;
            }

            .tabs {
                flex-wrap: wrap;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-content">
                <div class="logo">
                    <h1>name of our app</h1>
                </div>
                <nav>
                    <button class="nav-btn active" onclick="showSection('home')">Home</button>
                    <button class="nav-btn" onclick="showSection('menstrual')">Cycle Tracker</button>
                    <button class="nav-btn" onclick="showSection('fitness')">Diet & Exercise</button>
                    <button class="nav-btn" onclick="showSection('chatbot')">Chat</button>
                </nav>
            </div>
        </header>

        <main class="main-content">
            <!-- HOME SECTION -->
            <section id="home" class="section active">
                <div class="hero">
                    <h2 class="hero-title">Welcome to app </h2>
                    <p class="hero-subtitle">
                        Describe the app idk something something women's health
                    </p>
                </div>

                <div class="features-overview">
                    <div class="overview-card">
                        <h3 class="overview-title">menstrual & repro health tracker</h3>
                        <p class="overview-text">
                            Log cycle, track symptoms, keep health journal 
                            Period tracking, reproductive health, menopause symptoms?
                        </p>
                    </div>
                    <div class="overview-card">
                        <h3 class="overview-title">diet & exercise</h3>
                        <p class="overview-text">
                            set goals for health - diet, workout, fitness, nutrition ...
                            Create personalized plans based on demographics (age, height, weight) and goals
                            ex: weight loss, build muscle, focus on specific areas of body 
                        </p>
                    </div>
                    <div class="overview-card">
                        <h3 class="overview-title">chat</h3>
                        <p class="overview-text">
                            get health advice, find local providers?
                        </p>
                    </div>
                </div>
            </section>

            <!-- MENSTRUAL SECTION -->
            <section id="menstrual" class="section">
                <h2 class="section-title">Menstrual Cycle Tracker</h2>
                <p class="section-description">
                    Track your menstrual cycle and maintain a personal journal to better understand your body's patterns.
                </p>
                
                <div class="tabs">
                    <button class="tab-btn active" onclick="showTab('menstrual', 'tracker')">Tracker</button>
                    <button class="tab-btn" onclick="showTab('menstrual', 'journal')">Journal</button>
                </div>

                <div id="menstrual-tracker" class="tab-content active">
                    <h3 style="color: #ff9dbf; margin-bottom: 20px;">Cycle Calendar</h3>
                    <p style="color: #666; margin-bottom: 20px;">Log your periods and track cycle patterns over time.</p>
                    <div class="placeholder">
                        <p class="placeholder-text">Cycle tracker calendar coming soon</p>
                    </div>
                </div>

                <div id="menstrual-journal" class="tab-content">
                    <h3 style="color: #ff9dbf; margin-bottom: 20px;">Personal Journal</h3>
                    <p style="color: #666; margin-bottom: 20px;">Record symptoms, moods, and notes about your cycle.</p>
                    <div class="placeholder">
                        <p class="placeholder-text">Journal interface coming soon</p>
                    </div>
                </div>
            </section>

            <!-- FITNESS SECTION -->
            <section id="fitness" class="section">
                <h2 class="section-title">Diet & Exercise</h2>
                <p class="section-description">
                    Monitor your nutrition and fitness to maintain a healthy, balanced lifestyle.
                </p>
                
                <div class="tabs">
                    <button class="tab-btn active" onclick="showTab('fitness', 'diet')">Diet</button>
                    <button class="tab-btn" onclick="showTab('fitness', 'exercise')">Exercise</button>
                </div>

                <div id="fitness-diet" class="tab-content active">
                    <h3 style="color: #ff9dbf; margin-bottom: 20px;">Nutrition Tracker</h3>
                    <p style="color: #666; margin-bottom: 20px;">Log your meals and track your nutritional intake.</p>
                    <div class="placeholder">
                        <p class="placeholder-text">Diet tracker interface coming soon</p>
                    </div>
                </div>

                <div id="fitness-exercise" class="tab-content">
                    <h3 style="color: #ff9dbf; margin-bottom: 20px;">Workout Log</h3>
                    <p style="color: #666; margin-bottom: 20px;">Record your exercises and track your fitness progress.</p>
                    <div class="placeholder">
                        <p class="placeholder-text">Exercise tracker interface coming soon</p>
                    </div>
                </div>
            </section>

            <!-- CHATBOT SECTION -->
            <section id="chatbot" class="section">
                <h2 class="section-title">Health Assistant</h2>
                <p class="section-description">
                    Chat with our AI health assistant for personalized guidance and wellness support.
                </p>
                
                <div class="chatbot-container">
                    <div class="chat-messages" id="chatMessages">
                        <p style="color: #999; text-align: center; padding: 40px 20px;">
                            Start a conversation with your health assistant
                        </p>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" class="chat-input" placeholder="Type your message here..." id="chatInput">
                        <button class="chat-send-btn" onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script>
        function showSection(sectionName) {
            const sections = document.querySelectorAll('.section');
            const buttons = document.querySelectorAll('.nav-btn');
            
            sections.forEach(section => {
                section.classList.remove('active');
            });
            
            buttons.forEach(button => {
                button.classList.remove('active');
            });
            
            document.getElementById(sectionName).classList.add('active');
            event.target.classList.add('active');
        }

        function showTab(sectionName, tabName) {
            const tabs = document.querySelectorAll(`#${sectionName} .tab-content`);
            const buttons = document.querySelectorAll(`#${sectionName} .tab-btn`);
            
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });
            
            buttons.forEach(button => {
                button.classList.remove('active');
            });
            
            document.getElementById(`${sectionName}-${tabName}`).classList.add('active');
            event.target.classList.add('active');
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const messagesContainer = document.getElementById('chatMessages');
            const message = input.value.trim();
            
            if (message) {
                if (messagesContainer.querySelector('p[style*="color: #999"]')) {
                    messagesContainer.innerHTML = '';
                }
                
                const userMsg = document.createElement('div');
                userMsg.style.cssText = 'background: #ffb3d9; color: white; padding: 12px 20px; border-radius: 18px; margin-bottom: 10px; max-width: 70%; margin-left: auto; text-align: right;';
                userMsg.textContent = message;
                messagesContainer.appendChild(userMsg);
                
                setTimeout(() => {
                    const botMsg = document.createElement('div');
                    botMsg.style.cssText = 'background: #fff5f8; color: #666; padding: 12px 20px; border-radius: 18px; margin-bottom: 10px; max-width: 70%; border: 2px solid #ffd6e8;';
                    botMsg.textContent = 'Chatbot integration coming soon!';
                    messagesContainer.appendChild(botMsg);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }, 500);
                
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        }

        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page route"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/menstrual/tracker', methods=['GET', 'POST'])
def menstrual_tracker():
    """API endpoint for menstrual cycle tracking"""
    return {"status": "success", "message": "Menstrual tracker endpoint"}

@app.route('/api/menstrual/journal', methods=['GET', 'POST'])
def menstrual_journal():
    """API endpoint for menstrual journal entries"""
    return {"status": "success", "message": "Menstrual journal endpoint"}

@app.route('/api/fitness/diet', methods=['GET', 'POST'])
def diet_tracker():
    """API endpoint for diet tracking"""
    return {"status": "success", "message": "Diet tracker endpoint"}

@app.route('/api/fitness/exercise', methods=['GET', 'POST'])
def exercise_tracker():
    """API endpoint for exercise tracking"""
    return {"status": "success", "message": "Exercise tracker endpoint"}

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """API endpoint for health assistant chatbot"""
    return {"status": "success", "message": "Chatbot endpoint"}

# what to work on:
# implement backend for each endpoint:
# 1. period tracker
# 2. journal
# 3. diet tracker
# 4. exercise tracker
# 5. chatbot

# decide which features are premium
# add on more depending on time

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)