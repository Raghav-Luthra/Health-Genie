from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import base64

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCbkB5-zV7XrODvkM9x0LfHhKtN61e9E_E")

# Load models
text_model = genai.GenerativeModel("gemini-pro")
image_model = genai.GenerativeModel("gemini-pro-vision")

# Function to analyze food from an image
def analyze_food(image_base64):
    prompt = "Analyze this food image and give details about calories, proteins, and nutrients."

    try:
        # Decode base64 image to bytes
        image_bytes = base64.b64decode(image_base64)

        # Send to Gemini
        response = image_model.generate_content([prompt, image_bytes])
        return response.text if response and hasattr(response, "text") else "No response received."
    except Exception as e:
        return f"Error analyzing food: {str(e)}"

# Function to diagnose based on symptoms
def ai_doctor(symptoms):
    prompt = f"I have the following symptoms: {symptoms}. What possible conditions could this be? Provide recommendations."
    try:
        response = text_model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else "No response received."
    except Exception as e:
        return f"Error processing symptoms: {str(e)}"

# Function to generate a diet plan
def generate_diet_plan(goal):
    prompt = f"My goal is {goal}. Suggest a balanced meal plan with breakfast, lunch, and dinner."
    try:
        response = text_model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else "No response received."
    except Exception as e:
        return f"Error generating diet plan: {str(e)}"

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze_food", methods=["POST"])
def analyze_food_route():
    data = request.json
    image_base64 = data.get("image")
    if not image_base64:
        return jsonify({"error": "No image provided"}), 400
    food_analysis = analyze_food(image_base64)
    return jsonify({"food_analysis": food_analysis})

@app.route("/ai_doctor", methods=["POST"])
def ai_doctor_route():
    data = request.json
    symptoms = data.get("symptoms")
    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400
    diagnosis = ai_doctor(symptoms)
    return jsonify({"diagnosis": diagnosis})

@app.route("/diet_plan", methods=["POST"])
def diet_plan_route():
    data = request.json
    goal = data.get("goal")
    if not goal:
        return jsonify({"error": "No goal provided"}), 400
    diet_plan = generate_diet_plan(goal)
    return jsonify({"diet_plan": diet_plan})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
