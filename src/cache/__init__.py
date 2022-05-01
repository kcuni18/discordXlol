from . import match
from . import summoner
from .core import *

import os.path as path
import os

if not path.isdir(directory):
	os.mkdir(directory)
if not path.isdir(directory_matches):
	os.mkdir(directory_matches)
if not path.isdir(directory_summoners):
	os.mkdir(directory_summoners)
