# http://localhost:5001
# run using python app.py and then go to ^^
# to do list @ bottom, we can add more tabs to app if we have time!

from flask import Flask, render_template_string, request, jsonify

# Optional heavy ML / data libraries — import defensively so the UI/dev
# server can start even if these aren't available in the environment.
torch = None
AutoModelForCausalLM = None
AutoTokenizer = None
np = None
pd = None
WomensHealthRAG = None
SymptomNutritionEngine = None
ProviderSearcher = None
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import numpy as np
    import pandas as pd
    from chat.rag import WomensHealthRAG
    from back.nutrition_engine import SymptomNutritionEngine
    from chat.find_a_provider import ProviderSearcher
except Exception:
    # Missing optional packages — continue with heuristics/fallbacks
    pass

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pomegranate - Women's Health App</title>
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

        /* Nutrition Engine Styles */
        .symptom-logger {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe5ee 100%);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border: 2px solid #ffd6e8;
        }

        .symptom-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin: 20px 0;
        }

        .symptom-btn {
            padding: 15px;
            border: 2px solid #ffd6e8;
            background: white;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #666;
            font-weight: 500;
            text-align: center;
            font-size: 14px;
        }

        .symptom-btn:hover {
            background: #ffe5f0;
            border-color: #ff9dbf;
            transform: translateY(-2px);
        }

        .symptom-btn.selected {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            border-color: #ff9dbf;
        }

        .cycle-phase-selector {
            margin: 20px 0;
        }

        .cycle-phase-selector label {
            display: block;
            color: #666;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .cycle-phase-select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ffd6e8;
            border-radius: 8px;
            font-size: 16px;
            color: #666;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s ease;
        }

        .cycle-phase-select:focus {
            outline: none;
            border-color: #ff9dbf;
        }

        .recommendation-btn {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 15px;
        }

        .recommendation-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(255, 157, 191, 0.4);
        }

        .quick-snacks-btn {
            background: #ffcc99;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-left: 10px;
        }

        .quick-snacks-btn:hover {
            background: #ffb380;
            transform: translateY(-2px);
        }

        .recommendations-container {
            margin-top: 40px;
            display: none;
            animation: fadeIn 0.5s ease;
        }

        .recommendations-container.active {
            display: block;
        }

        .encouragement-message {
            background: linear-gradient(135deg, #fff5e6 0%, #ffe8cc 100%);
            padding: 25px;
            border-radius: 12px;
            border-left: 5px solid #ffcc99;
            margin-bottom: 30px;
            color: #666;
            font-size: 16px;
            line-height: 1.8;
            font-style: italic;
        }

        .nutrients-section, .foods-section, .recipes-section {
            margin-bottom: 30px;
        }

        .nutrients-section h3, .foods-section h3, .recipes-section h3 {
            color: #ff9dbf;
            font-size: 20px;
            margin-bottom: 15px;
            border-bottom: 2px solid #ffd6e8;
            padding-bottom: 10px;
        }

        .nutrient-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }

        .nutrient-tag {
            background: #ffe5f0;
            color: #ff6ba6;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            border: 1px solid #ffd6e8;
        }

        .nutrient-tag.highlight {
            background: #ffb3d9;
            color: white;
            border-color: #ffb3d9;
        }

        .foods-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
            margin-bottom: 15px;
        }

        .food-item {
            background: white;
            border: 2px solid #ffd6e8;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            color: #666;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            cursor: help;
        }

        .food-item:hover {
            background: #ffe5f0;
            border-color: #ff9dbf;
            transform: translateY(-2px);
        }

        .food-tooltip {
            visibility: hidden;
            width: 200px;
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 10px 12px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s ease;
            font-size: 12px;
            line-height: 1.4;
            font-weight: normal;
            white-space: normal;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .food-tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }

        .food-item:hover .food-tooltip {
            visibility: visible;
            opacity: 1;
        }

        .recipe-card {
            background: white;
            border: 2px solid #ffd6e8;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }

        .recipe-card:hover {
            box-shadow: 0 8px 25px rgba(255, 157, 191, 0.2);
            border-color: #ff9dbf;
        }

        .recipe-card h4 {
            color: #ff9dbf;
            margin-bottom: 10px;
            font-size: 18px;
        }

        .recipe-meta {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            font-size: 14px;
            color: #999;
        }

        .recipe-meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .recipe-ingredients {
            background: #fffaf0;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #ffcc99;
        }

        .recipe-ingredients h5 {
            color: #ff9dbf;
            margin-bottom: 8px;
            font-size: 14px;
        }

        .recipe-ingredients ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .recipe-ingredients li {
            color: #666;
            font-size: 14px;
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
        }

        .recipe-ingredients li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #ffcc99;
            font-weight: bold;
        }

        .ingredient-with-tooltip {
            position: relative;
            cursor: help;
            border-bottom: 1px dotted #ffcc99;
            transition: color 0.2s ease;
        }

        .ingredient-with-tooltip:hover {
            color: #ff9dbf;
        }

        .ingredient-tooltip {
            visibility: hidden;
            position: absolute;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            font-weight: normal;
            border-bottom: 1px dotted transparent;
        }

        .ingredient-tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }

        .ingredient-with-tooltip:hover .ingredient-tooltip {
            visibility: visible;
            opacity: 1;
        }

        }

        .recipe-instructions {
            color: #666;
            line-height: 1.6;
            font-size: 14px;
        }

        .cycle-insight-card {
            background: linear-gradient(135deg, #e8f0ff 0%, #d4e3ff 100%);
            border: 2px solid #b3d9ff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            border-left: 5px solid #669bff;
        }

        .cycle-insight-card h4 {
            color: #4a7ba7;
            margin-bottom: 10px;
            font-size: 16px;
        }

        .cycle-insight-card p {
            color: #556a82;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 5px;
        }

        .snacks-container {
            display: none;
            animation: fadeIn 0.5s ease;
        }

        .snacks-container.active {
            display: block;
            margin-top: 30px;
            padding: 25px;
            background: #fffaf0;
            border-radius: 10px;
            border: 2px dashed #ffcc99;
        }

        .snacks-container h3 {
            color: #ff9dbf;
            margin-bottom: 20px;
            font-size: 20px;
        }

        .snacks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }

        .snack-card {
            background: white;
            border: 2px solid #ffcc99;
            border-radius: 8px;
            padding: 15px;
            transition: all 0.3s ease;
        }

        .snack-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 20px rgba(255, 204, 153, 0.3);
        }

        .snack-card h5 {
            color: #ff9dbf;
            margin-bottom: 8px;
            font-size: 16px;
        }

        .snack-meta {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
        }

        .snack-nutrients {
            background: #fff5f0;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 13px;
            color: #ff6ba6;
            font-weight: 500;
        }

        .symptom-reasoning {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #ff9dbf;
        }

        .symptom-reasoning h5 {
            color: #ff9dbf;
            margin-bottom: 8px;
            font-size: 14px;
        }

        .symptom-reasoning p {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin: 0;
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
                    <h1>Pomegranate</h1>
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
                    <h2 class="hero-title">Welcome to Pomegranate </h2>
                    <p class="hero-subtitle">
                        96% of scientific knowledge, drug testing, and treatment guidelines are based on male biology.
                    </p>
                    <p class="hero-subtitle">
                        This app takes a holistic approach - helping women meet their health goals and live healthy lives.
                     </p>
                </div>
                <div class="features-overview">
                    <div class="overview-card">
                        <h3 class="overview-title">Menstrual & Reproductive Health</h3>
                        <p class="overview-text">
                            Log period cycle, symptoms, moods, and notes to track patterns over time. Get insights into predicted periods, fertile windows, and ovulation days.
                        </p>
                    </div>
                    <div class="overview-card">
                        <h3 class="overview-title">Exercise & Nutrition</h3>
                        <p class="overview-text">
                            Track fitness and nutrition to maintain a healthy lifestyle. Get personalized food recommendations and be alerted when unhealthy patterns are present. 
                        </p>
                    </div>
                    <div class="overview-card">
                        <h3 class="overview-title">Chat with Pommie</h3>
                        <p class="overview-text">
                            Get information and advice surrounding women's health, or be redirected to helpful resources.
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
                    <button class="tab-btn" onclick="showTab('fitness', 'nutrition')">Nutrition</button>
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

                <div id="fitness-nutrition" class="tab-content">
                    <h3 style="color: #ff9dbf; margin-bottom: 20px;">Symptom-Aware Nutrition</h3>
                    <p style="color: #666; margin-bottom: 15px;">
                        Honor what your body is telling you. Log your symptoms and receive evidence-informed, personalized food recommendations tailored to your menstrual cycle or menopausal phase.
                    </p>

                    <div class="symptom-logger">
                        <h3 style="color: #ff9dbf; margin-bottom: 15px;">What are you experiencing?</h3>
                        <p style="color: #666; margin-bottom: 20px; font-size: 14px;">Select one or more symptoms to get personalized recommendations:</p>
                        
                        <div class="symptom-grid" id="symptomGrid">
                            <!-- Symptoms will be loaded here via JavaScript -->
                        </div>

                        <div class="cycle-phase-selector">
                            <label for="cyclePhaseSelect">Which cycle phase are you in? (optional)</label>
                            <select id="cyclePhaseSelect" class="cycle-phase-select">
                                <option value="">Not tracking cycle phase</option>
                                <option value="menstruation">Menstruation (Days 1-5)</option>
                                <option value="follicular">Follicular (Days 1-13)</option>
                                <option value="ovulation">Ovulation (Days 14-16)</option>
                                <option value="luteal">Luteal (Days 17-28)</option>
                            </select>
                        </div>

                        <div class="cycle-phase-selector">
                            <label for="lifePhaseSelect">Are you navigating perimenopause, menopause, or post-menopause? (optional)</label>
                            <select id="lifePhaseSelect" class="cycle-phase-select">
                                <option value="">Not applicable</option>
                                <option value="perimenopause">Perimenopause</option>
                                <option value="menopause">Menopause</option>
                                <option value="post-menopause">Post-Menopause</option>
                            </select>
                        </div>

                        <div style="display: flex; gap: 10px; margin-top: 15px;">
                            <button class="recommendation-btn" onclick="getRecommendations()">Get Recommendations</button>
                            <button class="quick-snacks-btn" onclick="toggleQuickSnacks()">Quick Snacks</button>
                        </div>
                    </div>

                    <!-- Recommendations Display -->
                    <div id="recommendationsContainer" class="recommendations-container">
                        <!-- Recommendations will be loaded here -->
                    </div>

                    <!-- Quick Snacks Display -->
                    <div id="snacksContainer" class="snacks-container">
                        <!-- Quick snacks will be loaded here -->
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

            <!-- resources (link + zip??) -->
            <section id="resources" class="section">
                <h2 class="section-title">Health Resources</h2>
                <p class="section-description">
                    Find trusted healthcare providers in your area and access national health resources.
                </p>
                
                <!-- Provider Search -->
                <div style="background: linear-gradient(135deg, #fff0f5 0%, #ffe5ee 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px;">
                    <h3 style="color: #ff9dbf; margin-bottom: 20px; font-size: 24px;">Find Local Providers</h3>
                    <p style="color: #666; margin-bottom: 20px;">Enter your ZIP code to find women's health providers, mental health services, hospitals, and clinics near you.</p>
                    
                    <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                        <input 
                            type="text" 
                            id="zipcodeInput" 
                            placeholder="Enter 5-digit ZIP code" 
                            maxlength="5"
                            style="flex: 1; padding: 12px 20px; border: 2px solid #ffd6e8; border-radius: 25px; font-size: 16px; outline: none;"
                        />
                        <button 
                            onclick="searchProviders()" 
                            style="padding: 12px 30px; background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%); color: white; border: none; border-radius: 25px; font-size: 16px; font-weight: 600; cursor: pointer;"
                        >
                            Search
                        </button>
                    </div>
                    
                    <div id="providerResults"></div>
                </div>
                
                <!-- National Resources -->
                <h3 style="color: #ff9dbf; margin-bottom: 20px; font-size: 24px;">National Resources</h3>
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
                        <h4>Planned Parenthood</h4>
                        <p>Reproductive health services, birth control, STI testing, and sexual wellness education.</p>
                        <p><strong>Phone:</strong> 1-800-230-7526</p>
                        <a href="https://www.plannedparenthood.org/health-center" target="_blank">Find a Health Center →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>National Suicide & Crisis Lifeline</h4>
                        <p>24/7 crisis support for mental health emergencies.</p>
                        <p><strong>Call/Text:</strong> 988</p>
                        <a href="https://988lifeline.org" target="_blank">Visit Website →</a>
                    </div>
                    
                    <div class="resource-item">
                        <h4>Postpartum Support International</h4>
                        <p>Support for pregnancy and postpartum mental health concerns.</p>
                        <p><strong>Phone:</strong> 1-800-944-4773</p>
                        <a href="https://www.postpartum.net" target="_blank">Visit Website →</a>
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
            // determine clicked button: prefer document.activeElement, otherwise fallback to matching onclick
            let clicked = document.activeElement;
            if (!clicked || !clicked.classList || !clicked.classList.contains('nav-btn')) {
                clicked = Array.from(buttons).find(b => {
                    const attr = b.getAttribute('onclick') || '';
                    return attr.includes(`showSection('${sectionName}')`) || attr.includes(`showSection("${sectionName}")`);
                }) || null;
            }
            if (clicked) clicked.classList.add('active');
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
            // set active on the clicked tab button
            let clicked = document.activeElement;
            if (!clicked || !clicked.classList || !clicked.classList.contains('tab-btn')) {
                clicked = Array.from(buttons).find(b => {
                    const attr = b.getAttribute('onclick') || '';
                    return attr.includes(`showTab('${sectionName}', '${tabName}')`) || attr.includes(`showTab("${sectionName}", "${tabName}")`);
                }) || null;
            }
            if (clicked) clicked.classList.add('active');
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

        // ============ NUTRITION ENGINE FUNCTIONS ============
        //add nutrition logic

        let selectedSymptoms = [];

        async function initializeNutritionSection(lifePhase = null) {
            try {
                let response;
                if (lifePhase) {
                    response = await fetch('/api/nutrition/symptoms', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ life_phase: lifePhase })
                    });
                } else {
                    response = await fetch('/api/nutrition/symptoms');
                }
                
                const data = await response.json();
                const symptoms = data.symptoms;
                const grid = document.getElementById('symptomGrid');
                grid.innerHTML = '';
                
                // Clear selected symptoms when changing life phase
                selectedSymptoms = [];

                symptoms.forEach(symptom => {
                    const btn = document.createElement('button');
                    btn.className = 'symptom-btn';
                    btn.textContent = symptom.charAt(0).toUpperCase() + symptom.slice(1).replace('_', ' ');
                    btn.onclick = () => toggleSymptom(symptom, btn);
                    grid.appendChild(btn);
                });
            } catch (error) {
                console.error('Error loading symptoms:', error);
            }
        }

        function toggleSymptom(symptom, button) {
            const index = selectedSymptoms.indexOf(symptom);
            if (index > -1) {
                selectedSymptoms.splice(index, 1);
                button.classList.remove('selected');
            } else {
                selectedSymptoms.push(symptom);
                button.classList.add('selected');
            }
        }

        async function getRecommendations() {
            if (selectedSymptoms.length === 0) {
                alert('Please select at least one symptom to get recommendations.');
                return;
            }

            const cyclePhase = document.getElementById('cyclePhaseSelect').value;
            const lifePhase = document.getElementById('lifePhaseSelect').value;
            
            try {
                const response = await fetch('/api/nutrition/recommendations', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        symptoms: selectedSymptoms,
                        cycle_phase: cyclePhase || null,
                        life_phase: lifePhase || null
                    })
                });

                const data = await response.json();
                if (data.status === 'success') {
                    displayRecommendations(data.data);
                } else {
                    alert('Error getting recommendations: ' + data.message);
                }
            } catch (error) {
                console.error('Error fetching recommendations:', error);
                alert('Failed to get recommendations. Please try again.');
            }
        }

        function displayRecommendations(recommendations) {
            const container = document.getElementById('recommendationsContainer');
            container.innerHTML = '';
            container.classList.add('active');

            // Encouragement message
            const encouragement = document.createElement('div');
            encouragement.className = 'encouragement-message';
            encouragement.textContent = recommendations.encouragement;
            container.appendChild(encouragement);

            // Phase insight (cycle or menopausal) if available
            if (recommendations.phase_insight) {
                const phaseCard = document.createElement('div');
                phaseCard.className = 'cycle-insight-card';
                phaseCard.innerHTML = `
                    <h4>${recommendations.phase_insight.phase.charAt(0).toUpperCase() + recommendations.phase_insight.phase.slice(1).replace('-', '-')} Phase</h4>
                    <p><strong>Focus:</strong> ${recommendations.phase_insight.focus}</p>
                    <p><strong>💡 Tip:</strong> ${recommendations.phase_insight.tip}</p>
                `;
                container.appendChild(phaseCard);
            }

            // Symptom reasoning
            if (recommendations.symptom_reasoning.length > 0) {
                const reasoningDiv = document.createElement('div');
                reasoningDiv.innerHTML = '<h3 style="color: #ff9dbf; margin-bottom: 15px; border-bottom: 2px solid #ffd6e8; padding-bottom: 10px;">Why Your Body Needs This</h3>';
                recommendations.symptom_reasoning.forEach(item => {
                    const card = document.createElement('div');
                    card.className = 'symptom-reasoning';
                    card.innerHTML = `
                        <h5>${item.symptom.charAt(0).toUpperCase() + item.symptom.slice(1)}</h5>
                        <p>${item.reason}</p>
                    `;
                    reasoningDiv.appendChild(card);
                });
                container.appendChild(reasoningDiv);
            }

            // Key nutrients
            if (recommendations.nutrients.length > 0) {
                const nutSection = document.createElement('div');
                nutSection.className = 'nutrients-section';
                nutSection.innerHTML = '<h3>Key Nutrients Your Body Is Asking For</h3>';
                const tagContainer = document.createElement('div');
                tagContainer.className = 'nutrient-tags';
                recommendations.nutrients.forEach((nutrient, index) => {
                    const tag = document.createElement('span');
                    tag.className = 'nutrient-tag ' + (index < 3 ? 'highlight' : '');
                    tag.textContent = nutrient;
                    tagContainer.appendChild(tag);
                });
                nutSection.appendChild(tagContainer);
                container.appendChild(nutSection);
            }

            // Recommended foods
            if (recommendations.recommended_foods.length > 0) {
                const foodSection = document.createElement('div');
                foodSection.className = 'foods-section';
                foodSection.innerHTML = '<h3>Nourishing Foods That Help</h3>';
                const foodGrid = document.createElement('div');
                foodGrid.className = 'foods-grid';
                recommendations.recommended_foods.forEach(food => {
                    const foodItem = document.createElement('div');
                    foodItem.className = 'food-item';
                    foodItem.innerHTML = `
                        ${food}
                        <div class="food-tooltip">${recommendations.food_benefits[food] || 'Nutritious choice for your body'}</div>
                    `;
                    foodGrid.appendChild(foodItem);
                });
                foodSection.appendChild(foodGrid);
                container.appendChild(foodSection);
            }

            // Recipes
            if (recommendations.recipes && recommendations.recipes.length > 0) {
                const recipeSection = document.createElement('div');
                recipeSection.className = 'recipes-section';
                recipeSection.innerHTML = '<h3>Easy Recipe & Snack Ideas</h3>';
                recommendations.recipes.forEach(recipe => {
                    const card = document.createElement('div');
                    card.className = 'recipe-card';
                    
                    // Build ingredients list with tooltips
                    let ingredientsList = '';
                    if (recipe.ingredients_with_benefits && recipe.ingredients_with_benefits.length > 0) {
                        ingredientsList = recipe.ingredients_with_benefits.map(ing => 
                            `<li><span class="ingredient-with-tooltip">${ing.name}<span class="ingredient-tooltip">${ing.benefit}</span></span></li>`
                        ).join('');
                    } else {
                        ingredientsList = recipe.ingredients.map(ing => 
                            `<li>${ing}</li>`
                        ).join('');
                    }
                    
                    card.innerHTML = `
                        <h4>${recipe.name}</h4>
                        <div class="recipe-meta">
                            <span class="recipe-meta-item">⏱️ ${recipe.time}</span>
                        </div>
                        <div class="recipe-ingredients">
                            <h5>Ingredients</h5>
                            <ul>
                                ${ingredientsList}
                            </ul>
                        </div>
                        <div class="recipe-instructions">
                            <strong>Instructions:</strong><br>${recipe.instructions}
                        </div>
                    `;
                    recipeSection.appendChild(card);
                });
                container.appendChild(recipeSection);
            }

            // Scroll to recommendations
            setTimeout(() => {
                container.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        }

        async function toggleQuickSnacks() {
            if (selectedSymptoms.length === 0) {
                alert('Please select at least one symptom to see quick snack ideas.');
                return;
            }

            const snacksContainer = document.getElementById('snacksContainer');
            
            if (snacksContainer.classList.contains('active')) {
                snacksContainer.classList.remove('active');
                snacksContainer.innerHTML = '';
                return;
            }

            try {
                console.log('Fetching snacks for symptoms:', selectedSymptoms);
                const response = await fetch('/api/nutrition/quick-snacks', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        symptoms: selectedSymptoms
                    })
                });

                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);
                
                if (data.status === 'success') {
                    displayQuickSnacks(data.data, snacksContainer);
                } else {
                    alert('Error getting snacks: ' + data.message);
                }
            } catch (error) {
                console.error('Error fetching snacks:', error);
                alert('Failed to get snack ideas. Please try again: ' + error.message);
            }
        }

        function displayQuickSnacks(snacks, container) {
            container.innerHTML = '<h3>⚡ 5-Minute Snack Ideas</h3>';
            container.classList.add('active');
            
            const grid = document.createElement('div');
            grid.className = 'snacks-grid';
            
            snacks.forEach(snack => {
                const card = document.createElement('div');
                card.className = 'snack-card';
                card.innerHTML = `
                    <h5>${snack.name}</h5>
                    <div class="snack-meta">
                        <span>⏱️ ${snack.time}</span>
                    </div>
                    <div class="snack-nutrients">${snack.nutrients}</div>
                `;
                grid.appendChild(card);
            });
            
            container.appendChild(grid);
            
            // Scroll to snacks container
            setTimeout(() => {
                container.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        }

        // Initialize nutrition section when page loads
        document.addEventListener('DOMContentLoaded', function() {
            initializeNutritionSection();
            
            // Listen for life phase changes to reload appropriate symptoms
            const lifePhaseSelect = document.getElementById('lifePhaseSelect');
            if (lifePhaseSelect) {
                lifePhaseSelect.addEventListener('change', function() {
                    const selectedLifePhase = this.value;
                    initializeNutritionSection(selectedLifePhase || null);
                    
                    // Clear previous recommendations and snacks
                    const recommendationsContainer = document.getElementById('recommendationsContainer');
                    const snacksContainer = document.getElementById('snacksContainer');
                    recommendationsContainer.classList.remove('active');
                    recommendationsContainer.innerHTML = '';
                    snacksContainer.classList.remove('active');
                    snacksContainer.innerHTML = '';
                    
                    // Hide/show cycle phase selector based on life phase
                    const cyclePhaseSelectElement = document.getElementById('cyclePhaseSelect');
                    const cyclePhaseDiv = cyclePhaseSelectElement.closest('.cycle-phase-selector');
                    if (selectedLifePhase) {
                        cyclePhaseDiv.style.display = 'none';
                        cyclePhaseSelectElement.value = '';
                    } else {
                        cyclePhaseDiv.style.display = 'block';
                    }
                });
            }
            
            // Listen for cycle phase changes to clear recommendations
            const cyclePhaseSelect = document.getElementById('cyclePhaseSelect');
            if (cyclePhaseSelect) {
                cyclePhaseSelect.addEventListener('change', function() {
                    // Clear previous recommendations and snacks
                    const recommendationsContainer = document.getElementById('recommendationsContainer');
                    const snacksContainer = document.getElementById('snacksContainer');
                    recommendationsContainer.classList.remove('active');
                    recommendationsContainer.innerHTML = '';
                    snacksContainer.classList.remove('active');
                    snacksContainer.innerHTML = '';
                });
            }
        });

        // Provider Search Function
        function searchProviders() {
            const zipcode = document.getElementById('zipcodeInput').value.trim();
            const resultsDiv = document.getElementById('providerResults');
            
            if (!zipcode || zipcode.length !== 5 || !/^\d{5}$/.test(zipcode)) {
                resultsDiv.innerHTML = '<p style="color: #c62828; padding: 15px; background: #ffebee; border-radius: 8px;">Please enter a valid 5-digit ZIP code.</p>';
                return;
            }
            
            resultsDiv.innerHTML = '<p style="color: #999; padding: 15px;">🔍 Searching for providers...</p>';
            
            fetch('/api/providers/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ zipcode: zipcode })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    resultsDiv.innerHTML = `<p style="color: #c62828; padding: 15px; background: #ffebee; border-radius: 8px;">${data.error}</p>`;
                    return;
                }
                
                let html = '<div style="margin-top: 20px;">';
                
                // Local Providers
                if (data.providers && data.providers.length > 0) {
                    html += '<h4 style="color: #ff9dbf; margin-bottom: 15px;">Local Healthcare Providers</h4>';
                    html += '<div style="display: grid; gap: 15px;">';
                    
                    data.providers.forEach(provider => {
                        const distanceText = provider.distance !== 'N/A' ? `${provider.distance} miles away` : '';
                        html += `
                            <div style="background: white; border: 2px solid #ffd6e8; border-radius: 8px; padding: 15px;">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                                    <h5 style="color: #ff9dbf; margin: 0; font-size: 16px;">${provider.name}</h5>
                                    ${distanceText ? `<span style="color: #999; font-size: 14px;">${distanceText}</span>` : ''}
                                </div>
                                <p style="color: #666; margin: 5px 0; font-size: 14px;"><strong>Type:</strong> ${provider.type}</p>
                                ${provider.address !== 'Address not available' ? `<p style="color: #666; margin: 5px 0; font-size: 14px;"><strong>Address:</strong> ${provider.address}</p>` : ''}
                                ${provider.phone !== 'N/A' ? `<p style="color: #666; margin: 5px 0; font-size: 14px;"><strong>Phone:</strong> ${provider.phone}</p>` : ''}
                                ${provider.website ? `<a href="${provider.website}" target="_blank" style="color: #ff9dbf; text-decoration: none; font-size: 14px;">Visit Website →</a>` : ''}
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                } else {
                    html += '<p style="color: #666; padding: 15px; background: #fff5f8; border-radius: 8px;">No providers found in your area. Try expanding your search or contact the national resources below.</p>';
                }
                
                // Mental Health Resources
                if (data.mental_health_resources && data.mental_health_resources.length > 0) {
                    html += '<h4 style="color: #ff9dbf; margin-top: 30px; margin-bottom: 15px;">National Mental Health Resources</h4>';
                    html += '<div style="display: grid; gap: 15px;">';
                    
                    data.mental_health_resources.forEach(resource => {
                        html += `
                            <div style="background: white; border: 2px solid #ffd6e8; border-radius: 8px; padding: 15px;">
                                <h5 style="color: #ff9dbf; margin: 0 0 8px 0; font-size: 16px;">${resource.name}</h5>
                                <p style="color: #666; margin: 5px 0; font-size: 14px;">${resource.description}</p>
                                ${resource.phone ? `<p style="color: #666; margin: 5px 0; font-size: 14px;"><strong>Phone:</strong> ${resource.phone}</p>` : ''}
                                ${resource.website ? `<a href="${resource.website}" target="_blank" style="color: #ff9dbf; text-decoration: none; font-size: 14px;">Visit Website →</a>` : ''}
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                }
                
                html += '</div>';
                resultsDiv.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
                resultsDiv.innerHTML = '<p style="color: #c62828; padding: 15px; background: #ffebee; border-radius: 8px;">An error occurred while searching. Please try again.</p>';
            });
        }

        // Allow Enter key to trigger search
        document.addEventListener('DOMContentLoaded', function() {
            const zipcodeInput = document.getElementById('zipcodeInput');
            if (zipcodeInput) {
                zipcodeInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        searchProviders();
                    }
                });
            }
        });
    </script>
