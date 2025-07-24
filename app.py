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

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forceurl': True,
        'format': 'best[ext=mp4]/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info.get('url')

    # Instead of returning the real video link (which iOS hates), return your proxy
    return jsonify({
        'proxy_stream_url': f'https://yt-dlp-wrapper-flask-1.onrender.com/stream?target={stream_url}'
    })

@app.route('/stream')
def stream():
    target_url = request.args.get('target')

    def generate():
        with requests.get(target_url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    response = Response(stream_with_context(generate()), content_type="video/mp4")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Disposition'] = 'inline'
    return response
