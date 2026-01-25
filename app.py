# app.py
# http://localhost:5001
# Run using: python app.py

from flask import Flask, render_template_string, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from flask import Flask, render_template_string, request, jsonify
from chat.rag import WomensHealthRAG

app = Flask(__name__)


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

                /* Resources section styling */
        .resource-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .resource-item {
            background: #fff5f8;
            border: 2px solid #ffd6e8;
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .resource-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(255, 182, 193, 0.3);
        }

        .resource-item h4 {
            color: #ff9dbf;
            margin-bottom: 10px;
            font-size: 18px;
        }

        .resource-item p {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 10px;
        }

        .resource-item a {
            color: #ff9dbf;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }

        .resource-item a:hover {
            color: #ff6b9d;
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
                    <button class="nav-btn" onclick="showSection('menstrual')">Reproductive & Mental Health</button>
                    <button class="nav-btn" onclick="showSection('fitness')">Diet & Exercise</button>
                    <button class="nav-btn" onclick="showSection('chatbot')">Chat</button>
                    <button class="nav-btn" onclick="showSection('resources')">Resources</button>

                </nav>
            </div>
        </header>

        <main class="main-content">
            <!-- home  -->
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

            <!-- Menstural & Mental -->
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

            <!-- Diet & Exercise -->
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

            <!-- Chat (Pommie!!) -->
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

            <!-- resources (link + zip??) -->
            <section id="resources" class="section">
                <h2 class="section-title">Helpful links</h2>
                <p class="section-description">
                    Trusted medical sources for women's health information.
                </p>
                
                <div class="resource-list">
                    <div class="resource-item">
                        <h4>Women's Health (womenshealth.gov)</h4>
                        <p>Official U.S. government resource providing reliable, accessible health information for women.</p>
                        <a href="https://www.womenshealth.gov/" target="_blank">Visit Website →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>ACOG - American College of Obstetricians and Gynecologists</h4>
                        <p>Expert resources on women's reproductive health, pregnancy, and gynecological care.</p>
                        <a href="https://www.acog.org/" target="_blank">Visit Website →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>Mayo Clinic Women's Health</h4>
                        <p>Evidence-based information on women's health conditions, treatments, and wellness.</p>
                        <a href="https://www.mayoclinic.org/diseases-conditions/" target="_blank">Visit Website →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>Cleveland Clinic Health Library</h4>
                        <p>Comprehensive health information reviewed by medical professionals.</p>
                        <a href="https://my.clevelandclinic.org/health" target="_blank">Visit Website →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>Planned Parenthood</h4>
                        <p>Information about reproductive health, birth control, and sexual wellness.</p>
                        <a href="https://www.plannedparenthood.org/learn" target="_blank">Visit Website →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>NIH - Office of Research on Women's Health</h4>
                        <p>Research and resources on women's health from the National Institutes of Health.</p>
                        <a href="https://orwh.od.nih.gov/" target="_blank">Visit Website →</a>
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

        // Global variable to track current message for feedback
        let currentMessageData = null;

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

                const loadingMsg = document.createElement('div');
                loadingMsg.id = 'loading-msg';
                loadingMsg.style.cssText = 'background: #fff5f8; color: #999; padding: 12px 20px; border-radius: 18px; margin-bottom: 10px; max-width: 70%; border: 2px solid #ffd6e8;';
                loadingMsg.textContent = 'Thinking...';
                messagesContainer.appendChild(loadingMsg);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                fetch('/api/chatbot', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: message })
                })
                .then(res => res.json())
                .then(data => {
                    const loading = document.getElementById('loading-msg');
                    if (loading) loading.remove();
                    
                    displayBotMessage(data, message, messagesContainer);
                })
                .catch(error => {
                    const loading = document.getElementById('loading-msg');
                    if (loading) loading.remove();
                    
                    console.error('Error:', error);
                    const errorMsg = document.createElement('div');
                    errorMsg.style.cssText = 'background: #ffebee; color: #c62828; padding: 12px 20px; border-radius: 18px; margin-bottom: 10px; max-width: 70%; border: 2px solid #ef9a9a;';
                    errorMsg.textContent = 'Sorry, there was an error processing your message.';
                    messagesContainer.appendChild(errorMsg);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                });

                input.value = '';
            }
        }

        function displayBotMessage(data, question, container) {
            const botMsgContainer = document.createElement('div');
            botMsgContainer.style.cssText = 'max-width: 70%; margin-bottom: 10px;';
            botMsgContainer.id = 'latest-bot-message';
            
            const botMsg = document.createElement('div');
            botMsg.style.cssText = 'background: #fff5f8; color: #666; padding: 12px 20px; border-radius: 18px; border: 2px solid #ffd6e8;';
            botMsg.textContent = data.reply;
            botMsgContainer.appendChild(botMsg);
            
            // Add feedback buttons if needed
            if (data.needs_feedback) {
                const feedbackContainer = document.createElement('div');
                feedbackContainer.style.cssText = 'display: flex; gap: 10px; margin-top: 8px; align-items: center;';
                feedbackContainer.id = 'feedback-buttons';
                
                const feedbackText = document.createElement('span');
                feedbackText.style.cssText = 'color: #999; font-size: 12px;';
                feedbackText.textContent = 'Was this helpful?';
                feedbackContainer.appendChild(feedbackText);
                
                const thumbsUpBtn = document.createElement('button');
                thumbsUpBtn.innerHTML = '👍';
                thumbsUpBtn.style.cssText = 'background: white; border: 2px solid #ffd6e8; border-radius: 50%; width: 36px; height: 36px; cursor: pointer; font-size: 16px; transition: all 0.3s ease;';
                thumbsUpBtn.onmouseover = () => thumbsUpBtn.style.background = '#e8f5e9';
                thumbsUpBtn.onmouseout = () => thumbsUpBtn.style.background = 'white';
                thumbsUpBtn.onclick = () => handleFeedback('up', question, data.reply, botMsgContainer);
                
                const thumbsDownBtn = document.createElement('button');
                thumbsDownBtn.innerHTML = '👎';
                thumbsDownBtn.style.cssText = 'background: white; border: 2px solid #ffd6e8; border-radius: 50%; width: 36px; height: 36px; cursor: pointer; font-size: 16px; transition: all 0.3s ease;';
                thumbsDownBtn.onmouseover = () => thumbsDownBtn.style.background = '#ffebee';
                thumbsDownBtn.onmouseout = () => thumbsDownBtn.style.background = 'white';
                thumbsDownBtn.onclick = () => handleFeedback('down', question, data.reply, botMsgContainer);
                
                feedbackContainer.appendChild(thumbsUpBtn);
                feedbackContainer.appendChild(thumbsDownBtn);
                botMsgContainer.appendChild(feedbackContainer);
            }
            
            container.appendChild(botMsgContainer);
            container.scrollTop = container.scrollHeight;
        }

        function handleFeedback(feedback, question, answer, messageContainer) {
            const feedbackButtons = document.getElementById('feedback-buttons');
            if (feedbackButtons) {
                feedbackButtons.innerHTML = '<span style="color: #999; font-size: 12px;">Processing...</span>';
            }
            
            fetch('/api/chatbot/feedback', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    feedback: feedback,
                    question: question,
                    answer: answer
                })
            })
            .then(res => res.json())
            .then(data => {
                if (feedback === 'up') {
                    // Show success message
                    if (feedbackButtons) {
                        feedbackButtons.innerHTML = `
                            <span style="color: #4caf50; font-size: 12px;">
                                ✓ ${data.message}
                            </span>
                        `;
                    }
                } else if (feedback === 'down' && data.new_reply) {
                    // Replace with new response
                    const oldMessage = document.getElementById('latest-bot-message');
                    if (oldMessage) oldMessage.remove();
                    
                    const container = messageContainer.parentElement;
                    displayBotMessage({
                        reply: data.new_reply,
                        needs_feedback: data.needs_feedback
                    }, question, container);
                }
            })
            .catch(error => {
                console.error('Feedback error:', error);
                if (feedbackButtons) {
                    feedbackButtons.innerHTML = '<span style="color: #c62828; font-size: 12px;">Error processing feedback</span>';
                }
            });
        }

        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


