# yt_dlp_wrapper_flask

This is a simple wrapper made with flask for yt-dlp. 

as of now there's only one route that is implemented that i use in my other project to extract clips from video/livestreams

`/download/<video-id>/<start-time>/<end-time>`</br>
where start-time and end-time are number. (float or int). 
and video-id is simply video id from youtube. </br>
Example - `https://www.youtube.com/watch?v=nWed2eTY7_Q` -> `nWed2eTY7_Q`
