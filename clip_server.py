#!/usr/bin/env python3

from utils import *

PASTE_LIMIT = 5000

app = Flask(__name__)

def show_form():
    with open("clip.html", "r") as f:
        r = f.read()

    return r

def read_js():
    with open("funcs.js", "r") as f:
        r = f.read()

    return r

def get_file():
    paths = get_paths()

    file_path = paths["clip_path"]
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            r = f.read()

            os.remove(file_path)

            return r

    ret = {}
    ret["type"] = "nothing"
    ret["content"] = ""
        
    return json.dumps(ret)
    
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # whitelist = ['http://localhost:9999']
    # r = request.referrer[:-1]
    # if r in whitelist:
    #     response.headers.add('Access-Control-Allow-Origin', r)
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    #     response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    #     response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    #     response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    # return response        
        

@app.route("/", methods=["GET"])
def index():
    print(request.method)
    
    response = make_response(get_file(), 200)
    response.mimetype = "application/json"
    return response

@app.route("/form/", methods=["GET", "POST"])
def form():
    print(request.method)

    if request.method == "POST":
        pastearea = request.form["pastearea"]
        pastearea = pastearea[0:PASTE_LIMIT]

        r = {}
        r["type"] = "content"
        r["content"] = pastearea

        paths = get_paths()
        insert_path = paths["insert_path"]
        with open(insert_path, "w") as f:
            f.write(json.dumps(r))

    response = make_response(show_form(), 200)
    response.mimetype = "text/html"
    return response

@app.route("/form/funcs.js", methods=["GET"])
def return_js():
    response = make_response(read_js(), 200)
    response.mimetype = "application/javascript"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)
