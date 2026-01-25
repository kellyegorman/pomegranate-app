# app.py
# http://localhost:5001
# run using python app.py and then go to ^^
# to do list @ bottom, we can add more tabs to app if we have time!

from flask import Flask, render_template_string, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from chat.rag import WomensHealthRAG
from back.nutrition_engine import SymptomNutritionEngine
from back.nutrition_api import nutrition_bp
from chat.find_a_provider import ProviderSearcher
from flask import Flask, render_template, render_template_string, request, jsonify
import time

import json

app = Flask(__name__)

# Register blueprints
app.register_blueprint(nutrition_bp)


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

        <!-- Menstural Tracker Styling -->
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #ffd6e8 0%, #ffc0d3 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(255, 182, 193, 0.2);
            padding: 40px;
        }

        h1 {
            text-align: center;
            color: #ff9dbf;
            margin-bottom: 10px;
            font-size: 32px;
            font-weight: 700;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
            line-height: 1.8;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe5ee 100%);
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #ffd6e8;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 182, 193, 0.25);
        }

        .phase-card {
            position: relative;
            overflow: hidden;
        }

        .phase-card.menstrual {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            border-color: #ff9dbf;
        }

        .phase-card.menstrual .stat-label,
        .phase-card.menstrual .stat-value,
        .phase-card.menstrual .phase-day {
            color: white;
        }

        .phase-card.follicular {
            background: linear-gradient(135deg, #d4f1f4 0%, #a8e6cf 100%);
            border-color: #75d4b3;
        }

        .phase-card.follicular .stat-value {
            color: #2d8659;
        }

        .phase-card.ovulation {
            background: linear-gradient(135deg, #e3f2ff 0%, #cce5ff 100%);
            border-color: #99ccff;
        }

        .phase-card.ovulation .stat-value {
            color: #0066cc;
        }

        .phase-card.luteal {
            background: linear-gradient(135deg, #ffefd5 0%, #ffe4b5 100%);
            border-color: #ffd699;
        }

        .phase-card.luteal .stat-value {
            color: #cc8800;
        }

        .phase-day {
            font-size: 14px;
            margin-top: 5px;
            opacity: 0.9;
            font-weight: 500;
        }

        .stat-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #ff9dbf;
        }

        .calendar-header {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 25px;
            gap: 30px;
        }

        nav.-btn.calendar-nav {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            border: none;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            transition: all 0.3s ease;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .nav-btn.calendar-nav:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 15px rgba(255, 157, 191, 0.4);
        }

        .current-month {
            font-size: 24px;
            font-weight: 700;
            color: #ff9dbf;
            min-width: 250px;
            text-align: center;
            white-space: nowrap;
        }

        .calendar {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            max-width: 100px
            margin-bottom: 30px;
        }

        .day-header {
            text-align: center;
            font-weight: 600;
            color: #ff9dbf;
            padding: 8px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .day {
            aspect-ratio: 1;
            border: 2px solid #ffd6e8;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            background: white;
            font-weight: 500;
            font-size: 14px;
        }

        .day:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(255, 182, 193, 0.2);
            border-color: #ffb3d9;
        }

        .day.other-month {
            color: #d0d0d0;
            border-color: #f5f5f5;
        }

        .day.period {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            border-color: #ff9dbf;
            font-weight: 600;
        }

        .day.predicted {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe5ee 100%);
            border-color: #ffc0d3;
            color: #ff9dbf;
        }

        .day.ovulation {
            background: linear-gradient(135deg, #e3f2ff 0%, #cce5ff 100%);
            border-color: #99ccff;
            color: #0066cc;
        }

        .day.today {
            border: 3px solid #ff9dbf;
            font-weight: 700;
            box-shadow: 0 0 0 3px rgba(255, 157, 191, 0.1);
        }

        .legend {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-bottom: 25px;
            padding: 20px;
            background: #fff5f8;
            border-radius: 12px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }

        .legend-color {
            width: 28px;
            height: 28px;
            border-radius: 6px;
            border: 2px solid rgba(0,0,0,0.1);
        }

        .phase-legend {
            background: #fff5f8;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }

        .phase-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
        }

        .phase-info {
            background: white;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #ffd6e8;
        }

        .phase-badge {
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .phase-badge.menstrual {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
        }

        .phase-badge.follicular {
            background: linear-gradient(135deg, #d4f1f4 0%, #a8e6cf 100%);
            color: #2d8659;
        }

        .phase-badge.ovulation {
            background: linear-gradient(135deg, #e3f2ff 0%, #cce5ff 100%);
            color: #0066cc;
        }

        .phase-badge.luteal {
            background: linear-gradient(135deg, #ffefd5 0%, #ffe4b5 100%);
            color: #cc8800;
        }

        .phase-info p {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            margin: 0;
        }

        .controls {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }

        .btn {
            padding: 12px 28px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            font-weight: 600;
        }

        .btn-primary {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 157, 191, 0.3);
        }

        .btn-secondary {
            background: white;
            color: #ff9dbf;
            border: 2px solid #ffd6e8;
        }

        .btn-secondary:hover {
            background: #fff5f8;
            border-color: #ffb3d9;
        }

        .instructions {
            background: #fff5f8;
            padding: 25px;
            border-radius: 12px;
            margin-top: 25px;
            border-left: 4px solid #ff9dbf;
        }

        .instructions h3 {
            color: #ff9dbf;
            margin-bottom: 15px;
            font-size: 20px;
            font-weight: 600;
        }

        .instructions ul {
            margin-left: 20px;
            color: #666;
            line-height: 1.8;
        }

        .instructions li {
            margin-bottom: 8px;
        }

        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 192, 211, 0.3);
            backdrop-filter: blur(5px);
            animation: fadeIn 0.3s;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background-color: white;
            margin: 3% auto;
            border-radius: 15px;
            width: 90%;
            max-width: 650px;
            box-shadow: 0 20px 60px rgba(255, 157, 191, 0.3);
            animation: slideDown 0.3s;
            max-height: 90vh;
            overflow-y: auto;
        }

        @keyframes slideDown {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .modal-header {
            padding: 25px 35px;
            border-bottom: 2px solid #ffe5f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #fff0f5 0%, #ffe5ee 100%);
            border-radius: 15px 15px 0 0;
        }

        .modal-header h2 {
            color: #ff9dbf;
            margin: 0;
            font-size: 24px;
            font-weight: 700;
        }

        .close {
            color: #ff9dbf;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            line-height: 1;
        }

        .close:hover {
            color: #ff6b9d;
            transform: rotate(90deg);
        }

        .modal-body {
            padding: 35px;
        }

        .modal-footer {
            padding: 20px 35px;
            border-top: 2px solid #ffe5f0;
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            background: #fff5f8;
            border-radius: 0 0 15px 15px;
        }

        .form-group {
            margin-bottom: 28px;
        }

        .form-group label {
            display: block;
            margin-bottom: 12px;
            color: #ff9dbf;
            font-weight: 600;
            font-size: 16px;
        }

        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            padding: 10px 12px;
            border-radius: 8px;
            transition: background 0.2s;
            color: #666;
            font-weight: 500;
        }

        .checkbox-label:hover {
            background: #fff5f8;
        }

        .checkbox-label input[type="checkbox"] {
            width: 22px;
            height: 22px;
            cursor: pointer;
            accent-color: #ff9dbf;
        }

        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 8px;
            background: #fff5f8;
            padding: 15px;
            border-radius: 8px;
        }

        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .option-btn {
            flex: 1;
            min-width: 90px;
            padding: 14px 18px;
            border: 2px solid #ffd6e8;
            background: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 15px;
            font-weight: 600;
            color: #666;
        }

        .option-btn:hover {
            border-color: #ffb3d9;
            background: #fff5f8;
            color: #ff9dbf;
        }

        .option-btn.selected {
            background: linear-gradient(135deg, #ffb3d9 0%, #ff9dbf 100%);
            color: white;
            border-color: #ff9dbf;
            box-shadow: 0 4px 12px rgba(255, 157, 191, 0.3);
        }

        textarea {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #ffd6e8;
            border-radius: 12px;
            font-family: inherit;
            font-size: 15px;
            resize: vertical;
            transition: all 0.3s ease;
            color: #333;
        }

        textarea:focus {
            outline: none;
            border-color: #ff9dbf;
            box-shadow: 0 0 0 3px rgba(255, 157, 191, 0.1);
        }

        /* Day indicator dots for symptoms */
        .day {
            position: relative;
        }

        .day-indicator {
            position: absolute;
            bottom: 4px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 3px;
        }

        .indicator-dot {
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: rgba(255, 157, 191, 0.5);
        }

        .day.period .indicator-dot {
            background: rgba(255, 255, 255, 0.8);
        }

        @media (max-width: 768px) {
            .container {
                padding: 25px;
            }
            
            h1 {
                font-size: 26px;
            }

            .stats {
                grid-template-columns: 1fr;
            }

            .calendar-header {
                gap: 15px;
            }

            .current-month {
                font-size: 20px;
                min-width: 180px;
            }
            
            .calendar {
                gap: 8px;
            }
            
            .day {
                font-size: 14px;
            }

            .day-header {
                font-size: 12px;
                padding: 8px;
            }

            .legend {
                gap: 15px;
            }

            .modal-content {
                width: 95%;
                margin: 5% auto;
            }

            .modal-body {
                padding: 25px;
            }

            .checkbox-group {
                grid-template-columns: 1fr;
            }

            .button-group {
                flex-direction: column;
            }

            .option-btn {
                width: 100%;
            }
        }
    </style>
    <!-- Tailwind CDN for utility classes -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html, body { overflow-x: hidden; }
        img, video, iframe { max-width: 100%; height: auto; }
        .main-content { overflow: hidden; }
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
                    <h2 class="hero-title">Welcome to Pomegranate 👩‍⚕️</h2>
                    <p class="hero-subtitle">
                        96% of scientific knowledge, drug testing, and treatment guidelines are based on male biology.
                    </p>
                    <p class="hero-subtitle">
                        This app takes a holistic approach to helping women meet their health goals and live healthy lives.
                     </p>
                </div>
                <div class="features-overview">
                    <div class="overview-card">
                        <h3 class="overview-title">Reproductive & Mental Health</h3>
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

            <!-- Menstural & Mental -->
            <section id="menstrual" class="section">
                <h2 class="section-title">🌸 Menstrual Cycle Tracker 🌸</h2>
                <p class="section-description">
                    Track your menstrual cycle and maintain a personal journal to better understand your body's patterns.
                </p>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Average Cycle Length</div>
                <div class="stat-value" id="avgCycleLength">--</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Next Period Expected</div>
                <div class="stat-value" id="nextPeriod">--</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Days Until Next Period</div>
                <div class="stat-value" id="daysUntil">--</div>
            </div>
            <div class="stat-card phase-card" id="phaseCard">
            <div class="stat-label">Current Cycle Phase</div>
            <div class="stat-value" id="currentPhase">--</div>
        <div class="phase-day" id="phaseDay"></div>
        </div>
        <div id="phaseInfoModal" class="modal">
            <div class="modal-body" id="phaseModalBody">
            </div>
        </div>
        </div>

        <div class="calendar-header">
                <button class="nav-btn" onclick="previousMonth()">‹</button>
                <div class="current-month" id="currentMonth"></div>
                <button class="nav-btn" onclick="nextMonth()">›</button>
        </div>

        <div class="calendar" id="calendar">
            <div class="day-header">Sun</div>
            <div class="day-header">Mon</div>
            <div class="day-header">Tue</div>
            <div class="day-header">Wed</div>
            <div class="day-header">Thu</div>
            <div class="day-header">Fri</div>
            <div class="day-header">Sat</div>
        </div>

        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #ff6b9d 0%, #c06c84 100%);"></div>
                <span>Period Days</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);"></div>
                <span>Predicted Period</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);"></div>
                <span>Predicted Ovulation</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="border: 3px solid #764ba2; background: white;"></div>
                <span>Today</span>
            </div>
        </div>

        <div class="phase-legend">
    <h3>Cycle Phases Explained</h3>
    <div class="phase-info-grid">
        <div class="phase-info">
            <div class="phase-badge menstrual">🩸 Menstrual</div>
            <p>Days 1-5: Period days. Hormone levels are low.</p>
        </div>
        <div class="phase-info">
            <div class="phase-badge follicular">🌱 Follicular</div>
            <p>Days 6-13: Energy increases as estrogen rises.</p>
        </div>
        <div class="phase-info">
            <div class="phase-badge ovulation">✨ Ovulation</div>
            <p>Days 14-16: Peak fertility. Estrogen peaks.</p>
        </div>
        <div class="phase-info">
            <div class="phase-badge luteal">🌙 Luteal</div>
            <p>Days 17-28: Progesterone rises, PMS may occur.</p>
        </div>
    </div>
</div>

        <div class="controls">
            <button class="btn btn-primary" onclick="clearData()">Clear All Data</button>
            <button class="btn btn-secondary" onclick="exportData()">Export Data</button>
        </div>

    <!-- Modal for day details -->
    <div id="dayModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalDate"></h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            
            <div class="modal-body">
                <div class="form-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="isPeriodDay" onchange="updatePeriodStatus()">
                        <span>This is a period day</span>
                    </label>
                </div>

                <div class="form-group" id="flowGroup" style="display: none;">
                    <label>Flow Intensity:</label>
                    <div class="button-group">
                        <button type="button" class="option-btn" data-value="spotting" onclick="selectFlow('spotting')">Spotting</button>
                        <button type="button" class="option-btn" data-value="light" onclick="selectFlow('light')">Light</button>
                        <button type="button" class="option-btn" data-value="medium" onclick="selectFlow('medium')">Medium</button>
                        <button type="button" class="option-btn" data-value="heavy" onclick="selectFlow('heavy')">Heavy</button>
                    </div>
                </div>

                <div class="form-group">
                    <label>Symptoms:</label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" value="cramps" class="symptom-check">
                            <span>Cramps</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="headache" class="symptom-check">
                            <span>Headache</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="bloating" class="symptom-check">
                            <span>Bloating</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="fatigue" class="symptom-check">
                            <span>Fatigue</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="back-pain" class="symptom-check">
                            <span>Back Pain</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="nausea" class="symptom-check">
                            <span>Nausea</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="breast-tenderness" class="symptom-check">
                            <span>Breast Tenderness</span>
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" value="acne" class="symptom-check">
                            <span>Acne</span>
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label>Mood:</label>
                    <div class="button-group">
                        <button type="button" class="option-btn" data-value="great" onclick="selectMood('great')">😊 Great</button>
                        <button type="button" class="option-btn" data-value="good" onclick="selectMood('good')">🙂 Good</button>
                        <button type="button" class="option-btn" data-value="okay" onclick="selectMood('okay')">😐 Okay</button>
                        <button type="button" class="option-btn" data-value="low" onclick="selectMood('low')">😔 Low</button>
                        <button type="button" class="option-btn" data-value="irritable" onclick="selectMood('irritable')">😠 Irritable</button>
                    </div>
                </div>

                <div class="form-group">
                    <label for="dayNotes">Notes:</label>
                    <textarea id="dayNotes" rows="4" placeholder="Add any notes about today..."></textarea>
                </div>
            </div>

            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button class="btn btn-primary" onclick="saveDayData()">Save</button>
            </div>
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

            <!-- Chat (Pommie!!) -->
            <section id="chatbot" class="section">
                <h2 class="section-title">Pommie</h2>
                <p class="section-description">
                    Ask questions related to women's health, get health advice, or redirect to Resources tab for more information.
                </p>
                
                <div class="chatbot-container">
                    <div class="chat-messages" id="chatMessages">
                        <p style="color: #999; text-align: center; padding: 40px 20px;">
                            Ask me a question about women's health! 😄😄
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

        async function showRecommendations() {
            saveBodyInfo();
            const recEl = document.getElementById('recommendations');
            recEl.innerHTML = 'Loading recommendations...';
            const body = JSON.parse(localStorage.getItem('bodyInfo') || '{}');
            const goalsLocal = goals.slice();
            const payload = {
                age: Number(body.age) || null,
                height_cm: Number(body.height_cm) || null,
                weight_kg: Number(body.weight_kg) || null,
                bodyType: body.bodyType || '',
                chars: body.chars || {},
                endGoal: localStorage.getItem('endGoal') || '',
                goals: goalsLocal || [],
                customExercises: JSON.parse(localStorage.getItem('customExercises')||'[]')
            };

            try {
                const resp = await fetch('/api/fitness/llm_recommend', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await resp.json();
                if (!data || data.status !== 'success') {
                    recEl.textContent = 'Recommendations unavailable.';
                    return;
                }
                let recs = data.recommendations || data.exercises || [];
                // merge in any user-added custom exercises that match endGoal or goals
                try {
                    const customs = JSON.parse(localStorage.getItem('customExercises')||'[]');
                    const eg = (localStorage.getItem('endGoal')||'').toLowerCase();
                    const goalTokens = (goalsLocal||[]).map(g=> (g.name||'').toLowerCase()).filter(Boolean);
                    const matches = [];
                    customs.forEach(c=>{
                        const name = (c.name||'').toLowerCase();
                        const targets = ((c.targets||'')+ '').toLowerCase();
                        let include = false;
                        if (eg && (name.includes(eg) || targets.includes(eg))) include = true;
                        if (!include && goalTokens.length) {
                            for (const t of goalTokens) {
                                if (name.includes(t) || targets.includes(t)) { include = true; break; }
                            }
                        }
                        if (include) matches.push({id: c.id || ('custom_'+Date.now()), name: c.name, description: c.description, rationale: 'User-added exercise', targets: (c.targets||'').split(',').map(s=>s.trim())});
                    });
                    // append matches (avoid duplicates by name)
                    const seen = new Set(recs.map(r=> (r.name||'').toLowerCase()));
                    matches.forEach(m=>{ if (!seen.has((m.name||'').toLowerCase())) { recs.push(m); seen.add((m.name||'').toLowerCase()); } });
                } catch(e) { console.error('merge custom exercises', e); }
                if (!recs.length) {
                    recEl.textContent = 'No recommendations found. Try changing goals or body info.';
                    return;
                }
                recEl.innerHTML = '<strong>Recommended exercises</strong><ul style="margin-top:8px; padding-left:18px; color:#444;">' +
                    recs.map(t => {
                        const pres = t.prescription || t.pres || null;
                        const presText = pres ? `<div style=\"color:#444; font-size:13px; margin-top:6px;\">${formatPrescription(pres)}</div>` : '';
                        return `<li style="margin-bottom:12px;"><strong>${t.name}</strong> — ${t.description || ''}<div style="color:#666; margin-top:6px; font-size:13px;">${t.rationale || ''}</div>${presText}</li>`;
                    }).join('') +
                    '</ul>';
            } catch (err) {
                console.error(err);
                recEl.textContent = 'Error loading recommendations.';
            }

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
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
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

                // Format a prescription object into readable text
        function formatPrescription(p){
            if(!p) return '';
            if(p.sets || p.reps){
                const sets = p.sets || '';
                const reps = p.reps || '';
                const freq = p.frequency_per_week ? (p.frequency_per_week + 'x/week') : '';
                return `${sets} sets x ${reps} reps ${freq ? ' · '+freq : ''}`.trim();
            }
            if(p.duration_min){
                const dur = p.duration_min + ' min';
                const freq = p.frequency_per_week ? (p.frequency_per_week + 'x/week') : '';
                return `${dur}${freq ? ' · '+freq : ''} · ${p.intensity || ''}`.trim();
            }
            return Object.keys(p).map(k=> `${k}: ${p[k]}`).join(', ');
        }

        // Exercise goals, logging, red-flag detection and breathing helpers
        const goals = [];
        const logs = [];

        function addGoal() {
            // Auto-save body info and ensure it exists before creating goals
            try { saveBodyInfo(); } catch(e){}
            const body = JSON.parse(localStorage.getItem('bodyInfo') || '{}');
            if (!body || !body.age) {
                alert('Please enter and save your body information first (age/height/weight).');
                return;
            }
            const name = document.getElementById('goalName').value.trim();
            const target = document.getElementById('goalTarget').value.trim();
            if (!name) return;
            const goal = { name, target };
            // prevent duplicate identical goals
            try {
                const saved = JSON.parse(localStorage.getItem('myGoals')||'[]');
                const exists = saved.some(g => (g.name||'').toLowerCase() === name.toLowerCase() && (g.target||'') === target);
                if (exists) {
                    alert('This goal already exists in My Goals.');
                    document.getElementById('goalName').value = '';
                    document.getElementById('goalTarget').value = '';
                    return;
                }
                saved.push(goal);
                localStorage.setItem('myGoals', JSON.stringify(saved));
            } catch(e){}
            goals.push(goal);
            document.getElementById('goalName').value = '';
            document.getElementById('goalTarget').value = '';
            renderGoals();

            // Ask backend to build a simple plan and tailored recommendations for this updated goals list
            (async ()=>{
                try {
                    const payload = {
                        age: Number(body.age)||null,
                        height_cm: Number(body.height_cm)||null,
                        weight_kg: Number(body.weight_kg)||null,
                        bodyType: body.bodyType||'',
                        chars: body.chars||{},
                        endGoal: localStorage.getItem('endGoal')||'',
                        goals: JSON.parse(localStorage.getItem('myGoals')||'[]')
                    };
                    const resp = await fetch('/api/fitness/llm_recommend',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
                    const data = await resp.json();
                    if (data && data.status === 'success') {
                        // show returned plan in recommendations area
                        const recEl = document.getElementById('recommendations');
                        let html = '';
                        if (data.plan && data.plan.length) {
                            html += '<strong>Personalized Plan</strong>';
                            html += '<ul style="margin-top:8px; padding-left:18px; color:#444;">' + data.plan.map(p=>{
                                const exHtml = (p.exercises||[]).map(e=>{
                                    if(!e) return '';
                                    if (typeof e === 'string') return e;
                                    const pres = e.prescription || e.pres || null;
                                    return pres ? `${e.name} — ${formatPrescription(pres)}` : e.name;
                                }).join('<br>');
                                return `<li style="margin-bottom:8px;"><strong>${p.goal}</strong> — ${p.schedule}<div style="color:#666; font-size:13px; margin-top:6px;">Exercises:<div style=\"margin-top:6px; color:#444;\">${exHtml}</div></div><div style="color:#666; font-size:13px; margin-top:6px;">${p.rationale||''}</div></li>`;
                            }).join('') + '</ul>';
                        }
                        if (data.recommendations && data.recommendations.length) {
                            html += '<hr style="margin:8px 0;">';
                            html += '<strong>Recommended exercises</strong><ul style="margin-top:8px; padding-left:18px; color:#444;">' +
                                data.recommendations.map(t=>`<li style="margin-bottom:12px;"><strong>${t.name}</strong> — ${t.description}<div style="color:#666; margin-top:6px; font-size:13px;">${t.rationale||''}</div></li>`).join('') + '</ul>';
                        }
                        recEl.innerHTML = html;
                        try { mergeRecommendedIntoCustom(data.recommendations || data.exercises || []); } catch(e){ console.error('merge recommended', e); }
                    }
                } catch(e) { console.error('Goal planning error', e); }
            })();
        }

        
        function logActivity() {
            const type = document.getElementById('activityType').value.trim();
            const minutes = document.getElementById('activityMinutes').value.trim();

            if (!type || !minutes) return;

            // collect built-in symptoms
            const symptoms = [];
            const built = [
                ['sym_chest','Chest pain','💓'],
                ['sym_breath','Shortness of breath','😮‍💨'],
                ['sym_nausea','Nausea','🤢'],
                ['sym_dizzy','Dizziness','💫'],
                ['sym_faint','Fainting / near-faint','⚠️'],
                ['sym_severe','Severe pain','🩸'],
                ['sym_joint','Joint pain','🦴'],
                ['sym_fatigue','Excessive fatigue','😴']
            ];
            built.forEach(s => { try{ if(document.getElementById(s[0]).checked) symptoms.push({key:s[1], icon:s[2]}); }catch(e){} });

            // collect custom symptoms (added by user)
            const customChecks = document.querySelectorAll('.custom-sym');
            customChecks.forEach(cb => {
                try {
                    if (cb.checked) {
                        const label = cb.dataset.label || cb.id || 'Other';
                        symptoms.push({ key: label, icon: '🔸' });
                    }
                } catch (e) {}
            });

            const entry = { type, minutes: Number(minutes), symptoms, ts: new Date().toLocaleString() };
            logs.unshift(entry);
            document.getElementById('activityType').value = '';
            document.getElementById('activityMinutes').value = '';
            // reset built-in symptom checkboxes
            built.forEach(s => { try{ document.getElementById(s[0]).checked = false; }catch(e){} });
            // reset custom symptom checkboxes
            customChecks.forEach(cb => { try{ cb.checked = false; }catch(e){} });
            renderLogs();

            // Send activity to backend for assessment (considers symptoms, activity, time)
            try {
                fetch('/api/fitness/assess_activity', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(entry)
                }).then(r => r.json()).then(resp => {
                    if (resp && resp.flag) {
                        showRedFlag(true, resp.reasons || []);
                    } else {
                        showRedFlag(false, []);
                    }
                }).catch(e => {
                    console.error('Flagging error', e);
                });
            } catch (e) { console.error(e); }
        }


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

        // Menstrual Tracker Functions
        let currentDate = new Date();
        let periodDays = new Set();
        let dayData = {};  // Store detailed info for each day: {date: {flow, symptoms, mood, notes}}
        
        // Load saved data
        function loadData() {
            const saved = localStorage.getItem('periodTracker');
            if (saved) {
                const data = JSON.parse(saved);
                periodDays = new Set(data.periodDays || []);
                dayData = data.dayData || {};
            }
        }

        // Save data
        function saveData() {
            const data = {
                periodDays: Array.from(periodDays),
                dayData: dayData
            };
            localStorage.setItem('periodTracker', JSON.stringify(data));
        }

        // Format date as YYYY-MM-DD
        function formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }

        // Get cycles from period days
        function getCycles() {
            if (periodDays.size === 0) return [];
            
            const sortedDays = Array.from(periodDays).sort();
            const cycles = [];
            let currentCycle = [sortedDays[0]];
            
            for (let i = 1; i < sortedDays.length; i++) {
                const prevDate = new Date(sortedDays[i - 1]);
                const currDate = new Date(sortedDays[i]);
                const daysDiff = (currDate - prevDate) / (1000 * 60 * 60 * 24);
                
                if (daysDiff <= 10) {
                    currentCycle.push(sortedDays[i]);
                } else {
                    if (currentCycle.length > 0) {
                        cycles.push(currentCycle);
                    }
                    currentCycle = [sortedDays[i]];
                }
            }
            
            if (currentCycle.length > 0) {
                cycles.push(currentCycle);
            }
            
            return cycles;
        }

        // Calculate average cycle length
        function getAverageCycleLength() {
            const cycles = getCycles();
            if (cycles.length < 2) return null;
            
            let totalLength = 0;
            for (let i = 1; i < cycles.length; i++) {
                const prevStart = new Date(cycles[i - 1][0]);
                const currStart = new Date(cycles[i][0]);
                const length = (currStart - prevStart) / (1000 * 60 * 60 * 24);
                totalLength += length;
            }
            
            return Math.round(totalLength / (cycles.length - 1));
        }

        // Get predicted period dates
        function getPredictedPeriods() {
            const cycles = getCycles();
            if (cycles.length === 0) return [];
            
            const avgLength = getAverageCycleLength();
            if (!avgLength) return [];
            
            const lastCycle = cycles[cycles.length - 1];
            const lastPeriodStart = new Date(lastCycle[0]);
            const predicted = [];
            
            // Predict next 3 cycles
            for (let i = 1; i <= 3; i++) {
                const nextStart = new Date(lastPeriodStart);
                nextStart.setDate(nextStart.getDate() + (avgLength * i));
                
                // Predict 5 days of period
                for (let j = 0; j < 5; j++) {
                    const day = new Date(nextStart);
                    day.setDate(day.getDate() + j);
                    predicted.push(formatDate(day));
                }
            }
            
            return predicted;
        }

        // Get predicted ovulation days
        function getPredictedOvulation() {
            const cycles = getCycles();
            if (cycles.length === 0) return [];
            
            const avgLength = getAverageCycleLength();
            if (!avgLength) return [];
            
            const lastCycle = cycles[cycles.length - 1];
            const lastPeriodStart = new Date(lastCycle[0]);
            const ovulationDays = [];
            
            // Predict ovulation for next 3 cycles (14 days before next period)
            for (let i = 1; i <= 3; i++) {
                const nextPeriod = new Date(lastPeriodStart);
                nextPeriod.setDate(nextPeriod.getDate() + (avgLength * i));
                
                const ovulation = new Date(nextPeriod);
                ovulation.setDate(ovulation.getDate() - 14);
                
                ovulationDays.push(formatDate(ovulation));
            }
            
            return ovulationDays;
        }

        function getCurrentPhase() {
            const cycles = getCycles();
            if (cycles.length === 0) return null;
            
            const avgLength = getAverageCycleLength();
            if (!avgLength) return null;
            
            const lastCycle = cycles[cycles.length - 1];
            const lastPeriodStart = new Date(lastCycle[0]);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            // Calculate days since last period started
            const daysSinceLastPeriod = Math.floor((today - lastPeriodStart) / (1000 * 60 * 60 * 24));
            
            // Calculate current cycle day (1-based)
            let cycleDay = (daysSinceLastPeriod % avgLength) + 1;
            if (daysSinceLastPeriod < 0) {
                return null;
            }
            
            if (cycleDay > avgLength) {
                cycleDay = avgLength;
            }
            
            // Determine phase based on cycle day
            let phase = '';
            let phaseEmoji = '';
            let phaseColor = '';
            
            if (cycleDay >= 1 && cycleDay <= 5) {
                phase = 'Menstrual';
                phaseEmoji = '🩸';
                phaseColor = 'menstrual';
            } else if (cycleDay >= 6 && cycleDay <= 13) {
                phase = 'Follicular';
                phaseEmoji = '🌱';
                phaseColor = 'follicular';
            } else if (cycleDay >= 14 && cycleDay <= 16) {
                phase = 'Ovulation';
                phaseEmoji = '✨';
                phaseColor = 'ovulation';
            } else {
                phase = 'Luteal';
                phaseEmoji = '🌙';
                phaseColor = 'luteal';
            }
            
            return {
                phase: phase,
                emoji: phaseEmoji,
                cycleDay: cycleDay,
                totalDays: avgLength,
                color: phaseColor
            };
        }

        // Update statistics
        function updateStats() {
            const avgLength = getAverageCycleLength();
            const avgLengthEl = document.getElementById('avgCycleLength');
            
            if (avgLength) {
                avgLengthEl.textContent = `${avgLength} days`;
                
                const cycles = getCycles();
                const lastCycle = cycles[cycles.length - 1];
                const lastPeriodStart = new Date(lastCycle[0]);
                const nextPeriod = new Date(lastPeriodStart);
                nextPeriod.setDate(nextPeriod.getDate() + avgLength);
                
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                const daysUntil = Math.round((nextPeriod - today) / (1000 * 60 * 60 * 24));
                
                document.getElementById('nextPeriod').textContent = 
                    nextPeriod.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                document.getElementById('daysUntil').textContent = 
                    daysUntil >= 0 ? daysUntil : 'Due';
            } else {
                avgLengthEl.textContent = '--';
                document.getElementById('nextPeriod').textContent = '--';
                document.getElementById('daysUntil').textContent = '--';
            }

            updatePhaseDisplay();
        }

        function updatePhaseDisplay() {
            const phaseData = getCurrentPhase();
            const phaseCard = document.getElementById('phaseCard');
            const phaseElement = document.getElementById('currentPhase');
            const phaseDayElement = document.getElementById('phaseDay');
            
            if (phaseData) {
                // Update text content
                phaseElement.textContent = `${phaseData.phase}`;
                phaseDayElement.textContent = `Day ${phaseData.cycleDay} of ${phaseData.totalDays}`;
                
                // Update card styling based on phase
                phaseCard.className = `stat-card phase-card ${phaseData.color}`;
            } else {
                // Not enough data to calculate phase
                phaseElement.textContent = '--';
                phaseDayElement.textContent = 'Track 2+ cycles to see';
                phaseCard.className = 'stat-card phase-card';
            }
        }

        // Render calendar
        function renderCalendar() {
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();
            
            // Update month display
            document.getElementById('currentMonth').textContent = 
                currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
            
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const prevLastDay = new Date(year, month, 0);
            
            const firstDayOfWeek = firstDay.getDay();
            const lastDateOfMonth = lastDay.getDate();
            const prevLastDate = prevLastDay.getDate();
            
            const predictedPeriods = new Set(getPredictedPeriods());
            const ovulationDays = new Set(getPredictedOvulation());
            const today = formatDate(new Date());
            
            let daysHTML = '';
            
            // Previous month days
            for (let i = firstDayOfWeek - 1; i >= 0; i--) {
                const day = prevLastDate - i;
                const date = new Date(year, month - 1, day);
                const dateStr = formatDate(date);
                daysHTML += `<div class="day other-month">${day}</div>`;
            }
            
            // Current month days
            for (let day = 1; day <= lastDateOfMonth; day++) {
                const date = new Date(year, month, day);
                const dateStr = formatDate(date);
                let classes = 'day';
                
                if (periodDays.has(dateStr)) {
                    classes += ' period';
                } else if (predictedPeriods.has(dateStr)) {
                    classes += ' predicted';
                } else if (ovulationDays.has(dateStr)) {
                    classes += ' ovulation';
                }
                
                if (dateStr === today) {
                    classes += ' today';
                }
                
                // Add indicators for tracked data
                let indicators = '';
                const data = dayData[dateStr];
                if (data) {
                    const hasData = [];
                    if (data.symptoms && data.symptoms.length > 0) hasData.push('symptoms');
                    if (data.mood) hasData.push('mood');
                    if (data.notes) hasData.push('notes');
                    
                    if (hasData.length > 0) {
                        indicators = '<div class="day-indicator">';
                        hasData.forEach(() => {
                            indicators += '<div class="indicator-dot"></div>';
                        });
                        indicators += '</div>';
                    }
                }
                
                daysHTML += `<div class="${classes}" onclick="togglePeriodDay('${dateStr}')">${day}${indicators}</div>`;
            }
            
            // Next month days
            const totalCells = daysHTML.split('<div').length - 1;
            const remainingCells = 42 - totalCells;
            for (let day = 1; day <= remainingCells; day++) {
                daysHTML += `<div class="day other-month">${day}</div>`;
            }
            
            document.getElementById('calendar').innerHTML = `
                <div class="day-header">Sun</div>
                <div class="day-header">Mon</div>
                <div class="day-header">Tue</div>
                <div class="day-header">Wed</div>
                <div class="day-header">Thu</div>
                <div class="day-header">Fri</div>
                <div class="day-header">Sat</div>
            ` + daysHTML;
            updateStats();
        }

        // Toggle period day
        let currentEditDate = null;
        
        function togglePeriodDay(dateStr) {
            currentEditDate = dateStr;
            openModal(dateStr);
        }

        function openModal(dateStr) {
            const date = new Date(dateStr);
            const formattedDate = date.toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
            
            document.getElementById('modalDate').textContent = formattedDate;
            
            // Load existing data
            const data = dayData[dateStr] || {};
            const isPeriod = periodDays.has(dateStr);
            
            // Set period checkbox
            document.getElementById('isPeriodDay').checked = isPeriod;
            updatePeriodStatus();
            
            // Set flow
            document.querySelectorAll('.option-btn[data-value]').forEach(btn => {
                btn.classList.remove('selected');
            });
            if (data.flow) {
                const flowBtn = document.querySelector(`.option-btn[data-value="${data.flow}"]`);
                if (flowBtn && flowBtn.parentElement.parentElement.id === 'flowGroup') {
                    flowBtn.classList.add('selected');
                }
            }
            
            // Set symptoms
            document.querySelectorAll('.symptom-check').forEach(checkbox => {
                checkbox.checked = data.symptoms && data.symptoms.includes(checkbox.value);
            });
            
            // Set mood
            if (data.mood) {
                const moodBtn = document.querySelector(`.option-btn[data-value="${data.mood}"]`);
                if (moodBtn && moodBtn.onclick.toString().includes('selectMood')) {
                    moodBtn.classList.add('selected');
                }
            }
            
            // Set notes
            document.getElementById('dayNotes').value = data.notes || '';
            
            // Show modal
            document.getElementById('dayModal').style.display = 'block';
        }

        function closeModal() {
            document.getElementById('dayModal').style.display = 'none';
            currentEditDate = null;
        }

        function updatePeriodStatus() {
            const isPeriod = document.getElementById('isPeriodDay').checked;
            document.getElementById('flowGroup').style.display = isPeriod ? 'block' : 'none';
        }

        function selectFlow(flow) {
            document.querySelectorAll('#flowGroup .option-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            event.target.classList.add('selected');
        }

        function selectMood(mood) {
            document.querySelectorAll('.button-group .option-btn').forEach(btn => {
                if (btn.onclick && btn.onclick.toString().includes('selectMood')) {
                    btn.classList.remove('selected');
                }
            });
            event.target.classList.add('selected');
        }

        function saveDayData() {
            if (!currentEditDate) return;
            
            const isPeriod = document.getElementById('isPeriodDay').checked;
            
            // Update period days set
            if (isPeriod) {
                periodDays.add(currentEditDate);
            } else {
                periodDays.delete(currentEditDate);
            }
            
            // Get flow
            let flow = null;
            const selectedFlowBtn = document.querySelector('#flowGroup .option-btn.selected');
            if (selectedFlowBtn) {
                flow = selectedFlowBtn.getAttribute('data-value');
            }
            
            // Get symptoms
            const symptoms = Array.from(document.querySelectorAll('.symptom-check:checked'))
                .map(cb => cb.value);
            
            // Get mood
            let mood = null;
            const moodBtns = document.querySelectorAll('.button-group .option-btn');
            moodBtns.forEach(btn => {
                if (btn.classList.contains('selected') && btn.onclick.toString().includes('selectMood')) {
                    mood = btn.getAttribute('data-value');
                }
            });
            
            // Get notes
            const notes = document.getElementById('dayNotes').value.trim();
            
            // Save data for this day
            if (flow || symptoms.length > 0 || mood || notes) {
                dayData[currentEditDate] = {
                    flow: flow,
                    symptoms: symptoms,
                    mood: mood,
                    notes: notes
                };
            } else if (!isPeriod) {
                // Remove data if nothing is tracked and not a period day
                delete dayData[currentEditDate];
            }
            
            saveData();
            renderCalendar();
            closeModal();
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('dayModal');
            if (event.target === modal) {
                closeModal();
            }
        }

        // Navigation
        function previousMonth() {
            currentDate.setMonth(currentDate.getMonth() - 1);
            renderCalendar();
        }

        function nextMonth() {
            currentDate.setMonth(currentDate.getMonth() + 1);
            renderCalendar();
        }

        // Clear all data
        function clearData() {
            if (confirm('Are you sure you want to clear all tracking data? This cannot be undone.')) {
                periodDays.clear();
                dayData = {};
                saveData();
                renderCalendar();
            }
        }

        // Export data
        function exportData() {
            const data = {
                periodDays: Array.from(periodDays).sort(),
                dayData: dayData,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = 'menstrual-cycle-data.json';
            link.click();
            
            URL.revokeObjectURL(url);
        }

 // Phase Info Functions
const phaseCard = document.getElementById('phaseCard');

phaseCard.addEventListener('click', () => {
    const phaseName = document
        .getElementById('currentPhase')
        .textContent
        .trim()
        .toLowerCase();

    if (!phaseName || phaseName === '--') return;

    openPhaseInfoModal(phaseName);
});

// Open the popup
async function openPhaseInfoModal(phaseName) {
    const modal = document.getElementById('phaseInfoModal');
    const modalBody = document.getElementById('phaseModalBody');

    modal.style.display = 'block';
    modalBody.innerHTML = 'Loading...';

    try {
        const response = await fetch('/api/menstrual/phase-info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phase: phaseName })
        });

        if (!response.ok) throw new Error('Failed to fetch');

        const result = await response.json();
        const phaseInfo = result.data;

        if (!phaseInfo) {
            modalBody.innerHTML = 'No information available.';
            return;
        }

        modalBody.innerHTML = `
            <h2>${phaseInfo.title}</h2>
            <p><strong>${phaseInfo.day_range}</strong></p>

            <p>${phaseInfo.summary}</p>

            <h4>What’s happening</h4>
            <p>${phaseInfo.what_is_happening}</p>

            <h4>Traits</h4>
            <ul>
                <li><strong>Physical:</strong> ${phaseInfo.traits.physical}</li>
                <li><strong>Emotional:</strong> ${phaseInfo.traits.emotional}</li>
                <li><strong>Mental:</strong> ${phaseInfo.traits.mental}</li>
            </ul>
            `;

    } catch (err) {
        modalBody.innerHTML = 'Error loading phase information.';
        console.error(err);
    }
}

// Close the popup
function closePhaseModal() {
    document.getElementById('phaseInfoModal').style.display = 'none';
}

// Close when clicking outside popup
window.addEventListener('click', event => {
    const modal = document.getElementById('phaseInfoModal');
    if (event.target === modal) closePhaseModal();
});


        // Initialize
        loadData();
        renderCalendar();

        // Provider Search Function
        function searchProviders() {
            const zipcode = document.getElementById('zipcodeInput').value.trim();
            const resultsDiv = document.getElementById('providerResults');
            
            if (!zipcode || zipcode.length !== 5 || !/^\d{5}$/.test(zipcode)) {
                resultsDiv.innerHTML = '<p style="color: #c62828; padding: 15px; background: #ffebee; border-radius: 8px;">Please enter a valid 5-digit ZIP code.</p>';
                return;
            }
            
            resultsDiv.innerHTML = '<p style="color: #999; padding: 15px;">Finding a provider near you ...</p>';
            
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

                // Custom symptom management
        function addCustomSymptom() {
            const input = document.getElementById('otherSymptomInput');
            const val = input.value.trim();
            if (!val) return;
            // Respect a cap of 10 stored custom symptoms; still allow immediate one-off logging
            const storedKey = 'customSymptoms';
            const stored = JSON.parse(localStorage.getItem(storedKey ) || '[]');
            if (stored.length >= 10) {
                // do not persist more than 10; inform user and still allow temporary use
                alert('Maximum of 10 custom symptoms saved — additional symptoms will be used for this log but not saved.');
                // create a temporary checkbox in the UI for immediate selection
                const container = document.getElementById('symptomContainer');
                const tempId = `temp_sym_${Date.now()}`;
                const label = document.createElement('label');
                label.className = 'sym-pill custom-node';
                label.style.cssText = 'display:inline-flex; align-items:center; gap:8px; padding:8px 10px; border-radius:999px; border:1px solid #fde8ef; background:#fff; cursor:pointer; margin-left:4px;';
                const cb = document.createElement('input'); cb.type = 'checkbox'; cb.id = tempId; cb.className = 'custom-sym'; cb.dataset.label = val;
                const span = document.createElement('span'); span.textContent = ' ' + val + ' 🔸';
                label.appendChild(cb); label.appendChild(span);
                container.appendChild(label);
                input.value = '';
                return;
            }

            stored.unshift(val);
            localStorage.setItem(storedKey, JSON.stringify(stored));
            input.value = '';
            renderCustomSymptoms();
        }

        function renderCustomSymptoms() {
            const container = document.getElementById('symptomContainer');
            // remove existing custom nodes
            const existing = container.querySelectorAll('.custom-node');
            existing.forEach(n => n.remove());
            const stored = JSON.parse(localStorage.getItem('customSymptoms' ) || '[]');
            stored.forEach((s, idx) => {
                const id = `custom_sym_${idx}`;
                const wrapper = document.createElement('div');
                wrapper.style.display = 'inline-flex';
                wrapper.style.alignItems = 'center';
                wrapper.style.marginLeft = '4px';

                const label = document.createElement('label');
                label.className = 'sym-pill custom-node';
                label.style.cssText = 'display:inline-flex; align-items:center; gap:8px; padding:8px 10px; border-radius:999px; border:1px solid #fde8ef; background:#fff; cursor:pointer;';
                const cb = document.createElement('input');
                cb.type = 'checkbox';
                cb.id = id;
                cb.className = 'custom-sym';
                cb.dataset.label = s;
                const span = document.createElement('span'); span.textContent = ' ' + s + ' 🔸';
                label.appendChild(cb);
                label.appendChild(span);

                const del = document.createElement('button');
                del.className = 'sym-pill';
                del.style.padding = '6px 8px';
                del.style.marginLeft = '6px';
                del.style.background = '#fff';
                del.style.color = '#c62828';
                del.style.border = '1px solid #fde8ef';
                del.style.borderRadius = '999px';
                del.style.cursor = 'pointer';
                del.style.fontSize = '14px';
                del.textContent = '✖';
                del.title = 'Delete custom symptom';
                del.onclick = () => { deleteCustomSym(idx); };

                wrapper.appendChild(label);
                wrapper.appendChild(del);
                container.appendChild(wrapper);
            });
        }

        function deleteCustomSym(idx){
            try{
                const stored = JSON.parse(localStorage.getItem('customSymptoms')||'[]');
                if(idx>=0 && idx<stored.length){ stored.splice(idx,1); localStorage.setItem('customSymptoms', JSON.stringify(stored)); renderCustomSymptoms(); }
            }catch(e){console.error(e)}
        }

        // Custom exercise management
        function showAddExerciseForm() {
            const f = document.getElementById('addExerciseForm');
            if (!f) return;
            f.style.display = 'block';
            f.scrollIntoView({behavior:'smooth'});
        }
        function hideAddExerciseForm(){ const f=document.getElementById('addExerciseForm'); if(f) f.style.display='none'; }
        function addCustomExercise(){
            const name = (document.getElementById('customExerciseName').value||'').trim();
            const targets = (document.getElementById('customExerciseTargets').value||'').trim();
            if(!name) { alert('Please provide an exercise name'); return; }
            // generate a tailored description and rationale based on name + targets + body
            const body = JSON.parse(localStorage.getItem('bodyInfo')||'{}');
            const gen = generateExerciseRecommendation(name, targets, body);
            const stored = JSON.parse(localStorage.getItem('customExercises')||'[]');
            const idx = stored.findIndex(e=> (e.name||'').toLowerCase() === name.toLowerCase());
            if(idx === -1){
                stored.unshift({ id: 'custom_'+Date.now(), name, description: gen.description, targets: gen.targets.join(', '), suggested: true });
            } else {
                stored[idx].description = gen.description || stored[idx].description;
                stored[idx].targets = gen.targets.join(', ') || stored[idx].targets;
                stored[idx].suggested = true;
            }
            localStorage.setItem('customExercises', JSON.stringify(stored));
            document.getElementById('customExerciseName').value='';
            document.getElementById('customExerciseTargets').value='';
            hideAddExerciseForm();
            renderCustomExercises();
            // immediately add the generated recommendation to recommendations area
            try{ mergeRecommendedIntoCustom([gen]); showRecommendations(); } catch(e){ console.error(e); }
            // also ask server to augment personalization
            try { fetchAndAddSuggestedExercises(); } catch(e){ /*ignore*/ }
        }

        // End-goal custom input handlers
        function showEndGoalForm(){ const f=document.getElementById('endGoalForm'); if(f){ f.style.display='block'; f.scrollIntoView({behavior:'smooth'}); } }
        function hideEndGoalForm(){ const f=document.getElementById('endGoalForm'); if(f) f.style.display='none'; }
        function saveEndGoalCustom(){ const v=(document.getElementById('endGoalInput').value||'').trim(); if(!v) return; localStorage.setItem('endGoal', v); document.getElementById('selectedGoal').textContent = v; hideEndGoalForm(); showSaveStatus(); }

        function saveBodyInfo() {
            const ft = Number(document.getElementById('userHeightFt').value || 0);
            const inch = Number(document.getElementById('userHeightIn').value || 0);
            const lbs = Number(document.getElementById('userWeightLbs').value || 0);
            const height_cm = ft*30.48 + inch*2.54;
            const weight_kg = lbs * 0.45359237;
            const info = {
                age: document.getElementById('userAge').value || '',
                height_ft: ft || '',
                height_in: inch || '',
                weight_lbs: lbs || '',
                height_cm: Math.round(height_cm*10)/10,
                weight_kg: Math.round(weight_kg*10)/10,
                bodyType: document.getElementById('bodyType').value || '',
                chars: {
                    preg: !!document.getElementById('char_preg').checked,
                    post: !!document.getElementById('char_post').checked,
                    meno: !!document.getElementById('char_meno').checked,
                    pelvic: !!document.getElementById('char_pelvic').checked,
                    osteo: !!document.getElementById('char_osteo').checked,
                    hbp: !!document.getElementById('char_hbp').checked,
                    lowfit: !!document.getElementById('char_lowfit').checked,
                    active: !!document.getElementById('char_active').checked
                }
            };
            localStorage.setItem('bodyInfo', JSON.stringify(info));
            // also persist selected end goal
            const eg = localStorage.getItem('endGoal') || '';
            if (eg) localStorage.setItem('endGoal', eg);
            try { showSaveStatus(); } catch(e){}
        }

        function showSaveStatus() {
            const el = document.getElementById('saveStatus');
            if (!el) return;
            el.style.display = 'inline-block';
            clearTimeout(el._hideTimer);
            el._hideTimer = setTimeout(() => { el.style.display = 'none'; }, 2000);
        }

        function loadGoals() {
            try {
                const stored = JSON.parse(localStorage.getItem('myGoals') || '[]');
                // populate the in-memory goals array (clear first to avoid duplicates)
                goals.length = 0;
                stored.forEach(g => { if (g && g.name) goals.push(g); });
                renderGoals();
            } catch (e) {}
        }

        function toggleGoals() {
            const sec = document.getElementById('goalsSection');
            const btn = document.getElementById('toggleGoalsBtn');
            if (!sec) return;
            if (sec.style.display === 'block') {
                sec.style.display = 'none';
                if (btn) btn.textContent = 'Add your own goal ✍️';
            } else {
                sec.style.display = 'block';
                if (btn) btn.textContent = 'Close goals ✖️';
                sec.scrollIntoView({ behavior: 'smooth' });
            }
        }

        function loadBodyInfo() {
            try {
                const info = JSON.parse(localStorage.getItem('bodyInfo') || 'null');
                if (!info) return;
                if (info.age) document.getElementById('userAge').value = info.age;
                if (info.height_ft !== undefined) document.getElementById('userHeightFt').value = info.height_ft;
                if (info.height_in !== undefined) document.getElementById('userHeightIn').value = info.height_in;
                if (info.weight_lbs !== undefined) document.getElementById('userWeightLbs').value = info.weight_lbs;
                if (info.bodyType) document.getElementById('bodyType').value = info.bodyType;
                if (info.chars) {
                    document.getElementById('char_preg').checked = !!info.chars.preg;
                    document.getElementById('char_post').checked = !!info.chars.post;
                    document.getElementById('char_meno').checked = !!info.chars.meno;
                    document.getElementById('char_pelvic').checked = !!info.chars.pelvic;
                    document.getElementById('char_osteo').checked = !!info.chars.osteo;
                    document.getElementById('char_hbp').checked = !!info.chars.hbp;
                    document.getElementById('char_lowfit').checked = !!info.chars.lowfit;
                    document.getElementById('char_active').checked = !!info.chars.active;
                }
                // load end goal display
                const eg = localStorage.getItem('endGoal') || '';
                if (eg) setEndGoal(eg);
            } catch (e) {}
        }

        function showGoalsForm() {
            document.getElementById('goalsSection').style.display = 'block';
            // scroll into view
            document.getElementById('goalsSection').scrollIntoView({ behavior: 'smooth' });
        }

        function renderGoals() {
            const ul = document.getElementById('exerciseGoalsList');
            ul.innerHTML = '';
            goals.forEach((g, i) => {
                const li = document.createElement('li');
                li.style.marginBottom = '6px';
                li.textContent = `${g.name}${g.target ? ' — ' + g.target + ' min' : ''}`;
                ul.appendChild(li);
            });
            // render persistent 'My Goals' section
            const my = document.getElementById('myGoalsList');
            if (my) {
                my.innerHTML = '';
                const stored = JSON.parse(localStorage.getItem('myGoals')||'[]');
                stored.forEach((g, idx) => {
                    const row = document.createElement('div');
                    row.style.display = 'flex';
                    row.style.justifyContent = 'space-between';
                    row.style.alignItems = 'center';
                    row.style.padding = '8px 6px';
                    row.style.borderBottom = '1px solid #f7edf2';
                    const text = document.createElement('div');
                    text.textContent = `${g.name}${g.target ? ' — ' + g.target + ' min' : ''}`;
                    const del = document.createElement('button');
                    del.className = 'sym-pill';
                    del.style.padding = '6px 10px';
                    del.style.background = '#fff';
                    del.style.color = '#c62828';
                    del.style.border = '1px solid #fde8ef';
                    del.style.borderRadius = '999px';
                    del.style.cursor = 'pointer';
                    del.style.fontSize = '14px';
                    del.title = 'Delete goal';
                    del.setAttribute('aria-label','Delete goal');
                    del.textContent = '✖';
                    del.onclick = () => { removeGoal(idx); };
                    row.appendChild(text);
                    row.appendChild(del);
                    my.appendChild(row);
                });
            }
        }

        function removeGoal(idx){
            try{
                const stored = JSON.parse(localStorage.getItem('myGoals')||'[]');
                if(idx>=0 && idx<stored.length){ stored.splice(idx,1); localStorage.setItem('myGoals', JSON.stringify(stored)); }
                // refresh in-memory goals
                goals.length = 0;
                const newStored = JSON.parse(localStorage.getItem('myGoals')||'[]');
                newStored.forEach(g=>{ if(g && g.name) goals.push(g); });
                renderGoals();
                showRecommendations();
            }catch(e){console.error(e)}
        }

        

        // end-goal helpers
        function setEndGoal(goal) {
            localStorage.setItem('endGoal', goal);
            const map = {
                'weight_loss': 'Lose weight 🔥',
                'build_muscle': 'Build muscle 💪',
                'endurance': 'Increase endurance ❤️‍🔥',
                'flexibility': 'Flexibility 🧘‍♀️',
                'general': 'General health ✨'
            };
            document.getElementById('selectedGoal').textContent = map[goal] || '';
            // Automatically fetch and add suggested exercises for this end-goal
            try { fetchAndAddSuggestedExercises(); } catch (e) { console.error('fetch suggested error', e); }
        }

        function quickActivity(type, minutes, auto=true) {
            document.getElementById('activityType').value = type;
            document.getElementById('activityMinutes').value = minutes;
            if (auto) logActivity();
        }

        // Body type helper removed; users choose from inclusive select

        function renderLogs() {
            const el = document.getElementById('exerciseLogs');
            el.innerHTML = '';
            logs.forEach(l => {
                const d = document.createElement('div');
                d.style.padding = '12px';
                d.style.borderBottom = '1px solid #f7edf2';
                d.style.display = 'flex';
                d.style.justifyContent = 'space-between';
                d.style.alignItems = 'flex-start';

                const left = document.createElement('div');
                left.style.maxWidth = '70%';
                const title = document.createElement('div');
                title.innerHTML = `<strong style="color:#333">${l.type}</strong> — <span style="color:#666">${l.minutes} min</span>`;
                left.appendChild(title);

                if (l.symptoms && l.symptoms.length) {
                    const pills = document.createElement('div');
                    pills.style.marginTop = '8px';
                    pills.style.display = 'flex';
                    pills.style.flexWrap = 'wrap';
                    pills.style.gap = '6px';
                    l.symptoms.forEach(s => {
                        const p = document.createElement('div');
                        p.style.background = '#fff5f8';
                        p.style.padding = '6px 8px';
                        p.style.borderRadius = '999px';
                        p.style.fontSize = '13px';
                        p.style.color = '#c62828';
                        p.textContent = `${s.key} ${s.icon || ''}`;
                        pills.appendChild(p);
                    });
                    left.appendChild(pills);
                }

                const right = document.createElement('div');
                right.style.textAlign = 'right';
                right.style.fontSize = '12px';
                right.style.color = '#666';
                right.textContent = l.ts;

                const del = document.createElement('button');
                del.className = 'sym-pill';
                del.style.padding = '6px 10px';
                del.style.marginTop = '6px';
                del.style.background = '#fff';
                del.style.color = '#c62828';
                del.style.border = '1px solid #fde8ef';
                del.style.borderRadius = '999px';
                del.style.cursor = 'pointer';
                del.style.fontSize = '14px';
                del.title = 'Delete log entry';
                del.setAttribute('aria-label','Delete log entry');
                del.textContent = '✖';
                del.onclick = () => { deleteLog(logs.indexOf(l)); };
                right.appendChild(document.createElement('br'));
                right.appendChild(del);

                d.appendChild(left);
                d.appendChild(right);
                el.appendChild(d);
            });
        }

        function deleteLog(idx){
            try{
                if(idx>=0 && idx<logs.length){ logs.splice(idx,1); renderLogs(); }
            }catch(e){console.error(e)}
        }

        function checkRedFlag(entry) {
            // Deprecated: server-based assessment now used
            return false;
        }

        function showRedFlag(flag, reasons) {
            const redEl = document.getElementById('redFlag');
            if (!flag) { redEl.style.display = 'none'; redEl.innerHTML = ''; return; }
            redEl.style.display = 'block';
            const list = (reasons || []).map(r => `<li style="margin-bottom:6px;">${r}</li>`).join('');
            redEl.innerHTML = `<strong>Red flag:</strong> Concerning signs detected. <ul style="margin-top:8px; padding-left:18px; color:#611;">${list}</ul>`;
        }

        // Breathing exercise helpers
        let breathInterval = null;
        function showBreathingModal() {
            const m = document.getElementById('breathingModal');
            if (!m) return;
            m.style.display = 'block';
        }

        function closeBreathing() {
            const m = document.getElementById('breathingModal');
            if (!m) return;
            m.style.display = 'none';
            if (breathInterval) { clearInterval(breathInterval); breathInterval = null; }
            document.getElementById('breathText').textContent = 'Get ready...';
        }

        function startBreathing(inhale=4, hold=2, exhale=4) {
            const text = document.getElementById('breathText');
            if (!text) return;
            let phase = 0; // 0 inhale,1 hold,2 exhale
            let timer = inhale;
            text.textContent = `Breathe in — ${timer}`;
            if (breathInterval) clearInterval(breathInterval);
            breathInterval = setInterval(() => {
                timer -= 1;
                if (timer <= 0) {
                    phase = (phase + 1) % 3;
                    if (phase === 0) timer = inhale;
                    else if (phase === 1) timer = hold;
                    else timer = exhale;
                }
                if (phase === 0) text.textContent = `Breathe in — ${timer}`;
                else if (phase === 1) text.textContent = `Hold — ${timer}`;
                else text.textContent = `Breathe out — ${timer}`;
            }, 1000);
        }

        // Show a short breathing prompt and load saved data on app load
        window.addEventListener('load', () => {
            // clear persisted custom symptoms on page refresh per user request
            try { localStorage.removeItem('customSymptoms'); } catch(e){}
            // delay slightly so UI paints
            setTimeout(showBreathingModal, 600);
            // load custom symptoms and body info
            try { renderCustomSymptoms(); } catch(e){}
            try { loadBodyInfo(); } catch(e){}
            try { loadGoals(); } catch(e){}
            try { /* ensure customExercises exists */ if(!localStorage.getItem('customExercises')) localStorage.setItem('customExercises','[]'); } catch(e){}
            try { renderCustomExercises(); } catch(e){}
        });

        function renderCustomExercises(){
            const container = document.getElementById('customExercisesList');
            if(!container) return;
            container.innerHTML = '';
            const stored = JSON.parse(localStorage.getItem('customExercises')||'[]');
            stored.forEach((c, idx)=>{
                const row = document.createElement('div');
                row.style.display='flex'; row.style.justifyContent='space-between'; row.style.alignItems='center'; row.style.padding='8px 6px'; row.style.borderBottom='1px solid #f7edf2';
                const left = document.createElement('div'); left.style.fontSize='14px';
                const title = document.createElement('div'); title.style.fontWeight='600'; title.style.color='#333'; title.textContent = c.name || '';
                const desc = document.createElement('div'); desc.style.fontSize='13px'; desc.style.color='#666'; desc.style.marginTop='4px'; desc.textContent = c.description || (c.targets? ('Targets: '+c.targets) : '');
                left.appendChild(title); if(desc.textContent) left.appendChild(desc);
                if(c.prescription){ const presNode = document.createElement('div'); presNode.style.fontSize='13px'; presNode.style.color='#444'; presNode.style.marginTop='6px'; presNode.textContent = formatPrescription(c.prescription); left.appendChild(presNode); }
                if(c.suggested){
                    const badge = document.createElement('div'); badge.style.display='inline-block'; badge.style.marginTop='6px'; badge.style.marginLeft='6px'; badge.style.padding='4px 8px'; badge.style.borderRadius='999px'; badge.style.background='#fff0f6'; badge.style.color='#c2185b'; badge.style.fontSize='12px'; badge.textContent='Suggested'; left.appendChild(badge);
                }
                const del = document.createElement('button'); del.className='sym-pill'; del.style.padding='6px 10px'; del.style.background='#fff'; del.style.color='#c62828'; del.style.border='1px solid #fde8ef'; del.style.borderRadius='999px'; del.style.cursor='pointer'; del.style.fontSize='14px'; del.title='Delete exercise'; del.setAttribute('aria-label','Delete exercise'); del.textContent='✖'; del.onclick = ()=>{ deleteCustomExercise(idx); };
                row.appendChild(left); row.appendChild(del); container.appendChild(row);
            });
        }

        // Merge recommended exercises (from server) into local customExercises storage
        function mergeRecommendedIntoCustom(recs){
            if(!recs || !recs.length) return;
            try{
                const stored = JSON.parse(localStorage.getItem('customExercises')||'[]');
                const seen = new Set(stored.map(s=> (s.name||'').toLowerCase()));
                recs.forEach(r=>{
                    const name = (r.name||'').trim();
                    if(!name) return;
                    if(seen.has(name.toLowerCase())) return;
                    stored.unshift({ id: r.id||('rec_'+Date.now()), name: r.name, description: r.description||'', targets: (Array.isArray(r.targets)? r.targets.join(', ') : (r.targets||'')), suggested: true, prescription: (r.prescription || r.pres || null) });
                    seen.add(name.toLowerCase());
                });
                localStorage.setItem('customExercises', JSON.stringify(stored));
                renderCustomExercises();
            }catch(e){ console.error('mergeRecommendedIntoCustom', e); }
        }

        // Fetch recommendations from server and merge them into customExercises (used when end-goal is set)
        async function fetchAndAddSuggestedExercises(){
            try{
                const body = JSON.parse(localStorage.getItem('bodyInfo')||'{}');
                const payload = { age: Number(body.age)||null, height_cm: Number(body.height_cm)||null, weight_kg: Number(body.weight_kg)||null, bodyType: body.bodyType||'', chars: body.chars||{}, endGoal: localStorage.getItem('endGoal')||'', goals: JSON.parse(localStorage.getItem('myGoals')||'[]'), customExercises: JSON.parse(localStorage.getItem('customExercises')||'[]') };
                const resp = await fetch('/api/fitness/llm_recommend',{ method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
                const data = await resp.json();
                if(data && data.status === 'success'){
                    mergeRecommendedIntoCustom(data.recommendations || data.exercises || []);
                    showRecommendations();
                }
            }catch(e){ console.error('fetchAndAddSuggestedExercises', e); }
        }

        // Generate a local tailored exercise recommendation based on name, targets and user body
        function generateExerciseRecommendation(name, targetsStr, body){
            const targets = (targetsStr||'').split(',').map(s=>s.trim()).filter(Boolean);
            const lname = (name||'').trim();
            const base = lname.charAt(0).toUpperCase() + lname.slice(1);
            const descriptionParts = [];
            if(targets.includes('cardio') || targets.includes('aerobic')) descriptionParts.push('Great for cardiovascular fitness; try intervals or sustained pace.');
            if(targets.includes('lower') || targets.includes('legs')) descriptionParts.push('Emphasize controlled movement and progressive sets to build lower-body strength.');
            if(targets.includes('upper') ) descriptionParts.push('Include upper-body progression or carries as complementary work.');
            if(targets.includes('flexibility') || targets.includes('mobility')) descriptionParts.push('Add dynamic mobility and cool-down stretches focused on target joints.');
            if(!descriptionParts.length) descriptionParts.push('Can be adapted for strength, cardio, or mobility depending on targets.');
            // tailor small note for pregnancy/postpartum/osteo
            if(body && body.chars){
                if(body.chars.preg) descriptionParts.push('Use pregnancy-safe modifications and consult provider if unsure.');
                if(body.chars.osteo) descriptionParts.push('Focus on controlled, load-managed strength progressions for bone health.');
                if(body.chars.lowfit) descriptionParts.push('Start with shorter durations and lower intensity, progress gradually.');
            }
            const description = descriptionParts.join(' ');
            const rationale = `Suggested because it matches targets: ${targets.join(', ')}`;
            return { id: 'local_'+Date.now(), name: base, description, targets: targets, rationale };
        }

        function deleteCustomExercise(idx){ try{ const stored = JSON.parse(localStorage.getItem('customExercises')||'[]'); if(idx>=0 && idx<stored.length){ stored.splice(idx,1); localStorage.setItem('customExercises', JSON.stringify(stored)); renderCustomExercises(); showRecommendations(); } }catch(e){console.error(e)} }

    </script>
</body>
</html>
"""

engine = SymptomNutritionEngine()
print("Nutrition Engine ready!")

provider_searcher = ProviderSearcher()
print("=" * 60)


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

@app.route('/api/menstrual/phase-info', methods=['POST'])
def get_phase_info():
    phase = request.json.get('phase')

    with open("back/tracker.json") as f:
        data = json.load(f)

    return jsonify({
        "data": data.get(phase.lower(), {})
    })

@app.route('/api/fitness/diet', methods=['GET', 'POST'])
def diet_tracker():
    return {"status": "success", "message": "Diet tracker endpoint"}

@app.route('/api/fitness/exercise', methods=['GET', 'POST'])
def exercise_tracker():
    return {"status": "success", "message": "Exercise tracker endpoint"}


#start
@app.route('/api/fitness/exercises', methods=['GET'])
def exercises_dataset():
    """Return exercise recommendations dataset as JSON"""
    import json, os, time
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, '..', 'data', 'exercise_recommendations.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {"status": "success", "exercises": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route('/api/fitness/llm_recommend', methods=['POST'])
def llm_recommend():
    """Endpoint that can be used to request LLM-curated recommendations.
    Currently returns heuristic recommendations; placeholder for integrating an LLM or external API.
    """
    data = None
    try:
        from flask import request
        data = request.get_json() or {}
    except Exception:
        data = {}

    # Basic heuristic fallback: reuse existing dataset filtering
    import json, os
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, '..', 'data', 'exercise_recommendations.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
    except Exception as e:
        return {"status": "error", "message": f"dataset load error: {e}"}

    # accept client-provided custom exercises and append as candidates
    try:
        custom_in = data.get('custom_exercises') or data.get('customExercises') or []
        if custom_in and isinstance(custom_in, list):
            def infer_type_from_text(txt):
                t = (txt or '').lower()
                if any(k in t for k in ['walk','run','jog','bike','cycle','cardio','ellipt']):
                    return 'cardio'
                if any(k in t for k in ['squat','deadlift','press','strength','resistance','band']):
                    return 'strength'
                if any(k in t for k in ['yoga','stretch','mobility','pilates']):
                    return 'flexibility'
                return 'general'

            for i, c in enumerate(custom_in):
                try:
                    cid = c.get('id') if isinstance(c, dict) and c.get('id') else f'custom_{i}_{int(time.time())}'
                    name = (c.get('name') or c.get('title') or '').strip()
                    desc = c.get('description') if isinstance(c, dict) else ''
                    targets_raw = c.get('targets') if isinstance(c, dict) else ''
                    # normalize targets into list
                    if isinstance(targets_raw, list):
                        targets_list = targets_raw
                    elif isinstance(targets_raw, str):
                        targets_list = [t.strip() for t in targets_raw.split(',') if t.strip()]
                    else:
                        targets_list = []
                    ex_entry = {
                        'id': cid,
                        'name': name or f'Custom Exercise {i+1}',
                        'description': desc or '',
                        'type': infer_type_from_text(' '.join(targets_list) + ' ' + (name or '')),
                        'impact': 'low',
                        'targets': targets_list,
                        'recommended_for': []
                    }
                    exercises.append(ex_entry)
                except Exception:
                    continue
    except Exception:
        pass

    # parse incoming data
    age = int(data.get('age') or 0)
    height_cm = float(data.get('height_cm') or 0)
    weight_kg = float(data.get('weight_kg') or 0)
    bodyType = (data.get('bodyType') or '').lower()
    endGoal = (data.get('endGoal') or '').lower()
    goals_list = data.get('goals') or []
    chars = data.get('chars') or {}

    # Normalize and de-duplicate incoming goals by name+target (case-insensitive)
    try:
        unique = []
        seen = set()
        for g in goals_list:
            name = (g.get('name') or '').strip()
            target = str(g.get('target') or '').strip()
            if not name:
                continue
            # de-duplicate by goal name only (ignore minor target differences)
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append({'name': name, 'target': target})
        goals_list = unique
    except Exception:
        pass

    bmi = None
    try:
        if height_cm and weight_kg:
            bmi = weight_kg / ((height_cm/100.0)**2)
    except Exception:
        bmi = None

    candidates = []
    for e in exercises:
        # filter by age suitability
        if age and (age < e.get('suitable_age_min', 0) or age > e.get('suitable_age_max', 999)):
            continue
        candidates.append(e)

    def score_ex(e):
        s = 0
        etype = (e.get('type') or '').lower()
        # normalize targets to a string for matching
        raw_targets = e.get('targets') or []
        if isinstance(raw_targets, list):
            targets = ' '.join([str(t) for t in raw_targets]).lower()
        else:
            targets = str(raw_targets).lower()
        impact = (e.get('impact') or '').lower()

        # bodyType match (stronger boost)
        rec_for = [r.lower() for r in (e.get('recommended_for') or [])]
        if bodyType and bodyType in rec_for:
            s += 4

        # endGoal boosts
        if endGoal == 'weight_loss':
            if 'cardio' in etype or 'cardio' in targets: s += 4
            if impact and 'low' in impact: s += 1
        if endGoal == 'build_muscle':
            if 'strength' in etype or 'strength' in targets or 'resistance' in targets: s += 5
        if endGoal == 'endurance' and 'cardio' in etype: s += 3
        if endGoal == 'flexibility' and ('flexibility' in etype or 'mobility' in targets): s += 4
        if endGoal == 'general': s += 1

        # typed goals (from user-added goals)
        for g in goals_list:
            gtxt = (g.get('name') or '').lower()
            if not gtxt: continue
            # match against targets and name
            if any(tok in targets for tok in gtxt.split()): s += 2
            if any(tok in (e.get('name') or '').lower() for tok in gtxt.split()): s += 2

        # BMI considerations
        try:
            if bmi and bmi >= 30 and impact and 'low' in impact: s += 2
        except Exception:
            pass

        # characteristics
        if chars.get('pelvic') and e.get('id') == 'pelvic_floor_exercises': s += 6
        if chars.get('preg') and e.get('id') == 'pelvic_floor_exercises': s += 5
        if chars.get('post') and e.get('id') == 'pelvic_floor_exercises': s += 4
        if chars.get('osteo') and ('strength' in etype or 'resistance' in etype or 'weight' in targets): s += 3
        if chars.get('hbp'):
            # de-prioritize high-impact cardio
            if 'cardio' in etype and impact and 'high' in impact: s -= 3
        if chars.get('lowfit'):
            if impact and 'high' in impact: s -= 2
            if impact and 'low' in impact: s += 1

        # body shape specific boosts
        if bodyType in ['pear','curvy'] and 'lower' in targets: s += 2
        if bodyType in ['apple'] and 'upper' in targets: s += 2

        # age-based adjustments
        if age and age >= 65:
            if impact and 'low' in impact: s += 2
            if 'strength' in etype: s += 2

        return s

    # helper to create a prescription for an exercise based on profile
    def make_prescription(e):
        etype = (e.get('type') or '').lower()
        impact = (e.get('impact') or '').lower()
        targets = e.get('targets') or []
        pres = {}
        # defaults
        if 'strength' in etype or any('strength' in str(t).lower() for t in targets):
            pres['sets'] = 3
            pres['reps'] = '8-12'
            pres['frequency_per_week'] = 2 if age and age>=65 else 3
            pres['intensity'] = 'moderate'
        elif 'cardio' in etype or any(t in ['cardio','aerobic'] for t in [str(x).lower() for x in targets]):
            pres['duration_min'] = 30
            pres['frequency_per_week'] = 3
            pres['intensity'] = 'moderate'
        elif 'flexibility' in etype or 'mobility' in etype or any('flex' in str(t).lower() for t in targets):
            pres['duration_min'] = 15
            pres['frequency_per_week'] = 3
            pres['intensity'] = 'low'
        else:
            pres['duration_min'] = 20
            pres['frequency_per_week'] = 2
            pres['intensity'] = 'moderate'

        # adjust for low fitness
        try:
            if chars.get('lowfit'):
                if 'sets' in pres:
                    pres['sets'] = max(1, pres['sets'] - 1)
                if 'reps' in pres:
                    # lower rep range
                    pres['reps'] = '6-10'
                if 'duration_min' in pres:
                    pres['duration_min'] = max(10, int(pres['duration_min']*0.6))
                pres['intensity'] = 'low'
        except Exception:
            pass

        # adjust for older age
        try:
            if age and age >= 65:
                if 'sets' in pres:
                    pres['sets'] = max(1, pres['sets'] - 1)
                if 'duration_min' in pres:
                    pres['duration_min'] = max(8, int(pres['duration_min']*0.75))
                pres['frequency_per_week'] = max(1, pres.get('frequency_per_week',2) - 1)
                pres['intensity'] = 'low'
        except Exception:
            pass

        # consider BMI and impact
        try:
            if bmi and bmi >= 30 and impact and 'high' in impact:
                # reduce impact and duration
                if 'duration_min' in pres:
                    pres['duration_min'] = max(10, int(pres['duration_min']*0.7))
                pres['intensity'] = 'low'
        except Exception:
            pass

        return pres

    scored = sorted(candidates, key=score_ex, reverse=True)
    # return top 6 recommendations (trim internal fields)
    top = []
    for ex in scored[:6]:
        # build a short rationale for why this exercise was recommended
        reasons = []
        if bodyType and bodyType in [r.lower() for r in (ex.get('recommended_for') or [])]:
            reasons.append('Matches suggested body type considerations.')
        if endGoal and ((endGoal == 'weight_loss' and ('cardio' in (ex.get('type') or '').lower())) or (endGoal == 'build_muscle' and ('strength' in (ex.get('type') or '').lower()))):
            reasons.append(f'Aligned with goal: {endGoal.replace("_"," ")}.')
        if chars.get('pelvic') and ex.get('id') == 'pelvic_floor_exercises':
            reasons.append('Recommended for pelvic floor support.')
        if chars.get('preg') and ex.get('id') == 'pelvic_floor_exercises':
            reasons.append('Safe option for pregnancy/postpartum adaptations.')
        if bmi and bmi >= 30 and (ex.get('impact') or '').lower().startswith('low'):
            reasons.append('Low-impact choice suitable for higher BMI.')

        pres = make_prescription(ex)
        top.append({
            'id': ex.get('id'), 'name': ex.get('name'), 'type': ex.get('type'),
            'impact': ex.get('impact'), 'targets': ex.get('targets'), 'description': ex.get('description'),
            'rationale': ' '.join(reasons), 'prescription': pres
        })
    # build a simple actionable plan when user provided goals
    plan = []
    try:
        if goals_list:
            for g in goals_list:
                gname = (g.get('name') or '').strip()
                if not gname: continue
                # pick top matching exercises for this goal
                tokens = [t.lower() for t in gname.split()]
                matches = []
                for e in scored:
                    text = ' '.join([e.get('name',''), ' '.join(e.get('targets') or [])]).lower()
                    if any(tok in text for tok in tokens):
                        matches.append(e)
                if not matches:
                    matches = scored
                ex_objs = []
                for m in matches[:3]:
                    if not m: continue
                    try:
                        pres = make_prescription(m)
                    except Exception:
                        pres = {}
                    ex_name = m.get('name')
                    if ex_name:
                        ex_objs.append({'name': ex_name, 'prescription': pres})
                # ensure unique by name
                seen_ex = set()
                uniq_ex_objs = []
                for o in ex_objs:
                    n = o.get('name') if isinstance(o, dict) else o
                    if not n: continue
                    if n in seen_ex: continue
                    seen_ex.add(n)
                    uniq_ex_objs.append(o)
                ex_objs = uniq_ex_objs
                # heuristic schedule (personalized)
                schedule = '3x/week, 20-40 min per session'
                g_lower = gname.lower()
                if 'run' in g_lower or 'cardio' in g_lower:
                    schedule = '3x/week run or brisk walk, 20-30 min'
                if 'strength' in g_lower or 'muscle' in g_lower:
                    schedule = '2-3x/week strength sessions, 20-40 min'
                # adapt for low fitness or older age
                try:
                    if chars.get('lowfit'):
                        schedule = schedule.replace('20-40','10-20').replace('20-30','10-20')
                    if age and age >= 65:
                        # reduce intensity and duration for older adults
                        schedule = schedule.replace('3x/week','2x/week').replace('2-3x/week','2x/week').replace('20-40','10-25').replace('20-30','10-20')
                except Exception:
                    pass
                rationale = f"Plan supports goal '{gname}' by prioritizing these exercises based on your profile."
                plan.append({'goal': gname, 'schedule': schedule, 'exercises': ex_objs, 'rationale': rationale})
    except Exception:
        plan = []

    return {"status": "success", "recommendations": top, "plan": plan}


@app.route('/api/fitness/assess_activity', methods=['POST'])
def assess_activity():
    """Assess a logged activity for potential red flags.
    Expects JSON: { type, minutes, symptoms, ts }
    Returns: { flag: bool, reasons: [str] }
    """
    try:
        from flask import request
        payload = request.get_json() or {}
    except Exception:
        payload = {}

    typ = (payload.get('type') or '').lower()
    minutes = int(payload.get('minutes') or 0)
    symptoms = payload.get('symptoms') or []
    ts = payload.get('ts') or ''

    reasons = []
    flag = False

    # normalize symptom keys
    keys = [ (s.get('key') or '').lower() for s in symptoms ]

    # immediate high-priority symptoms
    high = ['chest pain', 'shortness of breath', 'shortness of breath', 'fainting / near-faint', 'severe pain']
    for h in high:
        if h in keys:
            flag = True
            reasons.append(f'Presence of high-priority symptom: {h}. Seek immediate medical evaluation.')

    # activity-symptom interaction
    if symptoms and typ in ['run','sprint','interval','hiit'] and minutes >= 15:
        flag = True
        reasons.append('High-intensity activity with symptoms — stop activity and evaluate.')

    if symptoms and typ in ['strength','weightlifting'] and minutes >= 20:
        flag = True
        reasons.append('Strenuous resistance activity combined with symptoms — consider resting and seeking care if symptoms persist.')

    # long-duration with symptoms
    if symptoms and minutes >= 60:
        flag = True
        reasons.append('Long duration exercise with symptoms — may indicate overexertion or dehydration.')

    # also flag (or warn) based on activity type and duration even without symptoms
    if not symptoms:
        if typ in ['run','cycling','bike'] and minutes >= 120:
            flag = True
            reasons.append('Very long-duration cardio session — elevated risk of dehydration/overuse; monitor closely.')
        if typ in ['hiit','interval','sprint'] and minutes >= 45:
            flag = True
            reasons.append('Extended high-intensity session — ensure adequate recovery and stop if you feel unwell.')
        if minutes >= 180:
            flag = True
            reasons.append('Extremely long exercise duration — consider medical guidance for very long sessions.')

    # time-of-day heuristic: unusual late-night/early-morning activity with symptoms
    try:
        import dateutil.parser as dp
        dt = None
        try:
            dt = dp.parse(ts)
        except Exception:
            dt = None
        if dt:
            if dt.hour >= 0 and dt.hour <= 5 and symptoms:
                flag = True
                reasons.append('Activity logged at late/early hours while symptomatic — consider seeking immediate care if severe.')
    except Exception:
        # dateutil may not exist; skip deep time parsing
        pass

    # default informational reasons when not flagged but symptoms present
    if not flag and symptoms:
        reasons.append('Mild symptoms noted — monitor symptoms and rest if needed.')

    return { 'flag': bool(flag), 'reasons': reasons }

@app.route('/exercise', methods=['GET'])
def exercise_page():
    """Serve the consolidated standalone exercise HTML file.
    All exercise UI, CSS and JS are in `front/exercise.html`.
    """
    try:
        return render_template('front/exercise.html')
    except Exception:
        # fallback: simple JSON response if file missing
        return {"status": "error", "message": "Exercise page not found"}, 500

@app.route('/api/model/status', methods=['GET'])
def model_status():
    """Return whether a local model is available and where it's loaded from."""
    try:
        from chat.rag import get_rag
        rag = get_rag()
        loaded = rag.is_ready()
        return {"status": "success", "model_loaded": bool(loaded), "local_path": getattr(rag, 'model_path', None)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route('/api/model/generate', methods=['POST'])
def model_generate():
    """Generate text with local model (if available). POST JSON { prompt: "..." }"""
    try:
        from flask import request
        payload = request.get_json() or {}
        prompt = payload.get('prompt') or payload.get('message') or ''
    except Exception:
        prompt = ''

    try:
        from chat.rag import get_rag
        rag = get_rag()
        ok = rag.load()
        if not ok:
            return {"status": "error", "message": "Model not available locally. Install transformers/torch or set LOCAL_LLM_PATH."}
        out = rag.generate(prompt)
        return {"status": "success", "output": out}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# @app.route('/api/chatbot', methods=['POST'])
# def chatbot():
#     try:
#         data = request.json
#         user_msg = data.get("message", "")
#         print(f"\n{'='*60}")
#         print(f"User: {user_msg}")
        
#         if not user_msg:
#             return jsonify({"reply": "Please enter a message."})
        
#         # Generate response using RAG
#         reply = rag_system.generate_response(user_msg, top_k=3, verbose=True)
        
#         print(f"Assistant: {reply}")
#         print(f"{'='*60}\n")
        
#         return jsonify({"reply": reply})
        
#     except Exception as e:
#         print(f"Error in chatbot endpoint: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({"reply": "Sorry, I encountered an error processing your message."}), 500


@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        user_msg = data.get("message", "")
        print(f"\n{'='*60}")
        print(f"User: {user_msg}")
        
        if not user_msg:
            return jsonify({"reply": "Please enter a message."})
        
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

@app.route('/api/chatbot/feedback', methods=['POST'])
def chatbot_feedback():
    """Handle thumbs up/down feedback"""
    try:
        data = request.json
        feedback = data.get('feedback')  
        question = data.get('question')
        answer = data.get('answer')
        
        print(f"\n{'='*60}")
        print(f"Feedback: {feedback}")
        print(f"Q: {question}")
        print(f"A: {answer[:100]}...")
        
        if feedback == 'up':
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
            print("Regenerating response")
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
                'message': 'Generated a new response. Is this better?'
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

@app.route('/api/providers/search', methods=['POST'])
def search_providers():
    try:
        data = request.json
        zipcode = data.get('zipcode', '').strip()
        
        if not zipcode or len(zipcode) != 5 or not zipcode.isdigit():
            return jsonify({
                'success': False,
                'error': 'Please enter a valid 5-digit ZIP code'
            }), 400
        
        print(f"Searching providers in {zipcode}")
        
        coords = provider_searcher.get_coordinates_from_zipcode(zipcode)
        
        if not coords:
            return jsonify({
                'success': False,
                'error': 'Could not find location for this ZIP code'
            }), 404
        
        lat, lon = coords
        print(f"Coordinates: {lat}, {lon}")
        
        providers = provider_searcher.search_providers_overpass(lat, lon, radius_km=25)
        
        providers = provider_searcher.add_planned_parenthood_locations(providers)
        
        mental_health = provider_searcher.get_mental_health_resources()
        
        print(f"Found {len(providers)} providers")
        
        return jsonify({
            'success': True,
            'zipcode': zipcode,
            'location': f"{lat}, {lon}",
            'providers': providers[:20],  # Limit to 20 results
            'mental_health_resources': mental_health
        })
        
    except Exception as e:
        print(f"Error searching providers: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'An error occurred while searching for providers'
        }), 500

if __name__ == '__main__':
    print("\nStarting Flask server on http://localhost:5001")
    print("Chat interface ready!")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)