print("Initializing RAG")
rag = WomensHealthRAG(
    knowledge_base_path="./chat/data.csv",
    generation_model_path="./chat/fine-tune-attempts/distilgpt2-finetuned" 
)
print("=" * 60)

# routes
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/menstrual/tracker', methods=['GET', 'POST'])
def menstrual_tracker():
    return {"status": "success", "message": "Menstrual tracker endpoint"}

@app.route('/api/menstrual/journal', methods=['GET', 'POST'])
def menstrual_journal():
    return {"status": "success", "message": "Menstrual journal endpoint"}

@app.route('/api/fitness/diet', methods=['GET', 'POST'])
def diet_tracker():
    return {"status": "success", "message": "Diet tracker endpoint"}

@app.route('/api/fitness/exercise', methods=['GET', 'POST'])
def exercise_tracker():
    return {"status": "success", "message": "Exercise tracker endpoint"}

# chat route :)
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Main chatbot endpoint with feedback support"""
    try:
        data = request.json
        user_msg = data.get("message", "")
        print(f"\n{'='*60}")
        print(f"User: {user_msg}")
        
        if not user_msg:
            return jsonify({"reply": "Please enter a message."})
        
        # responses from csv data
        response_data = rag.generate_response_simple(
            user_msg,
            top_k=3,
            verbose=True,
            similarity_threshold=0.5
        )
        
        print(f"Assistant: {response_data['reply'][:100]}...")
        print(f"Type: {response_data['response_type']}, Needs feedback: {response_data['needs_feedback']}")
        print(f"{'='*60}\n")
        
        return jsonify({
            'reply': response_data['reply'],
            'needs_feedback': response_data['needs_feedback'],
            'similarity': response_data['similarity'],
            'response_type': response_data['response_type']
        })
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"reply": "Sorry, I encountered an error."}), 500

# feedback rt
@app.route('/api/chatbot/feedback', methods=['POST'])
def chatbot_feedback():
    """Handle thumbs up/down feedback"""
    try:
        data = request.json
        # is it a thumbs up or down <--
        feedback = data.get('feedback')  
        question = data.get('question')
        answer = data.get('answer')
        
        print(f"\n{'='*60}")
        print(f"Feedback: {feedback}")
        print(f"Q: {question}")
        print(f"A: {answer[:100]}...")
        
        if feedback == 'up':
            # add thumbs up to data
            success = rag.add_to_dataset(question, answer)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Thank you! This response has been saved to improve future answers.'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to save feedback.'
                }), 500
                
        elif feedback == 'down':
            # get a new response if the original wasn't good 
            print("Regenerating response...")
            response_data = rag.generate_response_simple(
                question,
                top_k=3,
                verbose=True,
                similarity_threshold=0.5,
                regenerate=True
            )
            
            print(f"Regenerated: {response_data['reply'][:100]}...")
            print(f"{'='*60}\n")
            
            return jsonify({
                'success': True,
                'new_reply': response_data['reply'],
                'needs_feedback': response_data['needs_feedback'],
                'message': 'Generated a new response. Does this help?'
            })
        
        return jsonify({'success': False, 'message': 'Invalid feedback type'}), 400
        
    except Exception as e:
        print(f"Error handling feedback: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'An error occurred processing your feedback.'
        }), 500

if __name__ == '__main__':
    print("\nStarting Flask server on http://localhost:5001")
    print("Chat interface ready!")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)
