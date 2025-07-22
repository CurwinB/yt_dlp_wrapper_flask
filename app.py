import os
import sys
from flask import Flask, request, send_file, jsonify
import yt_dlp

print(sys.version_info)
import importlib.metadata
print(importlib.metadata.version("yt-dlp"))


app = Flask(__name__)

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    output_filename = "video_output.%(ext)s"

    params = {
        'outtmpl': output_filename,
        'format': 'best',  # You can tweak this (e.g., 'bestvideo+bestaudio')
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(params) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": str(e)}), 500

    # Find the actual downloaded file name
    downloaded_file = next((f for f in os.listdir(".") if f.startswith("video_output.")), None)
    if not downloaded_file:
        return jsonify({"error": "Video download failed"}), 500

    return send_file(downloaded_file, as_attachment=True)

@app.route("/")
def index():
    return "Yes."

