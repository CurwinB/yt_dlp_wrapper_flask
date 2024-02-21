
import os
from flask import Flask, request, render_template, jsonify, send_file
import yt_dlp
import sys
print(sys.version_info)
print(yt_dlp.version.__version__)

app = Flask(__name__)

@app.route("/download/<vid>/<start_time>/<end_time>")
def download(vid, start_time, end_time):
  output_filename = vid+"_"+start_time+"_"+end_time
  video_url = "https://youtube.com/watch?v="+vid
  print(video_url)
  print(yt_dlp.version.__version__)
  params = {
        'download_ranges': yt_dlp.utils.download_range_func([], [[start_time, end_time]]),
        'match_filter': yt_dlp.utils.match_filter_func("!is_live & live_status!=is_upcoming & availability=public"),
        'no_warnings': True,
        'noprogress': True,
        'outtmpl': {'default': output_filename},
        'quiet': True
    }
  with yt_dlp.YoutubeDL(params) as ydl:
      try:
          ydl.download([video_url])
      except yt_dlp.utils.DownloadError as e:
          return str(e)
  return send_file([x for x in os.listdir(".") if x.startswith(output_filename)][0])

@app.route("/")
def index():
  return "Yes"


if __name__ == '__main__':
    app.run()