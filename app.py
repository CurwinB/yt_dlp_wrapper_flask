
import os
from flask import Flask, request, render_template, jsonify, send_file
import yt_dlp
import sys
print(sys.version_info)
print(yt_dlp.version.__version__)

app = Flask(__name__)

@app.route("/download/<vid>/<start_time>/<end_time>")
def download(vid, start_time, end_time):
	start = int(float(start_time))
	end = int(float(end_time))
	output_filename = vid+"_"+str(start)+"_"+str(end)
	matching_files = [x for x in os.listdir(".") if x.startswith(output_filename) and not x.endswith("part")]
	if matching_files:
		return send_file(matching_files[0])
	[os.remove(x) for x in os.listdir(".") if not os.path.isdir(x) and x.count("_")]
	video_url = "https://youtube.com/watch?v="+vid
	params = {
			'download_ranges': yt_dlp.utils.download_range_func([], [[start, end]]),
			'match_filter': yt_dlp.utils.match_filter_func("!is_live & live_status!=is_upcoming & availability=public"),
			'outtmpl': {'default': output_filename},
		}
	with yt_dlp.YoutubeDL(params) as ydl:
		try:
			ydl.download([video_url])
		except yt_dlp.utils.DownloadError as e:
			return str(e)

	return send_file([x for x in os.listdir(".") if x.startswith(output_filename)][0])

@app.route("/")
def index():
	return "Yes."
