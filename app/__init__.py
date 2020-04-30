from flask import Flask

app = Flask(__name__)
TEMPLATES_AUTO_RELOAD=True
app.config["MUSIC_UPLOADS"] = '/mnt/c/Users/Philip/Documents/GitHub/slowandreverbed/app/static/music/uploads'
app.config['ALLOWED_MUSIC_EXTENSIONS'] = ['WAV','MP3']
app.config['MAX_IMAGE_FILESIZE'] = 1024*1024*50*8
app.config['IMPULSES'] = '/mnt/c/Users/Philip/Documents/GitHub/slowandreverbed/impulses'
app.config['IMAGE_UPLOADS'] = '/mnt/c/Users/Philip/Documents/GitHub/slowandreverbed/app/static/assets/images'
app.config['OVERLAY_UPLOADS'] = '/mnt/c/Users/Philip/Documents/GitHub/slowandreverbed/app/static/assets/overlays'
app.config['GIF_UPLOADS'] = '/mnt/c/Users/Philip/Documents/GitHub/slowandreverbed/app/static/assets/gifs'

from app import routes
