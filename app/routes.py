from flask import render_template, request, redirect, url_for, send_from_directory, jsonify, make_response, flash, Markup
import os
from werkzeug.utils import secure_filename
from web_scripts import *

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/upload-music', methods = ['GET', 'POST'])
def upload_music():
    impulse_list = []

    if request.method == 'POST':
        if request.files:
            #checking for file size using data from cookies
            if not allowed_filesize(request.cookies.get('filesize')):
                print('File exceeded maximum size')
                return redirect(request.url)

            music = request.files["music"]
            impulse = request.cookies.get('user_choice')
            impulse = f'/{impulse}.wav'

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
                filename = "".join(secure_filename(music.filename).split(' '))
                #saving uploaded music into directory
                music.save(os.path.join(app.config["MUSIC_UPLOADS"],filename))
                print('{} Saved'.format(filename))

                #applying reverb algorithm
                path = build_reverb(filename, impulse)
                print(path)

                #downloads the slowed & reverbed file
                return send_from_directory(app.config['MUSIC_UPLOADS'], path, as_attachment=True)

        else:
            url = request.get_json()['url']
            #downloading file from youtube
            try:
                filename = get_music(url)
                impulse = f'/{request.cookies.get("user_choice")}.wav'
                path = build_reverb(filename, impulse)
                return make_response(jsonify({'message':path}), 200)

            except:
                return make_response(jsonify({'message':'Please enter a valid URL'}), 300)

    return render_template('upload_music.html')


@app.route("/upload-video", methods=['GET','POST'])

def upload_video():
    if request.method == 'POST':

        filesize = request.cookies.get("filesize")
        file = file.get_json()
        print(file)
        print(filesize)
        print(file)

        res = make_response(jsonify({"message":f"{file.filename} uploaded"}), 200)
        return res

    return render_template('test.html')











