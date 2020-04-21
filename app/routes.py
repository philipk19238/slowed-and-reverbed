from flask import render_template, request, redirect, url_for, send_from_directory
from app import app
import os
from werkzeug.utils import secure_filename
from web_scripts import *

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/upload-music', methods = ['GET', 'POST'])
def upload_music():
    if request.method == 'POST':
        if request.files:
            #checking for file size using data from cookies
            if not allowed_filesize(request.cookies.get('filesize')):
                print('File exceeded maximum size')
                return redirect(request.url)

            music = request.files["music"]

            if music.filename == "":
                #checking for blank filenames
                print('Music must have a filename')
                return redirect(request.url)

            if not allowed_file(music.filename):
                #checking for invalid extensions
                print('Invalid Music Extension')
                return redirect(request.url)

            else:
                #checking for malicious filenames
                filename = secure_filename(music.filename)

                #saving uploaded music into directory
                music.save(os.path.join(app.config["MUSIC_UPLOADS"],filename))
                print('{} Saved'.format(filename))

                #applying reverb algorithm
                path = build_reverb(filename)

                #downloads the slowed & reverbed file
                return send_from_directory(app.config['MUSIC_UPLOADS'], path, as_attachment=True)

    return render_template('upload_music.html')




