import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API Key securely
genai.configure(api_key="AIzaSyAuP6bX1RwtAhtDUr4mYMKLjlaETc0AMEY")

# Load Gemini Model
gemini_model = genai.GenerativeModel('gemini-pro')

# Streamlit App Configuration
st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styles
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; height: 3em; }
    .success-box { padding: 1rem; border-radius: 0.5rem; background-color: #f0fff4; border: 1px solid #9ae6b4; }
    .warning-box { padding: 1rem; border-radius: 0.5rem; background-color: #fffaf0; border: 1px solid #fbd38d; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# AI Response Function
def generate_response(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text

# Display Dietary Plan
def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        st.markdown("### 🍽️ Meal Plan")
        st.success(plan_content)

# Display Fitness Plan
def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        st.markdown("### 🏋️‍♂️ Workout Routine")
        st.success(plan_content)

# Main App Function
def main():
    st.title("🏋️‍♂️ AI Health & Fitness Planner")
    st.markdown("""
        <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
        Get personalized dietary and fitness plans tailored to your goals and preferences.
        </div>
    """, unsafe_allow_html=True)

    # User Inputs
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        height = st.number_input("Height (cm)", min_value=100.0, value=170.0)
        activity_level = st.selectbox(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
        )
        dietary_preferences = st.selectbox(
            "Dietary Preferences",
            options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"]
        )

    with col2:
        weight = st.number_input("Weight (kg)", min_value=20.0, value=70.0)
        sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
        fitness_goals = st.selectbox(
            "Fitness Goals",
            options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"]
        )

    # Generate Plans Button
    if st.button("🎯 Generate My Plan"):
        with st.spinner("Creating your personalized plan..."):
            try:
                # User Profile
                user_profile = f"""
                Age: {age}
                Weight: {weight}kg
                Height: {height}cm
                Sex: {sex}
                Activity Level: {activity_level}
                Dietary Preferences: {dietary_preferences}
                Fitness Goals: {fitness_goals}
                """

                # Dietary Plan Prompt
                dietary_prompt = f"""
                You are a dietary expert providing a personalized meal plan based on the following user profile:
                {user_profile}
                Include meal plans for breakfast, lunch, dinner, and snacks, with explanations.
                """
                dietary_plan_response = generate_response(dietary_prompt)

                # Fitness Plan Prompt
                fitness_prompt = f"""
                You are a fitness expert providing a personalized workout plan based on the following user profile:
                {user_profile}
                Include warm-ups, workouts, and cool-downs with explanations.
                """
                fitness_plan_response = generate_response(fitness_prompt)

                # Display Plans
                display_dietary_plan(dietary_plan_response)
                display_fitness_plan(fitness_plan_response)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
