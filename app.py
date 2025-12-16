import streamlit as st
import pandas as pd
import openai
import time
import random

# ---------------------------------------------------------
# 1. API Key Setup
# ---------------------------------------------------------
# OpenAI Key (Required for AI Analysis)
# Since we are using dummy metrics, we still need this to generate the report text.
OPENAI_API_KEY = "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"

# ---------------------------------------------------------
# 2. App Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="KOL Manager Pro (Demo)", page_icon="🧪", layout="wide")

# 🔴 GLOBAL WARNING BANNER
st.error("⚠️ DEMO MODE ACTIVATED: All data displayed below is RANDOMLY GENERATED for testing purposes. It is NOT real Twitter data.")

st.title("🧪 KOL Performance & Portfolio Manager (Simulation)")

# Tabs
tab1, tab2 = st.tabs(["📊 Tweet Analysis (Demo)", "💰 Budget Portfolio"])

# ---------------------------------------------------------
# 3. [Tab 1] Tweet Analysis (Mock Data)
# ---------------------------------------------------------
with tab1:
    st.subheader("Tweet Performance Simulator")
    st.info("ℹ️ Enter any URL to generate a simulated analysis report.")
    
    tweet_url = st.text_input("Enter Tweet URL", placeholder="https://x.com/username/status/...")
    
    if st.button("🚀 Analyze (Generate Dummy Data)"):
        if not tweet_url:
            st.warning("Please enter a URL first!")
        else:
            with st.spinner("Simulating data retrieval..."):
                time.sleep(1.5) # Fake loading time for realistic vibe
                
                # --- 🎲 GENERATING DUMMY DATA ---
                dummy_views = random.randint(10000, 500000)
                dummy_likes = int(dummy_views * random.uniform(0.02, 0.08)) # 2%~8% engagement rate
                dummy_retweets = int(dummy_likes * random.uniform(0.1, 0.3))
                dummy_replies = int(dummy_likes * random.uniform(0.05, 0.1))
                
                # Dummy Content
                dummy_text = "Crypto marketing is evolving. It's not just about hype anymore, but about building genuine community trust. #Web3 #Marketing"
                
                # Display Metrics
                st.success("Analysis Complete (Simulated)")
                
                # 1. Metrics Row
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Views (Simulated)", f"{dummy_views:,}")
                col2.metric("Likes", f"{dummy_likes:,}")
                col3.metric("Retweets", f"{dummy_retweets:,}")
                col4.metric("Replies", f"{dummy_replies:,}")
                
                st.divider()
                
                # 2. AI Analysis (Using OpenAI with Dummy Data)
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                
                prompt = f"""
                Act as a Senior Social Media Marketing Expert.
                Analyze the following SIMULATED tweet data.
                
                [Tweet Content]: {dummy_text}
                [Metrics]: {dummy_views} Views, {dummy_likes} Likes, {dummy_retweets} Retweets.
                
                Please provide a report in English:
                1. **Performance Analysis**: Why did this hypothetical tweet perform well?
                2. **Optimization Strategy**: Suggest specific improvements for the next campaign.
                """
                
                try:
                    with st.spinner("AI is writing the report..."):
                        completion = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.markdown("### 🤖 AI Insight Report")
                        st.write(completion.choices[0].message.content)
                        
                        st.caption("Note: This insight is based on simulated metrics.")
                        
                except Exception as e:
                    st.error(f"OpenAI Error: {e}")

# ---------------------------------------------------------
# 4. [Tab 2] Portfolio (Already Mock Data)
# ---------------------------------------------------------
with tab2:
    st.subheader("💰 Budget-Optimized KOL Recommendation")
    
    # Mock Database
    KOL_DB = [
        {"name": "AlphaUser", "region": "US", "price": 500, "avg_views": 10000},
        {"name": "KimCrypto", "region": "KR", "price": 300, "avg_views": 8000},
        {"name": "SatoshiJ", "region": "JP", "price": 400, "avg_views": 9000},
        {"name": "WhaleHunter", "region": "US", "price": 1200, "avg_views": 30000},
        {"name": "CoinMaster", "region": "KR", "price": 150, "avg_views": 2000},
        {"name": "EuroGem", "region": "EU", "price": 600, "avg_views": 11000},
        {"name": "LondonCrypto", "region": "EU", "price": 750, "avg_views": 13000},
    ]
    
    col1, col2 = st.columns(2)
    budget = col1.number_input("Total Budget ($)", min_value=100, value=1000, step=100)
    target_region = col2.selectbox("Target Region", ["All", "KR", "US", "JP", "EU"])
    
    if st.button("Generate Portfolio"):
        selected_kols = []
        current_spend = 0
        total_reach = 0
        
        # Filtering & Logic
        filtered_db = [k for k in KOL_DB if target_region == "All" or k['region'] == target_region]
        filtered_db.sort(key=lambda x: x['avg_views']/x['price'], reverse=True) # Sort by ROI
        
        for kol in filtered_db:
            if current_spend + kol['price'] <= budget:
                selected_kols.append(kol)
                current_spend += kol['price']
                total_reach += kol['avg_views']
        
        # Display Results
        if selected_kols:
            st.success(f"✅ Recommended {len(selected_kols)} KOLs!")
            
            # Show Table
            df = pd.DataFrame(selected_kols)
            st.dataframe(df)
            
            # Summary Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Cost", f"${current_spend}")
            c2.metric("Remaining Budget", f"${budget - current_spend}")
            c3.metric("Est. Total Reach", f"{total_reach:,}")
            
        else:
            st.warning("Budget is too low to hire any KOL from the list.")