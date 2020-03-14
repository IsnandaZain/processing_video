import json
import subprocess
import shlex
from typing import List

def _os_execute(command):
	result, err = subprocess.Popen(
		shlex.split(command),
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE).communicate()
	return result, err

def get_video_info(filename):
	video_info, err = _os_execute("ffprobe -v quiet -print_format json -show_format -show_streams {}".format(filename))
	video_info = json.loads(video_info)
	return video_info

def check_property_bitrate(filename_list: List[str]):
	for filename in filename_list:
		video_info = get_video_info(filename=filename)
		print(int(video_info["streams"][0]["bit_rate"]))

def check_property_width_height(filename_list: List[str]):
	for filename in filename_list:
		video_info = get_video_info(filename=filename)
		print("width : %i" % int(video_info["streams"][0]["width"]))
		print("height : %i " % int(video_info["streams"][0]["height"]))

def check_property_video(filename_list, 
						 check_width_height=False,
						 check_bitrate=False):
	if check_width_height:
		check_property_width_height(filename_list)
	if check_bitrate:
		check_property_bitrate(filename_list)


filename_list = ["output_bitrate_06.mp4", "output_bitrate_07.mp4", "output_bitrate_1.mp4"]
check_property_video(filename_list, 
					 check_width_height=True,
					 check_bitrate=True)