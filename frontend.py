import streamlit as st
import requests
from PIL import Image

# API Endpoint (Backend URL)
API_URL = "http://127.0.0.1:5000/generate-plan"

# Streamlit UI Setup
st.set_page_config(page_title="NutriVision", layout="wide")

st.title("🌟 NutriVision - AI-Powered Fitness Planner")
st.subheader("Achieve Your Dream Physique with AI")

# Collect user details
st.sidebar.header("👤 User Details")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.sidebar.number_input("Weight (kg)", min_value=1, max_value=300, step=1)
height = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, step=1)
health_issues = st.sidebar.text_area("Health Issues (if any)", placeholder="E.g., diabetes, hypertension, none")

food_type = st.sidebar.selectbox("🍽 Food Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
halal = st.sidebar.radio("🥩 Do you prefer halal food?", ["Yes", "No"])

# Upload images
st.sidebar.subheader("📸 Upload Your Images")
current_image = st.sidebar.file_uploader("Upload your current body image", type=["png", "jpg", "jpeg"])
desired_image = st.sidebar.file_uploader("Upload the body you want to achieve", type=["png", "jpg", "jpeg"])

st.sidebar.subheader("🚀 Ready?")
if st.sidebar.button("Generate My AI Plan"):
    if current_image and desired_image:
        if current_image.size > 5 * 1024 * 1024 or desired_image.size > 5 * 1024 * 1024:
            st.error("⚠ Image size should be less than 5MB.")
        else:
            user_details = {
                "age": age,
                "weight": weight,
                "height": height,
                "health_issues": health_issues,
            }
            preferences = {
                "food_type": food_type,
                "halal": halal,
            }

            with st.spinner("Generating your AI-powered plan..."):
                response = requests.post(API_URL, json={"user_details": user_details, "preferences": preferences})

            if response.status_code == 200:
                st.success("✅ Plan Generated Successfully!")
                st.subheader("📋 Your AI-Generated 7-Day Plan:")
                st.text(response.json().get("plan"))

                # Show uploaded images
                st.subheader("🖼 Uploaded Images")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(Image.open(current_image), caption="Current Body", width=250)
                with col2:
                    st.image(Image.open(desired_image), caption="Target Physique", width=250)

            else:
                st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.error("⚠ Please upload both images to proceed.")