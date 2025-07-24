from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'yes'

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        info = json.loads(result.stdout)
        hls_url = None

        # Try to find the best HLS stream
        for fmt in info.get('formats', []):
            if fmt.get('ext') == 'mp4' and fmt.get('protocol') == 'm3u8_native':
                hls_url = fmt.get('url')
                break
            elif fmt.get('protocol') == 'm3u8_native':
                hls_url = fmt.get('url')  # fallback to any HLS if no MP4

        if not hls_url:
            return jsonify({'error': 'No HLS stream found'}), 404

        return jsonify({'hls_url': hls_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