</body>
</html>
"""

# Initialize optional components defensively
print("=" * 60)

# Nutrition engine (optional)
engine = None
if SymptomNutritionEngine is not None:
    try:
        engine = SymptomNutritionEngine()
        print("Nutrition Engine ready!")
    except Exception as e:
        print("Warning: Nutrition engine failed to initialize:", e)

# Provider searcher (optional)
provider_searcher = None
if ProviderSearcher is not None:
    try:
        provider_searcher = ProviderSearcher()
    except Exception as e:
        print("Warning: Provider searcher failed to initialize:", e)

# RAG initialization (optional)
rag = None
if WomensHealthRAG is not None:
    try:
        print("Initializing rag...")
        from sentence_transformers import SentenceTransformer
        rag = WomensHealthRAG(
            knowledge_base_path="./chat/data.csv",
            generation_model_path="./chat/fine-tune-attempts/distilgpt2-finetuned"
        )
        print("RAG initialized successfully.")
    except Exception as e:
        print("Warning: RAG initialization failed — continuing without RAG.")
        print(e)

print("=" * 60)
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

@app.route('/api/nutrition/symptoms', methods=['GET', 'POST'])
def get_symptoms():
    """Get list of available symptoms to log based on life phase"""
    if engine is None:
        return {"status": "error", "message": "Nutrition engine unavailable"}, 503

    life_phase = None
    if request.method == 'POST' and request.json:
        life_phase = request.json.get('life_phase')

    symptoms = engine.get_symptoms(life_phase)
    return {
        "status": "success",
        "symptoms": symptoms,
        "life_phase": life_phase,
        "message": "Available symptoms for logging"
    }


@app.route('/api/nutrition/log', methods=['POST'])
def log_symptom():
    """Log a single symptom and get immediate recommendations"""
    if engine is None:
        return {"status": "error", "message": "Nutrition engine unavailable"}, 503

    data = request.json
    symptom = data.get('symptom')

    if not symptom:
        return {"status": "error", "message": "Symptom is required"}, 400

    recommendation = engine.log_symptom(symptom)

    if not recommendation:
        return {
            "status": "error",
            "message": f"Symptom '{symptom}' not found. Available symptoms: {engine.get_symptoms()}"
        }, 404

    return {
        "status": "success",
        "data": recommendation
    }


@app.route('/api/nutrition/recommendations', methods=['POST'])
def get_recommendations():
    """Get personalized nutrition recommendations based on symptoms and phase"""
    if engine is None:
        return {"status": "error", "message": "Nutrition engine unavailable"}, 503

    data = request.json
    symptoms_list = data.get('symptoms', [])
    cycle_phase = data.get('cycle_phase')
    life_phase = data.get('life_phase')

    if not symptoms_list:
        return {"status": "error", "message": "At least one symptom is required"}, 400

    recommendations = engine.get_recommendations(symptoms_list, cycle_phase, life_phase)

    # Add ingredient benefits to each recipe
    try:
        from back.nutrition_engine import INGREDIENT_BENEFITS
    except Exception:
        INGREDIENT_BENEFITS = {}

    for recipe in recommendations.get('recipes', []):
        recipe['ingredients_with_benefits'] = [
            {
                'name': ing,
                'benefit': INGREDIENT_BENEFITS.get(ing.lower(), 'Nutrient-rich ingredient supporting your wellness')
            }
            for ing in recipe.get('ingredients', [])
        ]

    return {
        "status": "success",
        "data": recommendations
    }


@app.route('/api/nutrition/quick-snacks', methods=['POST'])
def get_quick_snacks():
    """Get quick 5-minute snack ideas for logged symptoms"""
    if engine is None:
        return {"status": "error", "message": "Nutrition engine unavailable"}, 503

    data = request.json
    symptoms_list = data.get('symptoms', [])

    if not symptoms_list:
        return {"status": "error", "message": "At least one symptom is required"}, 400

    snacks = engine.get_quick_snacks(symptoms_list)

    return {
        "status": "success",
        "data": snacks,
        "message": f"Found {len(snacks)} quick snack ideas"
    }
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """API endpoint for health assistant chatbot"""
    data = request.json or {}
    user_msg = data.get('message', '')
    if not user_msg:
        return jsonify({'reply': 'Please send a message in the request body ("message").'}), 400

    if rag is None:
        return jsonify({"reply": "RAG unavailable — backend model stack not initialized in this environment."})

    try:
        reply = rag.generate_response_simple(user_msg, top_k=3, verbose=True, similarity_threshold=0.5)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Assistant error: {e}"}), 500

# what to work on:
# implement backend for each endpoint:
# 1. period tracker
# 2. journal
# 3. diet tracker
# 4. exercise tracker
# 5. chatbot

# decide which features are premium
# add on more depending on time

@app.route('/api/providers/search', methods=['POST'])
def search_providers():
    """Search for healthcare providers by zipcode"""
    try:
        data = request.json
        zipcode = data.get('zipcode', '').strip()
        
        if not zipcode or len(zipcode) != 5 or not zipcode.isdigit():
            return jsonify({
                'success': False,
                'error': 'Please enter a valid 5-digit ZIP code'
            }), 400

        if provider_searcher is None:
            return jsonify({'success': False, 'error': 'Provider search unavailable'}), 503

        print(f"🔍 Searching providers for ZIP: {zipcode}")

        # Get coordinates from zipcode
        coords = provider_searcher.get_coordinates_from_zipcode(zipcode)

        if not coords:
            return jsonify({
                'success': False,
                'error': 'Could not find location for this ZIP code'
            }), 404

        lat, lon = coords
        print(f"📍 Coordinates: {lat}, {lon}")

        # Search for providers
        providers = provider_searcher.search_providers_overpass(lat, lon, radius_km=25)

        # Add Planned Parenthood info
        providers = provider_searcher.add_planned_parenthood_locations(providers)

        # Get mental health resources
        mental_health = provider_searcher.get_mental_health_resources()

        print(f"✅ Found {len(providers)} providers")

        return jsonify({
            'success': True,
            'zipcode': zipcode,
            'location': f"{lat}, {lon}",
            'providers': providers[:20],  # Limit to 20 results
            'mental_health_resources': mental_health
        })
        
    except Exception as e:
        print(f"❌ Error searching providers: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'An error occurred while searching for providers'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)