%%writefile app.py
import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime
import json
import firebase_admin
from firebase_admin import credentials, firestore
import time

# Page configuration
st.set_page_config(
    page_title="HRD Financial Game 🎮", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with colors, gradients, and beautiful design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Poppins:wght@600;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Noto Sans TC', 'Poppins', sans-serif;
    }
    
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h1 {
        font-size: 2.5rem;
    }
    
    /* Regular text should be dark on light backgrounds, white on dark */
    p, div, span, label {
        color: #2d3748;
    }
    
    .center-text {
        text-align: center;
    }
    
    /* Beautiful buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Investment cards */
    .investment-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        margin: 1rem 0;
        color: white;
    }
    
    .expense-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        margin: 1rem 0;
        color: white;
    }
    
    /* Metric cards with gradients */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        border: none;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 12px;
        border: none;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 12px;
        border: none;
    }
    
    .stError {
        background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
        color: white;
        border-radius: 12px;
        border: none;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Month badge */
    .month-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
    }
    
    /* Asset display */
    .asset-display {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        color: #2d3748 !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        margin: 2rem 0;
    }
    
    /* Status badges */
    .status-submitted {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
        font-weight: 600;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
        font-weight: 600;
    }
    
    /* Emoji decorations */
    .emoji-decor {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Admin dashboard cards */
    .admin-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Leaderboard */
    .leaderboard-gold {
        background: linear-gradient(135deg, #f7b733 0%, #fc4a1a 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    .leaderboard-silver {
        background: linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    .leaderboard-bronze {
        background: linear-gradient(135deg, #ed6ea0 0%, #ec8c69 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ============= FIREBASE CONNECTION =============
@st.cache_resource
def init_firebase():
    """Initialize Firebase"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-key.json')
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"Firebase initialization failed: {e}")
        st.stop()

db = init_firebase()

# ============= DATABASE FUNCTIONS =============

def get_game_state():
    """Get game state from Firebase"""
    try:
        doc = db.collection('game_state').document('current').get()
        if doc.exists:
            return doc.to_dict()
        else:
            default_state = {
                'current_month': 1,
                'exact_cost_daily': 4000,
                'exact_cost_food': 4000,
                'updated_at': datetime.now()
            }
            db.collection('game_state').document('current').set(default_state)
            return default_state
    except Exception as e:
        st.error(f"Error getting game state: {e}")
        return {'current_month': 1, 'exact_cost_daily': 4000, 'exact_cost_food': 4000}

def update_game_state(updates):
    """Update game state"""
    try:
        updates['updated_at'] = datetime.now()
        db.collection('game_state').document('current').update(updates)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error updating game state: {e}")
        return False

@st.cache_data(ttl=5)
def get_all_players_cached():
    """Get all players from Firebase with caching"""
    try:
        players_ref = db.collection('players')
        docs = players_ref.stream()
        
        players = {}
        for doc in docs:
            data = doc.to_dict()
            players[doc.id] = data
        
        return players
    except Exception as e:
        st.error(f"Error getting players: {e}")
        return {}

def get_all_players():
    """Get all players"""
    return get_all_players_cached()

def get_player_data(group_name):
    """Get specific player"""
    try:
        doc = db.collection('players').document(group_name).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        st.error(f"Error getting player: {e}")
        return None

def update_player_data(group_name, data):
    """Update or create player data"""
    try:
        data['updated_at'] = datetime.now()
        db.collection('players').document(group_name).set(data, merge=True)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error updating player: {e}")
        return False

def get_lottery_results(month):
    """Get lottery results"""
    try:
        docs = db.collection('lottery_results').where('month', '==', month).stream()
        results = {}
        for doc in docs:
            data = doc.to_dict()
            results[data['group_name']] = {
                'won': data['won'],
                'prize': data['prize']
            }
        return results
    except Exception as e:
        return {}

def save_lottery_result(group_name, month, won, prize):
    """Save lottery result"""
    try:
        db.collection('lottery_results').add({
            'group_name': group_name,
            'month': month,
            'won': won,
            'prize': prize,
            'timestamp': datetime.now()
        })
        return True
    except Exception as e:
        return False

# ============= SESSION STATE =============

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'group_name' not in st.session_state:
    st.session_state.group_name = ''
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_current_month_name():
    game_state = get_game_state()
    return MONTHS[(game_state['current_month'] - 1) % 12]

# ============= HOME PAGE =============

def home_page():
    st.markdown("<h1 class='center-text' style='font-size: 3.5rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.3);'>HRD Financial Game</h1>", unsafe_allow_html=True)
    st.markdown("<p class='center-text' style='font-size: 1.3rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>Master Your Money, Shape Your Future! 🚀</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div class='emoji-decor'>👨‍💼</div>", unsafe_allow_html=True)
        if st.button("🎯 Administrator Dashboard", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<div class='emoji-decor'>🎓</div>", unsafe_allow_html=True)
        if st.button("🚀 Start Playing (Students)", use_container_width=True):
            st.session_state.page = 'student_login'
            st.rerun()

# ============= ADMIN LOGIN =============

def admin_login_page():
    st.markdown("<div class='emoji-decor'>🔐</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='center-text'>Administrator Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        password = st.text_input("🔑 Enter Admin Password", type="password", key="admin_password")

        if st.button("🚪 Login", use_container_width=True):
            if password == "admin123":
                st.session_state.is_admin = True
                st.session_state.page = 'admin_dashboard'
                st.success("✅ Login successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Incorrect password!")

        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# ============= STUDENT LOGIN =============

def student_login_page():
    st.markdown("<div class='emoji-decor'>🎓👥💼</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='center-text'>Welcome, Future Millionaire!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='center-text' style='color: #667eea;'>Choose Your Team Name</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        group_name = st.text_input("🏆 Your Team Name", key="group_name_input", placeholder="e.g., Money Masters")

        if st.button("🚀 Start Your Journey", use_container_width=True):
            if group_name.strip():
                st.session_state.group_name = group_name.strip()
                st.session_state.is_admin = False
                
                existing_data = get_player_data(group_name)
                if not existing_data:
                    game_state = get_game_state()
                    new_player_data = {
                        'total_asset': 30000,
                        'month': game_state['current_month'],
                        'savings': 30000,
                        'etf': 0,
                        'stock': 0,
                        'startup': 0,
                        'exact_cost_daily': game_state['exact_cost_daily'],
                        'exact_cost_food': game_state['exact_cost_food'],
                        'exact_cost_lottery': 0,
                        'is_broke': False,
                        'submitted': False
                    }
                    update_player_data(group_name, new_player_data)
                
                st.session_state.page = 'student_game'
                st.success(f"✅ Welcome, {group_name}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("⚠️ Please enter a team name!")

        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# ============= STUDENT GAME PAGE =============

def student_game_page():
    group_name = st.session_state.group_name
    player_data = get_player_data(group_name)
    game_state = get_game_state()

    if not player_data:
        st.error("❌ Player data not found. Please login again.")
        return

    if player_data.get('is_broke', False):
        st.markdown("<div class='emoji-decor'>💔😢💸</div>", unsafe_allow_html=True)
        st.markdown("<h1 class='center-text' style='color: #e53e3e;'>Game Over - You're Broke!</h1>", unsafe_allow_html=True)
        st.markdown("<p class='center-text'>Don't give up! Learn from this experience and try again! 💪</p>", unsafe_allow_html=True)
        return

    if player_data.get('submitted', False):
        st.markdown("<div class='emoji-decor'>⏳⌛⏰</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='center-text'>Waiting Room</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='center-text' style='color: #667eea;'>Hello, {group_name}! 👋</h2>", unsafe_allow_html=True)
        
        st.info("✅ Your submission has been received! Waiting for administrator to advance to next month...")

        lottery_results = get_lottery_results(game_state['current_month'])
        if group_name in lottery_results:
            result = lottery_results[group_name]
            if result['won']:
                st.markdown("<div class='emoji-decor'>🎉🎊🏆</div>", unsafe_allow_html=True)
                st.success(f"🎰 JACKPOT! You won the lottery! Prize: ${result['prize']:,.0f}")
                st.balloons()
            else:
                st.info("🎲 Sorry, you didn't win the lottery this time. Better luck next month!")

        if st.button("🔄 Refresh Status", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        return

    # Header
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        if player_data.get('month', 1) == 1:
            st.markdown("<div class='emoji-decor'>🎉💰🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 class='center-text'>Welcome, {group_name}!</h2>", unsafe_allow_html=True)
            st.markdown("<h3 class='center-text' style='color: #48bb78;'>Congratulations! You have $30,000 to invest!</h3>", unsafe_allow_html=True)
            st.markdown("<p class='center-text' style='font-size: 1.2rem;'>Make wise decisions to grow your wealth! 📈</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 class='center-text'>Welcome Back, {group_name}! 👋</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='asset-display'>${player_data['total_asset']:,.0f}</div>", unsafe_allow_html=True)

    with col_header2:
        st.markdown(f"<div class='month-badge'>📅 Month: {get_current_month_name()}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Expense section
    st.markdown("<h2 style='text-align: center;'>💸 Monthly Expenses 💸</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    exact_cost_daily = player_data.get('exact_cost_daily', game_state['exact_cost_daily'])
    exact_cost_food = player_data.get('exact_cost_food', game_state['exact_cost_food'])

    with col1:
        st.markdown("### 💼 Investment")
        st.info("Allocate wisely!")

    with col2:
        st.markdown("### 🏠 Daily Living")
        st.number_input("Amount ($)", value=exact_cost_daily, disabled=True, key="daily_exp")
        daily_percentage = (exact_cost_daily / player_data['total_asset'] * 100) if player_data['total_asset'] > 0 else 0
        st.metric("Percentage", f"{daily_percentage:.1f}%")

    with col3:
        st.markdown("### 🍔 Food")
        st.number_input("Amount ($)", value=exact_cost_food, disabled=True, key="food_exp")
        food_percentage = (exact_cost_food / player_data['total_asset'] * 100) if player_data['total_asset'] > 0 else 0
        st.metric("Percentage", f"{food_percentage:.1f}%")

    with col4:
        st.markdown("### 🎰 Lottery")
        st.caption("🍀 1% chance: 200% | 2% chance: 150%")
        exact_cost_lottery = st.number_input("Amount ($)", min_value=0, max_value=int(player_data['total_asset']), value=0, step=100, key="lottery_exp")
        lottery_percentage = (exact_cost_lottery / player_data['total_asset'] * 100) if player_data['total_asset'] > 0 else 0
        st.metric("Percentage", f"{lottery_percentage:.1f}%")

    total_fixed_expenses = exact_cost_daily + exact_cost_food + exact_cost_lottery
    remaining_for_investment = player_data['total_asset'] - total_fixed_expenses

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #48bb78;'>💰 Available for Investment: ${remaining_for_investment:,.0f} 💰</h2>", unsafe_allow_html=True)

    if remaining_for_investment < 0:
        st.error("⚠️ Your expenses exceed your total assets! Reduce lottery amount!")
        return

    # Investment allocation
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>📊 Allocate Your Investments 📊</h2>", unsafe_allow_html=True)
    
    col_inv1, col_inv2, col_inv3, col_inv4, col_inv5 = st.columns(5)

    with col_inv1:
        st.markdown("### 🏦 Savings")
        st.caption("Safe & Stable")
        savings = st.number_input("Amount ($)", min_value=0, max_value=int(remaining_for_investment), value=int(remaining_for_investment), step=100, key="savings_input")
    
    with col_inv2:
        st.markdown("### 📈 ETF")
        st.caption("Diversified")
        etf = st.number_input("Amount ($)", min_value=0, max_value=int(remaining_for_investment), value=0, step=100, key="etf_input")
    
    with col_inv3:
        st.markdown("### 📊 Stock")
        st.caption("High Return")
        stock = st.number_input("Amount ($)", min_value=0, max_value=int(remaining_for_investment), value=0, step=100, key="stock_input")
    
    with col_inv4:
        st.markdown("### 🚀 Startup")
        st.caption("High Risk")
        startup = st.number_input("Amount ($)", min_value=0, max_value=int(remaining_for_investment), value=0, step=100, key="startup_input")
    
    with col_inv5:
        total_allocated = savings + etf + stock + startup
        allocation_percentage = (total_allocated / remaining_for_investment * 100) if remaining_for_investment > 0 else 0
        st.metric("Total", f"{allocation_percentage:.1f}%")
        
        if total_allocated != remaining_for_investment:
            st.warning(f"⚠️ Must allocate ${remaining_for_investment:,.0f}")

    st.markdown(f"<h3 style='text-align: center;'>🏦 Your Safety Net: ${savings:,.0f}</h3>", unsafe_allow_html=True)

    if savings < 1:
        player_data['is_broke'] = True
        update_player_data(group_name, player_data)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if total_allocated == remaining_for_investment:
        if st.button("📤 Submit Your Allocation", use_container_width=True, type="primary"):
            st.session_state.show_confirm = True

        if st.session_state.get('show_confirm', False):
            st.warning("⚠️ Once submitted, you cannot change! Are you sure?")
            if st.button("✅ Yes, I'm Sure!", use_container_width=True):
                player_data.update({
                    'savings': savings,
                    'etf': etf,
                    'stock': stock,
                    'startup': startup,
                    'exact_cost_lottery': exact_cost_lottery,
                    'submitted': True
                })
                update_player_data(group_name, player_data)
                st.session_state.show_confirm = False
                st.success("🎉 Submission successful!")
                st.balloons()
                time.sleep(1)
                st.rerun()
    else:
        st.error("❌ Please allocate all funds before submitting!")

# ============= ADMIN DASHBOARD =============

def admin_dashboard_page():
    game_state = get_game_state()
    all_players = get_all_players()

    st.markdown("<div class='emoji-decor'>👨‍💼📊💼</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='center-text' style='color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);'>Game Administrator Dashboard</h1>", unsafe_allow_html=True)

    # Control buttons
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)

    with col_btn1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    with col_btn2:
        if st.button("🎲 Event Cards", use_container_width=True):
            st.session_state.page = 'admin_events'
            st.rerun()

    with col_btn3:
        if st.button("➡️ Next Month +$10K", use_container_width=True):
            advance_month()
            st.cache_data.clear()
            st.success("✅ Advanced to next month!")
            time.sleep(0.5)
            st.rerun()

    with col_btn4:
        if st.button("📊 Statistics", use_container_width=True):
            st.session_state.page = 'statistics'
            st.rerun()

    with col_btn5:
        if st.button("🏆 End Game", use_container_width=True):
            st.session_state.page = 'end_game'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Month control and delete players section
    col_control1, col_control2 = st.columns(2)

    with col_control1:
        st.markdown("### ⏮️ Go Back to Month")
        target_month = st.number_input(
            "Jump to month:",
            min_value=1,
            max_value=game_state['current_month'],
            value=game_state['current_month'],
            step=1,
            key="target_month"
        )
        if st.button("⏮️ Jump to Month", use_container_width=True):
            if target_month < game_state['current_month']:
                update_game_state({'current_month': target_month})
                st.success(f"✅ Jumped back to Month {target_month}!")
                st.cache_data.clear()
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Can only go back to previous months!")

    with col_control2:
        st.markdown("### 🗑️ Delete Player")
        if all_players:
            player_to_delete = st.selectbox(
                "Select player to remove:",
                options=["-- Select Player --"] + list(all_players.keys()),
                key="delete_player_select"
            )
            if player_to_delete != "-- Select Player --":
                if st.button(f"🗑️ Delete {player_to_delete}", use_container_width=True, type="primary"):
                    try:
                        db.collection('players').document(player_to_delete).delete()
                        st.success(f"✅ Deleted {player_to_delete}!")
                        st.cache_data.clear()
                        time.sleep(0.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting player: {e}")
        else:
            st.info("No players to delete")

    st.markdown("<br>", unsafe_allow_html=True)

    # Download button - convert datetime objects to strings
    def convert_to_json_serializable(obj):
        """Convert Firebase datetime objects to strings"""
        if isinstance(obj, dict):
            return {k: convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_json_serializable(item) for item in obj]
        elif hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        else:
            return obj
    
    download_state = {
        'players_data': convert_to_json_serializable(all_players),
        'current_month': game_state['current_month'],
        'exact_cost_daily': game_state['exact_cost_daily'],
        'exact_cost_food': game_state['exact_cost_food']
    }
    st.download_button(
        "💾 Download Game State",
        data=json.dumps(download_state, ensure_ascii=False, indent=2),
        file_name=f"game_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown(f"<div class='month-badge' style='font-size: 1.5rem;'>📅 Current Month: {get_current_month_name()}</div>", unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"<div class='month-badge' style='font-size: 1.5rem; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>👥 Total Players: {len(all_players)}</div>", unsafe_allow_html=True)

    if not all_players:
        st.info("📢 No players have joined yet. Share the game link with students!")
        return

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>📊 Player Overview 📊</h2>", unsafe_allow_html=True)

    # Display players in grid
    players_list = list(all_players.items())
    cols_per_row = 3

    for i in range(0, len(players_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(players_list):
                group_name, data = players_list[idx]
                with cols[j]:
                    display_player_card(group_name, data)

def display_player_card(group_name, data):
    """Display beautiful player card with pie chart"""
    
    # Status badge
    status = "✅ Submitted" if data.get('submitted', False) else "⏳ Pending"
    status_class = "status-submitted" if data.get('submitted', False) else "status-pending"
    
    st.markdown(f"<div class='admin-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>👤 {group_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='{status_class}'>{status}</div>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: #48bb78;'>💰 ${data['total_asset']:,.0f}</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Pie chart
    values = [data['savings'], data['etf'], data['stock'], data['startup']]
    labels = ['🏦 Savings', '📈 ETF', '📊 Stock', '🚀 Startup']
    colors = ['#667eea', '#48bb78', '#f093fb', '#f5576c']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=12)
    )])

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, key=f"pie_{group_name}")

    with st.expander("📊 View Full Details"):
        st.write(f"**Savings:** ${data['savings']:,}")
        st.write(f"**ETF:** ${data['etf']:,}")
        st.write(f"**Stock:** ${data['stock']:,}")
        st.write(f"**Startup:** ${data['startup']:,}")
        st.write(f"**Broke:** {'💀 Yes' if data.get('is_broke', False) else '✅ No'}")

def advance_month():
    """Advance to next month"""
    game_state = get_game_state()
    all_players = get_all_players()
    new_month = game_state['current_month'] + 1
    
    for group_name, data in all_players.items():
        if not data.get('is_broke', False):
            # Initialize history if not exists
            if 'history' not in data:
                data['history'] = {
                    'months': [],
                    'total_assets': [],
                    'savings': [],
                    'etf': [],
                    'stock': [],
                    'startup': []
                }
            
            # Record current state before advancing
            data['history']['months'].append(game_state['current_month'])
            data['history']['total_assets'].append(data['total_asset'])
            data['history']['savings'].append(data.get('savings', 0))
            data['history']['etf'].append(data.get('etf', 0))
            data['history']['stock'].append(data.get('stock', 0))
            data['history']['startup'].append(data.get('startup', 0))
            
            # Add monthly income
            data['total_asset'] += 10000
            data['month'] = new_month
            
            # Process lottery
            lottery_amount = data.get('exact_cost_lottery', 0)
            if lottery_amount > 0:
                rand = random.random()
                won = False
                prize = 0
                if rand < 0.01:
                    won = True
                    prize = lottery_amount * 2
                    data['total_asset'] += prize
                elif rand < 0.03:
                    won = True
                    prize = lottery_amount * 1.5
                    data['total_asset'] += prize
                save_lottery_result(group_name, new_month, won, prize)
            
            data['exact_cost_daily'] = game_state['exact_cost_daily']
            data['exact_cost_food'] = game_state['exact_cost_food']
            data['submitted'] = False
            update_player_data(group_name, data)
    
    update_game_state({'current_month': new_month})

# ============= ADMIN EVENTS PAGE =============

def admin_events_page():
    game_state = get_game_state()
    all_players = get_all_players()

    st.markdown("<h1 class='center-text' style='color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);'>Event Cards - Play God!</h1>", unsafe_allow_html=True)

    if st.button("← Back to Dashboard", use_container_width=False):
        st.session_state.page = 'admin_dashboard'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    event_choice = st.selectbox(
        "🎴 Select Event Card",
        ["-- Select an Event --", "Card I: Tariff War", "Card II: NVIDIA Revolution"]
    )

    if event_choice == "Card I: Tariff War":
        st.markdown("### 🌍 Card I: Tariff War")
        st.markdown("**Description:** Trump initiates global tariff war!")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎲 Reveal Result", key="reveal_tariff", use_container_width=True):
                st.session_state.tariff_revealed = True
                st.rerun()
        
        if st.session_state.get('tariff_revealed', False):
            st.warning("**Result:** Food cost increases by 10%")
            
            with col2:
                if st.button("✅ Apply Effect", type="primary", key="apply_tariff", use_container_width=True):
                    new_food_cost = int(game_state['exact_cost_food'] * 1.1)
                    update_game_state({'exact_cost_food': new_food_cost})

                    for group_name, data in all_players.items():
                        data['exact_cost_food'] = new_food_cost
                        update_player_data(group_name, data)

                    st.success(f"🎯 Food cost increased to ${new_food_cost}!")
                    st.balloons()
                    st.session_state.tariff_revealed = False
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()

    elif event_choice == "Card II: NVIDIA Revolution":
        st.markdown("### 🚀 Card II: NVIDIA Revolution")
        st.markdown("**Description:** AI breakthrough boosts tech stocks!")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎲 Reveal Result", key="reveal_nvidia", use_container_width=True):
                st.session_state.nvidia_revealed = True
                st.rerun()
        
        if st.session_state.get('nvidia_revealed', False):
            st.success("**Result:** All stocks increase 20%!")
            
            with col2:
                if st.button("✅ Apply Effect", type="primary", key="apply_nvidia", use_container_width=True):
                    for group_name, data in all_players.items():
                        if data.get('stock', 0) > 0:
                            profit = data['stock'] * 0.2
                            data['stock'] = data['stock'] + profit
                            data['total_asset'] = data['total_asset'] + profit
                            update_player_data(group_name, data)

                    st.success("📈 All stock investments increased by 20%!")
                    st.balloons()
                    st.session_state.nvidia_revealed = False
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()

# ============= STATISTICS PAGE =============

def statistics_page():
    import numpy as np
    from scipy import stats as scipy_stats
    
    st.markdown("<h1 class='center-text' style='color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);'>Statistical Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard", use_container_width=False):
        st.session_state.page = 'admin_dashboard'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    all_players = get_all_players()
    game_state = get_game_state()
    
    if not all_players:
        st.warning("No player data available yet!")
        return
    
    # Prepare data
    player_names = list(all_players.keys())
    total_assets = [data['total_asset'] for data in all_players.values()]
    savings_list = [data.get('savings', 0) for data in all_players.values()]
    etf_list = [data.get('etf', 0) for data in all_players.values()]
    stock_list = [data.get('stock', 0) for data in all_players.values()]
    startup_list = [data.get('startup', 0) for data in all_players.values()]
    
    # Analysis selection
    analysis_type = st.selectbox(
        "📊 Select Analysis Type",
        [
            "Overview Statistics",
            "Historical Trends",
            "Asset Distribution",
            "Investment Allocation Patterns",
            "Risk vs Return Analysis",
            "Correlation Analysis",
            "Player Comparison",
            "Portfolio Diversity Score",
            "Monte Carlo Simulation"
        ]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== OVERVIEW STATISTICS ==========
    if analysis_type == "Overview Statistics":
        st.markdown("### 📈 Descriptive Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Players", len(all_players))
            st.metric("Average Assets", f"${np.mean(total_assets):,.0f}")
        
        with col2:
            st.metric("Median Assets", f"${np.median(total_assets):,.0f}")
            st.metric("Std Deviation", f"${np.std(total_assets):,.0f}")
        
        with col3:
            st.metric("Max Assets", f"${np.max(total_assets):,.0f}")
            st.metric("Min Assets", f"${np.min(total_assets):,.0f}")
        
        with col4:
            st.metric("Total Wealth", f"${np.sum(total_assets):,.0f}")
            st.metric("Wealth Range", f"${np.max(total_assets) - np.min(total_assets):,.0f}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary table
        st.markdown("### 📋 Detailed Summary")
        summary_data = {
            'Player': player_names,
            'Total Assets': [f"${x:,.0f}" for x in total_assets],
            'Savings': [f"${x:,.0f}" for x in savings_list],
            'ETF': [f"${x:,.0f}" for x in etf_list],
            'Stock': [f"${x:,.0f}" for x in stock_list],
            'Startup': [f"${x:,.0f}" for x in startup_list]
        }
        st.table(summary_data)
    
    # ========== HISTORICAL TRENDS ==========
    elif analysis_type == "Historical Trends":
        st.markdown("### 📈 Historical Trends Over Time")
        
        # Check if any player has history
        has_history = any('history' in data and len(data['history'].get('months', [])) > 0 
                         for data in all_players.values())
        
        if not has_history:
            st.warning("⏳ No historical data yet! Historical data is recorded when you advance to the next month.")
            st.info("💡 Tip: After advancing to Month 2 or later, you'll see trend lines showing how each player's assets change over time.")
            return
        
        # Select what to visualize
        metric_choice = st.radio(
            "Select metric to track:",
            ["Total Assets", "Individual Investments", "All Players Comparison"]
        )
        
        if metric_choice == "Total Assets":
            st.markdown("#### 💰 Total Assets Over Time")
            
            fig = go.Figure()
            
            for player_name, data in all_players.items():
                if 'history' in data and len(data['history'].get('months', [])) > 0:
                    history = data['history']
                    # Add current month's data
                    months = history['months'] + [game_state['current_month']]
                    assets = history['total_assets'] + [data['total_asset']]
                    
                    fig.add_trace(go.Scatter(
                        x=months,
                        y=assets,
                        mode='lines+markers',
                        name=player_name,
                        line=dict(width=3),
                        marker=dict(size=8)
                    ))
            
            fig.update_layout(
                title="Asset Growth Over Time",
                xaxis_title="Month",
                yaxis_title="Total Assets ($)",
                height=500,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth rate analysis
            st.markdown("#### 📊 Growth Rate Analysis")
            col1, col2 = st.columns(2)
            
            growth_rates = {}
            for player_name, data in all_players.items():
                if 'history' in data and len(data['history'].get('total_assets', [])) > 0:
                    initial = data['history']['total_assets'][0]
                    current = data['total_asset']
                    months = len(data['history']['months'])
                    if initial > 0 and months > 0:
                        growth_rate = ((current - initial) / initial) * 100 / months
                        growth_rates[player_name] = growth_rate
            
            if growth_rates:
                sorted_growth = sorted(growth_rates.items(), key=lambda x: x[1], reverse=True)
                
                with col1:
                    st.markdown("**🚀 Fastest Growing:**")
                    for i, (player, rate) in enumerate(sorted_growth[:3], 1):
                        st.write(f"{i}. {player}: +{rate:.1f}% per month")
                
                with col2:
                    st.markdown("**🐌 Slowest Growing:**")
                    for i, (player, rate) in enumerate(sorted_growth[-3:], 1):
                        st.write(f"{i}. {player}: {rate:+.1f}% per month")
        
        elif metric_choice == "Individual Investments":
            st.markdown("#### 🎯 Investment Breakdown Over Time")
            
            selected_player = st.selectbox("Select player:", player_names)
            
            if selected_player:
                data = all_players[selected_player]
                
                if 'history' not in data or len(data['history'].get('months', [])) == 0:
                    st.warning(f"{selected_player} has no historical data yet.")
                else:
                    history = data['history']
                    months = history['months'] + [game_state['current_month']]
                    
                    fig = go.Figure()
                    
                    # Add traces for each investment type
                    investments = {
                        'Savings': (history['savings'] + [data.get('savings', 0)], '#667eea'),
                        'ETF': (history['etf'] + [data.get('etf', 0)], '#48bb78'),
                        'Stock': (history['stock'] + [data.get('stock', 0)], '#f093fb'),
                        'Startup': (history['startup'] + [data.get('startup', 0)], '#f5576c')
                    }
                    
                    for name, (values, color) in investments.items():
                        fig.add_trace(go.Scatter(
                            x=months,
                            y=values,
                            mode='lines+markers',
                            name=name,
                            line=dict(width=2, color=color),
                            marker=dict(size=6),
                            stackgroup='one'
                        ))
                    
                    fig.update_layout(
                        title=f"{selected_player}'s Investment Allocation Over Time",
                        xaxis_title="Month",
                        yaxis_title="Amount ($)",
                        height=500,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Strategy consistency
                    st.markdown("#### 🎯 Strategy Consistency")
                    if len(history['months']) >= 2:
                        # Calculate variance in allocation percentages
                        total_assets_history = history['total_assets']
                        savings_pct = [history['savings'][i] / total_assets_history[i] * 100 
                                      if total_assets_history[i] > 0 else 0 
                                      for i in range(len(history['savings']))]
                        
                        variance = np.var(savings_pct) if len(savings_pct) > 1 else 0
                        
                        if variance < 10:
                            st.success("✅ Very consistent strategy (low variance)")
                        elif variance < 50:
                            st.info("ℹ️ Moderately consistent strategy")
                        else:
                            st.warning("⚠️ Highly variable strategy (experimenting)")
        
        elif metric_choice == "All Players Comparison":
            st.markdown("#### 👥 All Players Asset Comparison")
            
            fig = go.Figure()
            
            colors = ['#667eea', '#48bb78', '#f093fb', '#f5576c', '#4facfe', '#feca57', '#ee5a6f', '#c44569']
            
            for idx, (player_name, data) in enumerate(all_players.items()):
                if 'history' in data and len(data['history'].get('months', [])) > 0:
                    history = data['history']
                    months = history['months'] + [game_state['current_month']]
                    assets = history['total_assets'] + [data['total_asset']]
                    
                    fig.add_trace(go.Scatter(
                        x=months,
                        y=assets,
                        mode='lines+markers',
                        name=player_name,
                        line=dict(width=2, color=colors[idx % len(colors)]),
                        marker=dict(size=6)
                    ))
            
            fig.update_layout(
                title="All Players - Asset Growth Comparison",
                xaxis_title="Month",
                yaxis_title="Total Assets ($)",
                height=600,
                hovermode='x unified',
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.05
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Leader board over time
            st.markdown("#### 🏆 Leader Changes Over Time")
            st.info("See who was leading at each month of the game!")
    
    # ========== ASSET DISTRIBUTION ==========
    elif analysis_type == "Asset Distribution":
        st.markdown("### 📊 Asset Distribution Analysis")
        
        chart_type = st.radio("Select Chart Type:", ["Histogram", "Box Plot", "Violin Plot"])
        
        if chart_type == "Histogram":
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=total_assets,
                nbinsx=10,
                marker_color='#667eea',
                name='Asset Distribution'
            ))
            fig.update_layout(
                title="Distribution of Total Assets",
                xaxis_title="Total Assets ($)",
                yaxis_title="Number of Players",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Box Plot":
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=total_assets,
                name='Total Assets',
                marker_color='#667eea',
                boxmean='sd'
            ))
            fig.update_layout(
                title="Asset Distribution (Box Plot)",
                yaxis_title="Total Assets ($)",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Violin Plot":
            fig = go.Figure()
            fig.add_trace(go.Violin(
                y=total_assets,
                name='Assets',
                box_visible=True,
                marker_color='#667eea'
            ))
            fig.update_layout(
                title="Asset Distribution (Violin Plot)",
                yaxis_title="Total Assets ($)",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== INVESTMENT ALLOCATION ==========
    elif analysis_type == "Investment Allocation Patterns":
        st.markdown("### 🎯 Investment Allocation Analysis")
        
        # Average allocation
        avg_savings = np.mean(savings_list)
        avg_etf = np.mean(etf_list)
        avg_stock = np.mean(stock_list)
        avg_startup = np.mean(startup_list)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Average Allocation (Amount)")
            fig = go.Figure(data=[go.Pie(
                labels=['Savings', 'ETF', 'Stock', 'Startup'],
                values=[avg_savings, avg_etf, avg_stock, avg_startup],
                hole=0.4,
                marker=dict(colors=['#667eea', '#48bb78', '#f093fb', '#f5576c'])
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Allocation Comparison")
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Savings', x=player_names, y=savings_list, marker_color='#667eea'))
            fig.add_trace(go.Bar(name='ETF', x=player_names, y=etf_list, marker_color='#48bb78'))
            fig.add_trace(go.Bar(name='Stock', x=player_names, y=stock_list, marker_color='#f093fb'))
            fig.add_trace(go.Bar(name='Startup', x=player_names, y=startup_list, marker_color='#f5576c'))
            fig.update_layout(barmode='stack', height=400, xaxis_title="Player", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== RISK VS RETURN ==========
    elif analysis_type == "Risk vs Return Analysis":
        st.markdown("### ⚖️ Risk vs Return Analysis")
        
        # Calculate risk score (higher investment in risky assets = higher risk)
        risk_scores = []
        for data in all_players.values():
            total = data['total_asset']
            if total > 0:
                risk = (data.get('stock', 0) * 0.5 + data.get('startup', 0) * 1.0) / total * 100
            else:
                risk = 0
            risk_scores.append(risk)
        
        # Scatter plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=risk_scores,
            y=total_assets,
            mode='markers+text',
            text=player_names,
            textposition='top center',
            marker=dict(
                size=15,
                color=total_assets,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Assets ($)")
            )
        ))
        fig.update_layout(
            title="Risk vs Total Assets",
            xaxis_title="Risk Score (%)",
            yaxis_title="Total Assets ($)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk categories
        st.markdown("### 📊 Risk Profile Distribution")
        conservative = sum(1 for r in risk_scores if r < 20)
        moderate = sum(1 for r in risk_scores if 20 <= r < 50)
        aggressive = sum(1 for r in risk_scores if r >= 50)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Conservative (<20%)", conservative)
        with col2:
            st.metric("Moderate (20-50%)", moderate)
        with col3:
            st.metric("Aggressive (≥50%)", aggressive)
    
    # ========== CORRELATION ANALYSIS ==========
    elif analysis_type == "Correlation Analysis":
        st.markdown("### 🔗 Correlation Between Investment Choices")
        
        # Create correlation matrix
        data_matrix = np.array([savings_list, etf_list, stock_list, startup_list, total_assets])
        correlation_matrix = np.corrcoef(data_matrix)
        
        labels = ['Savings', 'ETF', 'Stock', 'Startup', 'Total Assets']
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=labels,
            y=labels,
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlation_matrix, 2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlation")
        ))
        fig.update_layout(
            title="Correlation Matrix",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📊 Key Insights")
        
        # Find strongest correlations
        st.write("**Strongest Positive Correlations:**")
        for i in range(len(labels)):
            for j in range(i+1, len(labels)):
                corr = correlation_matrix[i][j]
                if corr > 0.5:
                    st.write(f"- {labels[i]} ↔ {labels[j]}: {corr:.2f}")
        
        st.write("**Strongest Negative Correlations:**")
        for i in range(len(labels)):
            for j in range(i+1, len(labels)):
                corr = correlation_matrix[i][j]
                if corr < -0.5:
                    st.write(f"- {labels[i]} ↔ {labels[j]}: {corr:.2f}")
    
    # ========== PLAYER COMPARISON ==========
    elif analysis_type == "Player Comparison":
        st.markdown("### 👥 Player Comparison")
        
        selected_players = st.multiselect(
            "Select players to compare:",
            options=player_names,
            default=player_names[:min(3, len(player_names))]
        )
        
        if selected_players:
            comparison_data = {
                'Metric': ['Total Assets', 'Savings', 'ETF', 'Stock', 'Startup']
            }
            
            for player in selected_players:
                data = all_players[player]
                comparison_data[player] = [
                    f"${data['total_asset']:,.0f}",
                    f"${data.get('savings', 0):,.0f}",
                    f"${data.get('etf', 0):,.0f}",
                    f"${data.get('stock', 0):,.0f}",
                    f"${data.get('startup', 0):,.0f}"
                ]
            
            st.table(comparison_data)
            
            # Radar chart
            st.markdown("#### Portfolio Comparison (Radar Chart)")
            fig = go.Figure()
            
            categories = ['Savings', 'ETF', 'Stock', 'Startup']
            
            for player in selected_players:
                data = all_players[player]
                values = [
                    data.get('savings', 0),
                    data.get('etf', 0),
                    data.get('stock', 0),
                    data.get('startup', 0)
                ]
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=player
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== PORTFOLIO DIVERSITY ==========
    elif analysis_type == "Portfolio Diversity Score":
        st.markdown("### 🌈 Portfolio Diversity Analysis")
        
        st.info("Diversity Score: Measures how well-balanced the portfolio is across different assets. Higher score = more diversified.")
        
        # Calculate diversity scores (Shannon entropy)
        diversity_scores = []
        for data in all_players.values():
            allocations = [
                data.get('savings', 0),
                data.get('etf', 0),
                data.get('stock', 0),
                data.get('startup', 0)
            ]
            total = sum(allocations)
            if total > 0:
                proportions = [a/total for a in allocations if a > 0]
                entropy = -sum(p * np.log(p) for p in proportions)
                # Normalize to 0-100 scale
                max_entropy = np.log(4)  # Maximum possible entropy with 4 categories
                diversity_score = (entropy / max_entropy) * 100
            else:
                diversity_score = 0
            diversity_scores.append(diversity_score)
        
        # Create bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=player_names,
            y=diversity_scores,
            marker_color=diversity_scores,
            marker=dict(
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Score")
            ),
            text=[f"{s:.1f}" for s in diversity_scores],
            textposition='outside'
        ))
        fig.update_layout(
            title="Portfolio Diversity Scores",
            xaxis_title="Player",
            yaxis_title="Diversity Score (0-100)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Rankings
        st.markdown("### 🏆 Diversity Rankings")
        diversity_ranking = sorted(zip(player_names, diversity_scores), key=lambda x: x[1], reverse=True)
        
        for i, (player, score) in enumerate(diversity_ranking, 1):
            if i == 1:
                st.success(f"🥇 {i}. {player} - {score:.1f} (Most Diversified)")
            elif i == 2:
                st.info(f"🥈 {i}. {player} - {score:.1f}")
            elif i == 3:
                st.warning(f"🥉 {i}. {player} - {score:.1f}")
            else:
                st.write(f"  {i}. {player} - {score:.1f}")
    
    # ========== MONTE CARLO SIMULATION ==========
    elif analysis_type == "Monte Carlo Simulation":
        st.markdown("### 🎲 Monte Carlo Simulation")
        
        st.info("""
        **What is Monte Carlo Simulation?**
        
        Monte Carlo simulation runs your game strategy thousands of times with random variations to predict likely outcomes.
        
        **How it works:**
        1. Takes your current investment allocation
        2. Simulates random market events (good and bad)
        3. Runs 1,000+ scenarios
        4. Shows you the range of possible outcomes
        
        **Why it's useful:**
        - See probability of reaching your goals
        - Understand risk in your strategy
        - Compare "safe" vs "risky" approaches
        - Learn about uncertainty in investing
        """)
        
        st.markdown("---")
        
        # Select player to simulate
        selected_player = st.selectbox("Select player to simulate:", player_names, key="mc_player")
        
        if selected_player:
            player_data = all_players[selected_player]
            
            col1, col2 = st.columns(2)
            
            with col1:
                num_simulations = st.slider("Number of simulations:", 100, 10000, 1000, 100)
                months_ahead = st.slider("Months to simulate:", 1, 12, 6)
            
            with col2:
                st.markdown("**Current Portfolio:**")
                st.write(f"💰 Total: ${player_data['total_asset']:,.0f}")
                st.write(f"🏦 Savings: ${player_data.get('savings', 0):,.0f}")
                st.write(f"📈 ETF: ${player_data.get('etf', 0):,.0f}")
                st.write(f"📊 Stock: ${player_data.get('stock', 0):,.0f}")
                st.write(f"🚀 Startup: ${player_data.get('startup', 0):,.0f}")
            
            if st.button("🎲 Run Simulation", type="primary", use_container_width=True):
                
                with st.spinner(f"Running {num_simulations} simulations..."):
                    
                    # Run simulations
                    results = []
                    
                    for _ in range(num_simulations):
                        # Start with current assets
                        total = player_data['total_asset']
                        savings = player_data.get('savings', 0)
                        etf = player_data.get('etf', 0)
                        stock = player_data.get('stock', 0)
                        startup = player_data.get('startup', 0)
                        
                        # Simulate each month
                        for month in range(months_ahead):
                            # Add monthly income
                            total += 10000
                            
                            # Simulate returns (random but realistic)
                            # Savings: 0-0.5% per month (very safe)
                            savings *= (1 + np.random.uniform(0, 0.005))
                            
                            # ETF: -2% to +4% per month (moderate)
                            etf *= (1 + np.random.uniform(-0.02, 0.04))
                            
                            # Stock: -10% to +15% per month (volatile)
                            stock *= (1 + np.random.uniform(-0.10, 0.15))
                            
                            # Startup: -20% to +30% per month (very volatile)
                            # 5% chance of total loss
                            if np.random.random() < 0.05:
                                startup = 0
                            else:
                                startup *= (1 + np.random.uniform(-0.20, 0.30))
                            
                            # Recalculate total
                            total = savings + etf + stock + startup
                            
                            # Subtract expenses (simplified)
                            total -= game_state['exact_cost_daily']
                            total -= game_state['exact_cost_food']
                        
                        results.append(total)
                    
                    results = np.array(results)
                    
                    # Display results
                    st.success(f"✅ Completed {num_simulations} simulations!")
                    
                    st.markdown("---")
                    st.markdown("### 📊 Simulation Results")
                    
                    # Key statistics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Average Outcome", f"${np.mean(results):,.0f}")
                        st.metric("Current Assets", f"${player_data['total_asset']:,.0f}")
                    
                    with col2:
                        st.metric("Best Case (95th %)", f"${np.percentile(results, 95):,.0f}")
                        st.metric("Median Outcome", f"${np.median(results):,.0f}")
                    
                    with col3:
                        st.metric("Worst Case (5th %)", f"${np.percentile(results, 5):,.0f}")
                        st.metric("Std Deviation", f"${np.std(results):,.0f}")
                    
                    with col4:
                        prob_profit = np.sum(results > player_data['total_asset']) / num_simulations * 100
                        prob_loss = 100 - prob_profit
                        st.metric("Chance of Gain", f"{prob_profit:.1f}%")
                        st.metric("Chance of Loss", f"{prob_loss:.1f}%")
                    
                    # Histogram
                    st.markdown("#### 📈 Distribution of Outcomes")
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Histogram(
                        x=results,
                        nbinsx=50,
                        marker_color='#667eea',
                        name='Outcomes'
                    ))
                    
                    # Add vertical lines for key values
                    fig.add_vline(x=player_data['total_asset'], 
                                 line_dash="dash", 
                                 line_color="red",
                                 annotation_text="Current")
                    fig.add_vline(x=np.mean(results), 
                                 line_dash="dash", 
                                 line_color="green",
                                 annotation_text="Average")
                    
                    fig.update_layout(
                        title=f"Distribution of Assets After {months_ahead} Months",
                        xaxis_title="Final Assets ($)",
                        yaxis_title="Frequency",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Percentile analysis
                    st.markdown("#### 📊 Percentile Analysis")
                    st.write("**What are the chances of different outcomes?**")
                    
                    percentiles = [10, 25, 50, 75, 90]
                    percentile_values = [np.percentile(results, p) for p in percentiles]
                    
                    percentile_data = {
                        'Percentile': [f"{p}th" for p in percentiles],
                        'Meaning': [
                            "Worst 10% of outcomes",
                            "Lower quarter outcomes",
                            "Middle outcome (50/50)",
                            "Upper quarter outcomes",
                            "Best 10% of outcomes"
                        ],
                        'Asset Value': [f"${v:,.0f}" for v in percentile_values]
                    }
                    
                    st.table(percentile_data)
                    
                    # Risk assessment
                    st.markdown("#### ⚠️ Risk Assessment")
                    
                    risk_of_loss = np.sum(results < player_data['total_asset'] * 0.8) / num_simulations * 100
                    chance_of_double = np.sum(results > player_data['total_asset'] * 2) / num_simulations * 100
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if risk_of_loss < 10:
                            st.success(f"✅ Low risk: Only {risk_of_loss:.1f}% chance of losing 20%+ of assets")
                        elif risk_of_loss < 30:
                            st.warning(f"⚠️ Moderate risk: {risk_of_loss:.1f}% chance of losing 20%+ of assets")
                        else:
                            st.error(f"❌ High risk: {risk_of_loss:.1f}% chance of losing 20%+ of assets")
                    
                    with col2:
                        if chance_of_double > 30:
                            st.success(f"🚀 High growth potential: {chance_of_double:.1f}% chance of doubling assets")
                        elif chance_of_double > 10:
                            st.info(f"📈 Moderate growth: {chance_of_double:.1f}% chance of doubling assets")
                        else:
                            st.warning(f"🐌 Conservative: Only {chance_of_double:.1f}% chance of doubling assets")
                    
                    # Strategy recommendation
                    st.markdown("#### 💡 Strategy Insights")
                    
                    # Calculate risk score
                    total_invested = player_data['total_asset']
                    if total_invested > 0:
                        risky_pct = (player_data.get('stock', 0) + player_data.get('startup', 0)) / total_invested
                        
                        if risky_pct < 0.2:
                            st.info("🛡️ **Conservative Strategy**: Your portfolio is very safe but growth may be limited.")
                        elif risky_pct < 0.5:
                            st.success("✅ **Balanced Strategy**: Good mix of safety and growth potential!")
                        else:
                            st.warning("🎲 **Aggressive Strategy**: High risk, high reward! Consider diversifying.")

# ============= END GAME PAGE =============

def end_game_page():
    all_players = get_all_players()

    st.markdown("<div class='emoji-decor'>🏆🎉👑</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='center-text'>Final Rankings - Game Over!</h1>", unsafe_allow_html=True)

    rankings = sorted(
        [(name, data['total_asset']) for name, data in all_players.items() if not data.get('is_broke', False)],
        key=lambda x: x[1],
        reverse=True
    )

    if len(rankings) >= 3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h2 class='center-text'>🥈 2nd Place</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='leaderboard-silver'><h3>{rankings[1][0]}</h3><h4>${rankings[1][1]:,.0f}</h4></div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<h1 class='center-text'>🥇 WINNER!</h1>", unsafe_allow_html=True)
            st.markdown(f"<div class='leaderboard-gold'><h2>{rankings[0][0]}</h2><h3>${rankings[0][1]:,.0f}</h3></div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<h2 class='center-text'>🥉 3rd Place</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='leaderboard-bronze'><h3>{rankings[2][0]}</h3><h4>${rankings[2][1]:,.0f}</h4></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📊 Complete Rankings")

    for i, (name, asset) in enumerate(rankings, 1):
        if i == 1:
            st.success(f"🥇 {i}. {name} - ${asset:,.0f}")
        elif i == 2:
            st.info(f"🥈 {i}. {name} - ${asset:,.0f}")
        elif i == 3:
            st.warning(f"🥉 {i}. {name} - ${asset:,.0f}")
        else:
            st.write(f"  {i}. {name} - ${asset:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Back to Dashboard"):
        st.session_state.page = 'admin_dashboard'
        st.rerun()

# ============= MAIN ROUTER =============

def main():
    page = st.session_state.page

    if page == 'home':
        home_page()
    elif page == 'admin_login':
        admin_login_page()
    elif page == 'student_login':
        student_login_page()
    elif page == 'student_game':
        student_game_page()
    elif page == 'admin_dashboard':
        admin_dashboard_page()
    elif page == 'admin_events':
        admin_events_page()
    elif page == 'statistics':
        statistics_page()
    elif page == 'end_game':
        end_game_page()

if __name__ == "__main__":
    main()
