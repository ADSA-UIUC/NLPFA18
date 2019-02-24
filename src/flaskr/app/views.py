# Contians all the routs for application


from flask import render_template, request, jsonify, session
from app import app
from website_interface import WebsiteInterface


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
        interface = WebsiteInterface('people.json')
        posts = interface.get_n_random_forum_posts()
        print(posts)
        return jsonify(posts)

@app.route('/testcomplete', methods=['GET', 'POST'])
def testcomplete():
    if request.method == 'POST':
        print("in testcomplete")
        groupings = request.get_json() # form['groupings']
        print('groupings: ', groupings)
        interface = WebsiteInterface('people.json')
        results = {} #interface.get_actual_groupings(data)
        response_data = {
            'placeholder' : 'group data',
            'results' : results
        }
        return jsonify(response_data)

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
