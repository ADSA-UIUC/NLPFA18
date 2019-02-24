# Application's entry point. Run this file to start the Flask server and launch app


from app import app

if __name__ == '__main__':
    app.run(debug=True)


# Commands to run (BASH):
# export FLASK_APP=run.py
# export FLASK_ENV=development
# flask run

# Extending a Shiny app with Python using Flask:
# https://github.com/ricardovm91/pyshiny
