from flask import Flask, request, jsonify
from anthropic import Anthropic
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Load environment variables first
load_dotenv()

# Initialize Flask app before other configurations
app = Flask(__name__)

# Configure CORS
CORS(app,
     origins=["*"],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type"]
)

# Validate API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables!")
elif not api_key.startswith('sk-ant-'):
    raise ValueError(f"API key appears to be invalid format: {api_key[:10]}...")
else:
    print("API key loaded successfully:", api_key[:10] + "...")

# Create Anthropic client
client = Anthropic(
    api_key=api_key.strip()
)

# Routes remain the same
@app.route("/")
def home():
    return "<h1>Hello world</h1>"

@app.route("/api/claude", methods=["POST"])
def query_claude():
    try:
        data = request.json
        query = data.get("query")
        print("Received query:", query)

        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        try:
            message = client.messages.create(
                model="claude-3-sonnet-20240229",  # Updated model name
                max_tokens=1000,
                temperature=0,
                messages=[{"role": "user", "content": query}],
            )
            return jsonify({"response": message.content[0].text}), 200
        except Exception as api_error:
            print(f"Anthropic API Error details: {str(api_error)}")
            return jsonify({"error": f"API Error: {str(api_error)}"}), 500
    
    except Exception as e:
        print(f"General Error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
