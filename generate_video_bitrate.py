import json
import subprocess
import shlex
import time

def _os_execute(command):
	result, err = subprocess.Popen(
		shlex.split(command),
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE).communicate()
	return result, err

filename = "SampleVideo_1280x720_1mb.mp4"

start = time.time()

# get info about video
video_info, err = _os_execute("ffprobe -v quiet -print_format json -show_format -show_streams {}".format(filename))
video_info = json.loads(video_info)

# calculate video bitrate
vid_bitrate_07 = int(int(video_info["streams"][0]["bit_rate"]) * 0.7)
vid_bitrate_06 = int(int(video_info["streams"][0]["bit_rate"]) * 0.6)

# resize video with same ratio
vid_width = int(video_info["streams"][0]["width"])
vid_height = int(video_info["streams"][0]["height"])
target_width = 640
target_height = int(target_width * vid_height / vid_width)

min_height = 480
max_height = 960

if target_height < min_height:
	cmd_resize_video = "-vf scale={}:{}".format(target_width, min_height)
elif target_height > max_height:
	cmd_resize_video = "-vf scale={}:{}".format(target_width, max_height)
else:
	cmd_resize_video = "-vf scale={}:{}".format(target_width, target_heigth)

# create video with compress video bitrate => 0.7
_os_execute("ffmpeg -i {} {} -b:v {} -maxrate {} -preset veryfast output_bitrate_07.mp4".format(filename, cmd_resize_video, vid_bitrate_07, vid_bitrate_07))

# create video with compress video bitrate => 0.6
_os_execute("ffmpeg -i {} {} -b:v {} -maxrate {} -preset veryfast output_bitrate_06.mp4".format(filename, cmd_resize_video, vid_bitrate_06, vid_bitrate_06))

# create with without compress video bitrate
_os_execute("ffmpeg -i {} {} -preset veryfast output_bitrate_1.mp4".format(filename, cmd_resize_video))

finish = time.time()
print("waktu proses : %s" % str(finish - start))