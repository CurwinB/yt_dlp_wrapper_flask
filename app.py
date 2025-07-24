from flask import Flask, request, jsonify, Response, stream_with_context
import requests
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return 'LustTag yt-dlp backend is running.'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = subprocess.run(
        ['yt-dlp', '-g', '-f', 'best[ext=mp4]/best', url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    stream_url = result.stdout.strip()

    return jsonify({
        "stream_url": stream_url
    })
