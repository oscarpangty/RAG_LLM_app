from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
import json
import ollama

import os
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for messages
messages = []

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def post_message():
    user_message = request.json
    messages.append(user_message)

    # Generate a response from the LLM
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': user_message['text'],
        },
    ])

    llm_response = {
        'text': response['message']['content'],
        'sender': 'llm'
    }
    messages.append(llm_response)
    print(messages)
    return jsonify(llm_response), 201

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    text = request.form.get('text', '')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded file to a directory
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Use raw string or forward slashes to avoid unicode escape issues
        file_path = r'{}'.format(file_path)

        # Generate a response from the Llava model with the image and text
        response = ollama.chat(model='llava', messages=messages+[
            {
                'role': 'user',
                'content': text,
                'images': [file_path]
            }
        ])

        llm_response = {
            'text': response['message']['content'],
            'sender': 'llm'
        }
        messages.append(llm_response)
        print(messages)
        return jsonify(llm_response), 201

    except Exception as e:
        print(f"Error processing image: {e}")  # Log the error
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
