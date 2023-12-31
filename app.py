import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            user_input = request.form['user_input']
        except KeyError:
            user_input = ""

        prompt = f"""Imagine you are a medical expert and you are giving accurate medical advice to a patient. 
        You are presented with a medical query and asked to provide a response with a detailed explanation. 
        Note that dont mention any inaccurate or misleading information.

        Medical Query: {user_input}

        Key Details:
        - Provide precise information related to the patient's medical concern.
        - Indicate if any diagnostic tests or examinations have been performed.
        - Specify the current medications or treatments prescribed.
        - The response should be in a paragraph format but not in point-wise.
        - If only a specific disease name is mentioned, response must contain the symptoms, causes, and treatment of the disease with respective headings.

        Guidelines:
        - Use clear and concise language.
        - The vocabulary should be appropriate for the medical context.
        - Include specific parameters or considerations within the medical context.
        - If the response contains a list of items, convert it into a paragraph format.
        - Avoid using abbreviations or acronyms.
        - Avoid Headings and Sub hheadings just give me the complete response in a paragraph format.
        - Refrain from presenting inaccurate or ambiguous information.
        - Ensure the query is focused and not overly broad."""

        # Get Gemini response
        gemini_response = get_gemini_response(prompt)

        return render_template('index.html', user_input=user_input, response=gemini_response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)