from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Debugging: Print API key (Comment this after checking)
if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found. Check .env file!")

app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    """ Generate AI-powered diet & fitness plan """
    data = request.json
    user_details = data.get("user_details", {})
    preferences = data.get("preferences", {})

    # Input validation
    if not all(key in user_details for key in ['age', 'weight', 'height']):
        return jsonify({"error": "Missing required user details"}), 400

    prompt = f"""
    User Profile:
    - Age: {user_details.get('age')}
    - Weight: {user_details.get('weight')} kg
    - Height: {user_details.get('height')} cm
    - Health Issues: {user_details.get('health_issues')}
    - Food Type: {preferences.get('food_type')}
    - Halal Preference: {preferences.get('halal')}

    Generate a **7-day AI-powered diet and fitness plan** based on this user.
    """

    try:
        # Using latest OpenAI API format
        client = openai.OpenAI(api_key=API_KEY)  

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        return jsonify({"plan": response.choices[0].message.content.strip()})

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": f"Unexpected Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)