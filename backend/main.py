from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/analyze", methods=['POST'])
def analyze_document():
    """
    This endpoint will eventually receive a PDF, analyze it with Gemini,
    and return the full analysis. For now, it returns a mock/fake response.
    """

    # In the future, we'll process the uploaded file here.
    # file = request.files['file']

    # --- MOCK DATA ---
    # This is a fake response. The Frontend Developer will use this structure
    # to build the UI while the AI logic is being developed.
    mock_analysis = {
        "healthScore": 72,
        "summary": {
            "parties": "Arun (Freelancer) vs. Innovate Corp (Client)",
            "agreementType": "Freelance Service Contract",
            "keyDates": "Effective Date: Aug 26, 2025",
            "financials": "Project Fee: ₹50,000"
        },
        "actionItems": [
            { "risk": "High", "text": "Payment term is 'Net 90', which is longer than the industry standard." },
            { "risk": "Medium", "text": "The Intellectual Property clause is overly broad." },
            { "risk": "Low", "text": "The termination clause is unclear." }
        ]
    }

    return jsonify(mock_analysis)

if __name__ == "__main__":
    app.run(debug=True)
    
