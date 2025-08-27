from flask import Flask, jsonify, request
from flask_cors import CORS
import PyPDF2
import io

# Import our new AI function
from ai_analyzer import analyze_text_with_gemini

app = Flask(__name__)
CORS(app)

@app.route("/api/analyze", methods=['POST'])
def analyze_document():
    # 1. Check if a file was uploaded in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 2. Read the PDF file from memory
        pdf_stream = io.BytesIO(file.read())
        reader = PyPDF2.PdfReader(pdf_stream)

        # 3. Extract text from all pages of the PDF
        document_text = ""
        for page in reader.pages:
            document_text += page.extract_text() or ""

        if not document_text.strip():
             return jsonify({"error": "Could not extract text from PDF"}), 400

        # 4. Call our new Gemini function with the extracted text
        analysis_result = analyze_text_with_gemini(document_text)

        # 5. Return the REAL analysis from the AI
        return jsonify(analysis_result)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)