import os.path as path
import os

directory = "cache"
directory_matches = "cache/matches"
directory_summoners = "cache/summoners"

def init():
	if not path.isdir(directory):
		os.mkdir(directory)
	if not path.isdir(directory_matches):
		os.mkdir(directory_matches)
	if not path.isdir(directory_summoners):
		os.mkdir(directory_summoners)
