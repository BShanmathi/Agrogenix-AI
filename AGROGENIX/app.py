from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from gtts import gTTS
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load Summarization Model
summarizer = pipeline("summarization")

# Summarize Endpoint
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    paragraph = data.get("text", "")
    if not paragraph:
        return jsonify({"error": "No text provided"}), 400

    summary = summarizer(paragraph, max_length=50, min_length=20, do_sample=False)
    return jsonify({"summary": summary[0]['summary_text']})

# Generate Video Endpoint
@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    summary = data.get("summary", "")
    if not summary:
        return jsonify({"error": "No summary provided"}), 400

    # Generate voiceover
    tts = gTTS(summary, lang='en')
    audio_path = "static/voiceover.mp3"
    tts.save(audio_path)

    # Dummy video generation (update later with MoviePy logic)
    video_path = "static/output.mp4"
    os.system(f"ffmpeg -loop 1 -i sample.jpg -i {audio_path} -shortest -c:v libx264 -c:a aac -strict experimental {video_path}")

    return jsonify({"video_url": video_path})

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
