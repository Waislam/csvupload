from app import app
from flask import render_template, request, send_file
import os
from vsf.vsf3 import Appointment

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

@app.route('/run', methods = ['GET'])
def run():
    bot = Appointment()
    bot.run()
    return "bot is running"

