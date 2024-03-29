import json
from time import time

from config import MAIN_DIR, STORAGE_PATH


def print_json_to_file(struct):
    with open(MAIN_DIR + STORAGE_PATH + f'/parsed_data{time()}') as outfile:
        json.dump(struct, outfile)
