# Contians all the routs for application


from flask import render_template, request, jsonify, session
from app import app
from website_interface import WebsiteInterface
import json


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

@app.route('/explore')
def explore():
    return render_template("explore.html")

@app.route('/testinit')
def testinit():
    return render_template("tester.html")

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        posts = Explorer.before()
        return jsonify(posts)

@app.route('/testcomplete', methods=['GET', 'POST'])
def testcomplete():
    if request.method == 'POST':
        json_groups = request.form['groupings']
        groupings = json.loads(json_groups)
        results = Explorer.after(groupings)
        response_data = {
            'placeholder' : 'group data',
            'results' : results
        }
        return jsonify(response_data)

class Explorer():
    interface = WebsiteInterface('people.json')

    def __init__(self):
        pass

    def before():
        return Explorer.interface.get_n_random_forum_posts()

    def after(groupings):
        return Explorer.interface.get_actual_groupings(groupings)

#
# from flask import request
#
# @app.route('/explore/go', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         f = request.files['the_file']
#         f.save()
#
#     request.get_json()
