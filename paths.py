"""
paths.py : Maintain path constants to our data.

"""
from os.path import join

# PATH CONSTANTS
DATA_PATH = "data"
IMG_PATH = join(DATA_PATH, "images")
LEVEL_PATH = join(DATA_PATH, "levels")

# Helper Functions
def getImagePath(img_file):
	return join(IMG_PATH, img_file)

def getLevelPath(lvl_file):
	return join(LEVEL_PATH, lvl_file)
