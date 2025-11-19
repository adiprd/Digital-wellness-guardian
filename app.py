from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import json
import random
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

# Setup matplotlib untuk non-GUI environment
plt.switch_backend('Agg')

app = Flask(__name__)
app.secret_key = 'digital_wellness_secret_2024'

class DigitalWellnessAnalyzer:
    def __init__(self):
        self.usage_data = None
        self.mood_data = None
        self.intervention_data = None
        
    def load_data(self):
        """Load data dari file CSV"""
        try:
            self.usage_data = pd.read_csv('data/digital_usage.csv')
            self.mood_data = pd.read_csv('data/mood_tracking.csv')
            self.intervention_data = pd.read_csv('data/interventions.csv')
            
            # Convert date columns
            self.usage_data['date'] = pd.to_datetime(self.usage_data['date'])
            self.mood_data['date'] = pd.to_datetime(self.mood_data['date'])
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_usage_patterns(self):
        """Analisis pola penggunaan digital"""
        # Daily usage summary
        daily_usage = self.usage_data.groupby('date').agg({
            'screen_time_minutes': 'sum',
            'social_media_minutes': 'sum',
            'productive_minutes': 'sum'
        }).reset_index()
        
        # App usage patterns
        app_usage = self.usage_data.groupby('app_category').agg({
            'usage_minutes': 'sum',
            'session_count': 'sum'
        }).reset_index()
        
        # Addiction scoring
        addiction_metrics = self.calculate_addiction_score()
        
        return {
            'daily_usage': daily_usage,
            'app_usage': app_usage,
            'addiction_metrics': addiction_metrics
        }
    
    def calculate_addiction_score(self):
        """Hitung skor kecanduan digital"""
        # Analisis weekly patterns
        weekly_usage = self.usage_data.groupby('date').agg({
            'screen_time_minutes': 'sum',
            'social_media_minutes': 'sum',
            'unlock_count': 'sum'
        }).reset_index()
        
        weekly_usage['day_of_week'] = weekly_usage['date'].dt.day_name()
        
        # Skor berdasarkan kriteria
        avg_daily_screen_time = weekly_usage['screen_time_minutes'].mean()
        avg_social_media_time = weekly_usage['social_media_minutes'].mean()
        avg_unlocks = weekly_usage['unlock_count'].mean()
        
        # Scoring system
        screen_time_score = min(100, (avg_daily_screen_time / 480) * 100)  # 8 jam = 100%
        social_media_score = min(100, (avg_social_media_time / 180) * 100)  # 3 jam = 100%
        unlock_score = min(100, (avg_unlocks / 100) * 100)  # 100 unlocks = 100%
        
        overall_score = (screen_time_score + social_media_score + unlock_score) / 3
        
        # Kategori kecanduan
        if overall_score < 25:
            addiction_level = "Low"
            risk_color = "green"
        elif overall_score < 50:
            addiction_level = "Moderate" 
            risk_color = "orange"
        elif overall_score < 75:
            addiction_level = "High"
            risk_color = "red"
        else:
            addiction_level = "Severe"
            risk_color = "darkred"
        
        return {
            'overall_score': round(overall_score, 1),
            'addiction_level': addiction_level,
            'risk_color': risk_color,
            'screen_time_score': round(screen_time_score, 1),
            'social_media_score': round(social_media_score, 1),
            'unlock_score': round(unlock_score, 1),
            'avg_daily_screen_time': round(avg_daily_screen_time, 1),
            'avg_social_media_time': round(avg_social_media_time, 1),
            'avg_unlocks': round(avg_unlocks, 1)
        }
    
    def analyze_mood_correlation(self):
        """Analisis korelasi antara screen time dan mood"""
        # Merge usage dan mood data
        merged_data = pd.merge(
            self.usage_data.groupby('date').agg({
                'screen_time_minutes': 'sum',
                'social_media_minutes': 'sum'
            }).reset_index(),
            self.mood_data,
            on='date',
            how='inner'
        )
        
        if len(merged_data) == 0:
            return None
            
        # Hitung korelasi
        screen_mood_corr = merged_data['screen_time_minutes'].corr(merged_data['mood_score'])
        social_mood_corr = merged_data['social_media_minutes'].corr(merged_data['mood_score'])
        
        # Mood trends by usage level
        merged_data['usage_level'] = pd.cut(merged_data['screen_time_minutes'], 
                                          bins=[0, 120, 240, 480, 1000],
                                          labels=['Low', 'Moderate', 'High', 'Very High'])
        
        mood_by_usage = merged_data.groupby('usage_level')['mood_score'].mean()
        
        return {
            'screen_mood_correlation': round(screen_mood_corr, 3),
            'social_mood_correlation': round(social_mood_corr, 3),
            'mood_by_usage': mood_by_usage.to_dict(),
            'merged_data': merged_data
        }
    
    def generate_interventions(self, addiction_metrics):
        """Generate intervensi personalized berdasarkan analisis"""
        interventions = []
        
        # Screen time interventions
        if addiction_metrics['screen_time_score'] > 50:
            interventions.append({
                'type': 'screen_time',
                'title': 'Screen Time Limit',
                'description': f"Your daily screen time is {addiction_metrics['avg_daily_screen_time']} minutes. Try setting a 2-hour limit.",
                'priority': 'high',
                'action': 'Set app limits in settings'
            })
        
        # Social media interventions
        if addiction_metrics['social_media_score'] > 40:
            interventions.append({
                'type': 'social_media',
                'title': 'Social Media Break',
                'description': f"You spend {addiction_metrics['avg_social_media_time']} minutes daily on social media. Take a 24-hour break.",
                'priority': 'medium',
                'action': 'Disable notifications for social apps'
            })
        
        # Phone usage interventions
        if addiction_metrics['unlock_score'] > 60:
            interventions.append({
                'type': 'phone_usage',
                'title': 'Reduce Phone Checking',
                'description': f"You unlock your phone {addiction_metrics['avg_unlocks']} times daily. Try keeping it out of reach.",
                'priority': 'medium',
                'action': 'Enable grayscale mode'
            })
        
        # Add general wellness interventions
        interventions.extend([
            {
                'type': 'wellness',
                'title': 'Digital Sunset',
                'description': 'No screens 1 hour before bedtime for better sleep quality.',
                'priority': 'low',
                'action': 'Set a daily reminder at 9 PM'
            },
            {
                'type': 'wellness', 
                'title': 'Mindful Morning',
                'description': 'Start your day without phone for first 30 minutes after waking up.',
                'priority': 'low',
                'action': 'Leave phone outside bedroom'
            }
        ])
        
        return interventions
    
    def suggest_offline_activities(self, user_interests=None):
        """Saran aktivitas offline berdasarkan interest"""
        if user_interests is None:
            user_interests = ['reading', 'sports', 'creative', 'social', 'nature']
        
        activities_db = {
            'reading': [
                'Visit local library',
                'Start a physical book club',
                'Journal writing session',
                'Read in a park'
            ],
            'sports': [
                '30-minute walk or run',
                'Yoga or stretching session',
                'Try a new sport',
                'Home workout routine'
            ],
            'creative': [
                'Drawing or painting',
                'Learn a musical instrument',
                'Cooking new recipe',
                'DIY craft project'
            ],
            'social': [
                'Meet friends for coffee',
                'Family board game night',
                'Community volunteering',
                'Join a local club'
            ],
            'nature': [
                'Park walk or hike',
                'Gardening',
                'Outdoor photography',
                'Beach or lake visit'
            ]
        }
        
        suggested_activities = []
        for interest in user_interests[:3]:  # Top 3 interests
            if interest in activities_db:
                suggested_activities.extend(random.sample(activities_db[interest], 2))
        
        return suggested_activities
    
    def create_digital_minimalism_challenge(self, level='beginner'):
        """Buat challenge digital minimalism"""
        challenges = {
            'beginner': [
                {'day': 1, 'challenge': 'No social media before noon', 'points': 10},
                {'day': 2, 'challenge': 'Delete one unused app', 'points': 15},
                {'day': 3, 'challenge': '30-minute walk without phone', 'points': 20},
                {'day': 4, 'challenge': 'Read a book for 30 minutes', 'points': 15},
                {'day': 5, 'challenge': 'No phone during meals', 'points': 10},
                {'day': 6, 'challenge': 'Digital sunset after 9 PM', 'points': 20},
                {'day': 7, 'challenge': 'Full day under 3 hours screen time', 'points': 30}
            ],
            'intermediate': [
                {'day': 1, 'challenge': '24-hour social media detox', 'points': 40},
                {'day': 2, 'challenge': 'Enable grayscale mode all day', 'points': 25},
                {'day': 3, 'challenge': 'No streaming services', 'points': 30},
                {'day': 4, 'challenge': 'Outdoor activity 2+ hours', 'points': 35},
                {'day': 5, 'challenge': 'Digital Sabbath (no screens)', 'points': 50},
                {'day': 6, 'challenge': 'Learn a new offline skill', 'points': 30},
                {'day': 7, 'challenge': 'Complete a creative project', 'points': 45}
            ]
        }
        
        return challenges.get(level, challenges['beginner'])
    
    def generate_visualizations(self, usage_patterns, mood_correlation):
        """Generate visualisasi data"""
        visualizations = {}
        
        # Color palette
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        # 1. Daily Screen Time Trend
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(usage_patterns['daily_usage']['date'], 
                usage_patterns['daily_usage']['screen_time_minutes'], 
                marker='o', color=colors[0], linewidth=2)
        ax1.set_title('Daily Screen Time Trend', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Screen Time (minutes)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight', facecolor='#F8F9FA')
        img1.seek(0)
        visualizations['screen_time_trend'] = base64.b64encode(img1.getvalue()).decode()
        plt.close(fig1)
        
        # 2. App Usage Distribution
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        ax2.pie(usage_patterns['app_usage']['usage_minutes'], 
               labels=usage_patterns['app_usage']['app_category'],
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('App Usage by Category', fontsize=14, fontweight='bold')
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight', facecolor='#F8F9FA')
        img2.seek(0)
        visualizations['app_usage_pie'] = base64.b64encode(img2.getvalue()).decode()
        plt.close(fig2)
        
        # 3. Mood vs Screen Time Scatter
        if mood_correlation and 'merged_data' in mood_correlation:
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            scatter = ax3.scatter(mood_correlation['merged_data']['screen_time_minutes'],
                                mood_correlation['merged_data']['mood_score'],
                                c=mood_correlation['merged_data']['mood_score'],
                                cmap='RdYlGn', alpha=0.7, s=100)
            ax3.set_title('Mood Score vs Screen Time', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Screen Time (minutes)')
            ax3.set_ylabel('Mood Score (1-10)')
            ax3.grid(True, alpha=0.3)
            plt.colorbar(scatter)
            
            img3 = io.BytesIO()
            plt.savefig(img3, format='png', bbox_inches='tight', facecolor='#F8F9FA')
            img3.seek(0)
            visualizations['mood_scatter'] = base64.b64encode(img3.getvalue()).decode()
            plt.close(fig3)
        
        return visualizations

# Initialize analyzer
analyzer = DigitalWellnessAnalyzer()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not analyzer.load_data():
        return render_template('error.html', message="Failed to load data")
    
    # Analisis data
    usage_patterns = analyzer.analyze_usage_patterns()
    mood_correlation = analyzer.analyze_mood_correlation()
    interventions = analyzer.generate_interventions(usage_patterns['addiction_metrics'])
    offline_activities = analyzer.suggest_offline_activities()
    challenge = analyzer.create_digital_minimalism_challenge()
    
    # Generate visualizations
    visuals = analyzer.generate_visualizations(usage_patterns, mood_correlation)
    
    # Stats untuk dashboard
    stats = {
        'addiction_score': usage_patterns['addiction_metrics']['overall_score'],
        'addiction_level': usage_patterns['addiction_metrics']['addiction_level'],
        'risk_color': usage_patterns['addiction_metrics']['risk_color'],
        'daily_screen_time': usage_patterns['addiction_metrics']['avg_daily_screen_time'],
        'daily_social_media': usage_patterns['addiction_metrics']['avg_social_media_time'],
        'daily_unlocks': usage_patterns['addiction_metrics']['avg_unlocks'],
        'total_interventions': len(interventions)
    }
    
    # Mood correlation info
    mood_info = {
        'screen_correlation': mood_correlation['screen_mood_correlation'] if mood_correlation else 0,
        'social_correlation': mood_correlation['social_mood_correlation'] if mood_correlation else 0
    }
    
    return render_template('dashboard.html',
                         stats=stats,
                         mood_info=mood_info,
                         interventions=interventions,
                         offline_activities=offline_activities,
                         challenge=challenge,
                         visuals=visuals)

@app.route('/api/usage_data')
def api_usage_data():
    if not analyzer.load_data():
        return jsonify({'error': 'Data loading failed'})
    
    usage_patterns = analyzer.analyze_usage_patterns()
    return jsonify(usage_patterns['daily_usage'].to_dict('records'))

@app.route('/api/add_intervention', methods=['POST'])
def api_add_intervention():
    data = request.get_json()
    # Simpan intervensi baru (dalam real app, save ke database)
    return jsonify({'success': True, 'message': 'Intervention added'})

@app.route('/api/start_challenge', methods=['POST'])
def api_start_challenge():
    data = request.get_json()
    level = data.get('level', 'beginner')
    challenge = analyzer.create_digital_minimalism_challenge(level)
    return jsonify({'challenge': challenge})

if __name__ == '__main__':
    print("Starting Digital Wellness Guardian...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
