import vertexai
from vertexai.generative_models import GenerativeModel
import json

# --- CONFIGURATION ---
PROJECT_ID = "certify-ai-hackathon"  # Replace with your project ID
LOCATION = "us-central1"            # Replace with your desired location

def analyze_text_with_gemini(document_text: str) -> dict:
    """
    Analyzes the given text using the Gemini model via Vertex AI.

    Args:
        document_text: The text extracted from the PDF document.

    Returns:
        A dictionary containing the structured analysis.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-1.0-pro")

    # This is the "magic" - a highly specific prompt telling the AI exactly what to do.
    prompt = f"""
    You are an AI legal assistant named CertifyAI. Your task is to analyze the following legal document text and return a JSON object with a forensic audit.

    The JSON object must have the following exact structure:
    {{
      "healthScore": <an integer between 0 and 100 assessing the overall fairness and clarity>,
      "summary": {{
        "parties": "<Identify the main parties involved>",
        "agreementType": "<Identify the type of agreement, e.g., Freelance Contract, Lease Agreement>",
        "keyDates": "<Identify key dates like effective date or term length>",
        "financials": "<Identify key financial terms like fees or salary>"
      }},
      "actionItems": [
        {{
          "risk": "<'High', 'Medium', or 'Low'>",
          "text": "<A clear, one-sentence description of a risky or non-standard clause>"
        }}
      ]
    }}

    Analyze the following document text:
    ---
    {document_text}
    ---
    """

    try:
        response = model.generate_content(prompt)

        # Extract the JSON string from the response
        json_string = response.text.strip().replace("```json", "").replace("```", "")

        # Convert the JSON string into a Python dictionary
        analysis_result = json.loads(json_string)
        return analysis_result

    except Exception as e:
        # If the AI fails or returns malformed JSON, return an error dictionary
        return {"error": f"An error occurred during AI analysis: {str(e)}"}