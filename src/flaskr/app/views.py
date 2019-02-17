# Contians all the routs for application


from flask import render_template
from app import app


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
