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
        
        # Filter for HLS streams and sort by quality
        hls_formats = []
        for fmt in info.get('formats', []):
            if fmt.get('protocol') == 'm3u8_native':
                hls_formats.append(fmt)
        
        if not hls_formats:
            return jsonify({'error': 'No HLS stream found'}), 404
        
        # Sort by height (resolution) descending, then by tbr (total bitrate) descending
        hls_formats.sort(key=lambda x: (
            x.get('height', 0), 
            x.get('tbr', 0)
        ), reverse=True)
        
        # Get the best quality HLS stream
        best_format = hls_formats[0]
        hls_url = best_format.get('url')
        
        return jsonify({
            'hls_url': hls_url,
            'quality': f"{best_format.get('height', 'unknown')}p",
            'bitrate': best_format.get('tbr', 'unknown')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

