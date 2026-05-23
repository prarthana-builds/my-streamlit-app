import streamlit as st
import cv2
import time

# 1. Page Configuration & Custom Theme (Dark Mode)
st.set_page_config(
    page_title="AI-Based Waste Segregation Bin",
    page_icon="♻️",
    layout="wide"
)

# Custom CSS to mimic the sleek, rounded card UI from the screenshots
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #121416;
        color: #E2E8F0;
    }
    /* Custom Card Style */
    .status-card {
        background-color: #1A1D20;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #2D3136;
    }
    /* Status Badge Text Styles */
    .status-ok { color: #4ADE80; font-weight: bold; }
    .status-error { color: #F87171; font-weight: bold; }
    .status-warn { color: #FBBF24; font-weight: bold; }
    
    /* Prediction Banners */
    .organic-banner {
        background-color: #1E291B;
        border: 2px solid #84CC16;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #84CC16;
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .recyclable-banner {
        background-color: #17252A;
        border: 2px solid #06B6D4;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #06B6D4;
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Header / Project Title Section
col_title, col_badges = st.columns([2, 1])

with col_title:
    st.markdown("## ♻️ AI-Based Waste Segregation Bin")
    st.markdown("<p style='color:#8A94A6; margin-top:-15px;'>Real-time waste detection and classification</p>", unsafe_allow_html=True)

with col_badges:
    # Top-right quick reference pill badges
    st.markdown("""
    <div style='text-align: right; margin-top: 10px;'>
        <span style='background-color:#1E291B; color:#84CC16; padding:5px 12px; border-radius:15px; font-size:13px; margin-right:8px; border:1px solid #84CC16;'>🍃 Organic</span>
        <span style='background-color:#17252A; color:#06B6D4; padding:5px 12px; border-radius:15px; font-size:13px; border:1px solid #06B6D4;'>🔄 Recyclable</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 3. Sidebar Simulation Data Setup (For testing/live toggling)
st.sidebar.header("🎛️ Simulation Controls")
sample_prediction = st.sidebar.selectbox("Test Classification Result", ["Organic", "Recyclable", "Awaiting..."])
confidence_score = st.sidebar.slider("Confidence Level (%)", 50, 100, 83)
camera_working = st.sidebar.checkbox("Camera Connected / Active", value=True)

# 4. Layout Layout Grid: Left Content (Video & Results) vs Right Content (System Info)
left_column, right_column = st.columns([1.8, 1])

with left_column:
    # --- Live Waste Detection Section ---
    st.markdown("### 📷 Live Waste Detection")
    
    # Live Active tag mimic
    if camera_working:
        st.markdown("<span style='color:#F87171;'>● LIVE</span>", unsafe_allow_html=True)
        
        # Display the streaming camera feed
        img_file_buffer = st.camera_input("Take a snapshot / Test feed view", label_visibility="collapsed")
    else:
        # Camera error block layout from screenshot
        st.markdown("""
        <div style='background-color:#1A1D20; border: 2px dashed #F87171; border-radius:12px; height:300px; display:flex; flex-direction:column; justify-content:center; align-items:center;'>
            <p style='font-size:40px; margin:0;'>📷</p>
            <p style='color:#F87171; font-weight:bold; margin:5px 0;'>Camera access denied or unavailable</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Retry Camera")

    st.write("") # Padding

    # --- Prediction Result Section ---
    st.markdown("### 🧠 Prediction Result")
    
    if sample_prediction == "Organic":
        col_banner, col_conf = st.columns([3, 1])
        with col_banner:
            st.markdown('<div class="organic-banner">♻️ ORGANIC WASTE <br><span style="font-size:12px; font-weight:normal; color:#A3E635;">Classification complete</span></div>', unsafe_allow_html=True)
        with col_conf:
            st.markdown(f'<div class="status-card" style="text-align:center; height:85px;"><h2 style="color:#84CC16; margin:0;">{confidence_score}%</h2><p style="color:#8A94A6; font-size:12px; margin:0;">Confidence</p></div>', unsafe_allow_html=True)
            
    elif sample_prediction == "Recyclable":
        col_banner, col_conf = st.columns([3, 1])
        with col_banner:
            st.markdown('<div class="recyclable-banner">♻️ RECYCLABLE WASTE <br><span style="font-size:12px; font-weight:normal; color:#22D3EE;">Classification complete</span></div>', unsafe_allow_html=True)
        with col_conf:
            st.markdown(f'<div class="status-card" style="text-align:center; height:85px;"><h2 style="color:#06B6D4; margin:0;">{confidence_score}%</h2><p style="color:#8A94A6; font-size:12px; margin:0;">Confidence</p></div>', unsafe_allow_html=True)
            
    else:
        st.markdown('<div class="status-card" style="text-align:center; color:#8A94A6;">Awaiting classification profile input...</div>', unsafe_allow_html=True)


with right_column:
    # --- System Status Module ---
    st.markdown("""
    <div class="status-card">
        <h4 style="margin-top:0; color:#8A94A6;">📶 System Status</h4>
        <hr style="margin:10px 0; border-color:#2D3136;">
        <div style="display:flex; justify-content:between; margin-bottom:8px;">
            <span style="flex-grow:1;">Camera</span>
            <span class="{}">{}</span>
        </div>
        <div style="display:flex; justify-content:between; margin-bottom:8px;">
            <span style="flex-grow:1;">AI Model</span>
            <span class="status-ok">🟢 Running</span>
        </div>
        <div style="display:flex; justify-content:between; margin-bottom:8px;">
            <span style="flex-grow:1;">ESP32 Core</span>
            <span class="status-ok">🟢 Connected</span>
        </div>
        <div style="display:flex; justify-content:between;">
            <span style="flex-grow:1;">Servo Motor</span>
            <span class="status-warn">⚡ Activated</span>
        </div>
    </div>
    """.format(
        "status-ok" if camera_working else "status-error",
        "🟢 Active" if camera_working else "🔴 Error"
    ), unsafe_allow_html=True)

    # --- Lid Action Module ---
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-top:0; color:#8A94A6;">⚡ Lid Action</h4>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:10px 0; border-color:#2D3136;">', unsafe_allow_html=True)
    
    if sample_prediction == "Organic":
        st.markdown('<div style="background-color:#1E291B; color:#84CC16; padding:12px; border-radius:8px; font-weight:bold; text-align:center;">🔓 Opening Organic Lid</div>', unsafe_allow_html=True)
    elif sample_prediction == "Recyclable":
        st.markdown('<div style="background-color:#17252A; color:#06B6D4; padding:12px; border-radius:8px; font-weight:bold; text-align:center;">🔓 Opening Recyclable Lid</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#8A94A6; text-align:center; font-style:italic; margin:5px 0;">Awaiting classification...</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Timer / Auto Close Module ---
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-top:0; color:#8A94A6;">⏱️ Auto Close Timer</h4>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:10px 0; border-color:#2D3136;">', unsafe_allow_html=True)
    
    if sample_prediction in ["Organic", "Recyclable"]:
        st.markdown("""
        <div style="text-align:center;">
            <div style="display:inline-block; border: 3px solid #4ADE80; border-radius:50%; width:50px; height:50px; line-height:44px; font-size:20px; color:#4ADE80; font-weight:bold; margin-bottom:10px;">3</div>
            <p style="color:#A3E635; margin:0; font-size:14px;">Closing lid in 3 seconds...</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#8A94A6; text-align:center; font-style:italic; margin:5px 0;">Timer inactive</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
