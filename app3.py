import streamlit as st
import pandas as pd
import requests
import io

st.title("📘 English Quiz from CSV")

# --- STEP 1: Load CSV from GitHub ---
csv_url = "https://raw.githubusercontent.com/yeeunk28/Myapps/main/quiz_questions.csv"

try:
    response = requests.get(csv_url)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    df.columns = df.columns.str.strip().str.replace(" ", "").str.capitalize()
except Exception as e:
    st.error(f"❌ Failed to load quiz data: {e}")
    st.stop()

# --- STEP 2: Display Quiz Questions ---
st.header("🧠 Take the Quiz")

if df.empty:
    st.warning("The quiz file is empty or incorrectly formatted.")
else:
    for idx, row in df.iterrows():
        question = row["Question"]
        options = [row[f"Option{i}"] for i in range(1, 6)]
        correct_answer = row["Answer"]

        with st.form(key=f"form_{idx}"):
            st.subheader(f"Q{idx+1}: {question}")
            user_choice = st.radio("Choose one:", options, key=f"q_{idx}")
            submitted = st.form_submit_button("Check Answer")

            if submitted:
                if user_choice == correct_answer:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Not quite. The correct answer is **{correct_answer}**")
