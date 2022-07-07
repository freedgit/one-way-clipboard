from flask import Flask
from flask import request
from flask import make_response

import os
import json
import time

import clipboard as pc

def get_paths():
    paths = {
        "insert_path": "/tmp/insert.json"
        , "clip_path": "/tmp/clip.json"
    }

    return paths
