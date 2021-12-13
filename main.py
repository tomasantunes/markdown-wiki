from flask import Flask, render_template, jsonify, request, send_from_directory
import os
from pathlib import Path
import markdown
from os import listdir
from os.path import isfile, join
from flask_jsglue import JSGlue
import time

app = Flask(__name__)
jsglue = JSGlue(app)

wiki_folder = "wiki"
static_folder = "wiki"
wiki_route = "/wiki"
wiki_title = "Markdown Wiki"
exclude = set(['.git', 'app'])
tree = {}
count = 0
for root, dirs, files in os.walk(wiki_folder, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    md_files = [ fi for fi in files if fi.endswith(".md") ]
    if (count == 0):
        for i in dirs:
            tree[i] = {}
    else:
        parts = Path(root).parts
        if (len(parts) == 2):
            tree[parts[1]]["root"] = root
            tree[parts[1]]["folders"] = {}
            tree[parts[1]]["md_files"] = md_files
            for i in dirs:
                tree[parts[1]]["folders"][i] = {}
        elif (len(parts) == 3):
            tree[parts[1]]["folders"][parts[2]]["root"] = root
            tree[parts[1]]["folders"][parts[2]]["folders"] = {}
            tree[parts[1]]["folders"][parts[2]]["md_files"] = md_files
            for i in dirs:
                tree[parts[1]]["folders"][parts[2]]["folders"][i] = {}
                tree[parts[1]]["folders"][parts[2]]["folders"][i]["root"] = join(root, i)
    count += 1

@app.route(wiki_route)
def mainWiki():
    return render_template(wiki_folder + "/" + "index.html", wiki_folder=wiki_folder, wiki_route=wiki_route, static_folder=static_folder, wiki_title=wiki_title)

@app.route(wiki_route + "/feed")
def feed():
    return render_template(wiki_folder + "/" + "feed.html", wiki_folder=wiki_folder, wiki_route=wiki_route, static_folder=static_folder, wiki_title=wiki_title)

@app.route(wiki_route + "/get-feed")
def getFeed():
    with open(wiki_folder + "/" + "logs/feed.md", encoding="utf8") as f:
        lines = f.readlines()
        return jsonify(lines)

@app.route(wiki_route + "/refresh-repo")
def refreshRepo():
	return 'OK'
	

@app.route(wiki_route + "/get-tree")
def getTree():
    return jsonify(tree)

@app.route(wiki_route + "/get-md-files")
def getMDFiles():
    root = request.args.get('root')

    md_files = [f for f in listdir(root) if isfile(join(root, f)) and f.endswith(".md")]

    data = []
    for i in md_files:
        with open(join(root, i), encoding="utf8") as f:
            data.append({
                "content": markdown.markdown(f.read(), extensions=['fenced_code']),
                "filename": os.path.splitext(i)[0],
                "link": "#" + os.path.splitext(i)[0]
            })
            
    return jsonify(data)

@app.route(wiki_route + "/get-images")
def getImages():
    root = request.args.get('root')

    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.jfif', '.webp')
    files = [join(root, f) for f in listdir(root) if isfile(join(root, f)) and f.endswith(extensions)]
            
    return jsonify(files)

@app.route(wiki_route + '/images/<path:filename>')
def getImageFile(filename):
    return send_from_directory("./" + wiki_folder, filename, as_attachment=True)

if __name__ == "__main__":
    app.run()