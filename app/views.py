from app import app
from flask import render_template, request
import os

app.config['UPLOAD_FOLDER'] = 'app/static/csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csvfile = request.files['csvfile']
        print(csvfile)
        if csvfile.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], csvfile.filename)
            csvfile.save(filepath)


    return render_template("index.html")