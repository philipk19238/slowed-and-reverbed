import os
from conversions import *
from reverb import Reverb
from app import app

def file_types(filename):
    '''
    This function checks for the file type by looping over filename
    in reverse and returning the text of everything behind the "."

    Returns a string value indicating file type (Ex: 'wav', 'mp3')
    and a string value indicating file name (Ex: 'travis_scott', 'harry_styles')
    '''

    for index in range(len(filename)):
        if filename[::-1][index] == '.':
            break
    return filename[-index:], filename[:-index-1]

def allowed_file(filename):
    '''
    This function checks for incorrect file types and names
     -> Files without "."
     -> Files without names | Ex: ".wav"
     -> Files that have incorrect extensions

     Returns a boolean value
    '''

    if not '.' in filename:
        return False

    elif len(filename) <= 4:
        return False

    else:
        if file_types(filename)[0].upper() not in app.config['ALLOWED_MUSIC_EXTENSIONS']:
            return False

    return True

def allowed_filesize(filesize):
    '''
    This function determines whether or not the uploaded
    file is too big

    Returns a boolean value
    '''
    if int(filesize) <= app.config['MAX_IMAGE_FILESIZE']:
        return True

    return False

def build_reverb(filename, impulse='/French 18th Century Salon.wav'):
    '''
    This function slows & reverbs the music file that the user uploaded.

    As it uses scipy to generate the reverb effects, the input file needs to be
    a '.wav' extension. Therefore, we check to see if the extension is a '.wav' and
    will convert it into one if it is not.

    After the revised song is generated, we delete the original upload and any converted files.

    Returns a string | Ex: 'travis_scottslowed_reverbed.mp3', 'harry_stylesslowed_reverbed.mp3'
    '''
    extension, name = file_types(filename)
    song = "{}/{}".format(app.config['MUSIC_UPLOADS'], filename)

    #convert to WAV if file was MP3
    if extension.upper() != 'WAV':
        convert_wav('{}/{}'.format(app.config['MUSIC_UPLOADS'], name))
        song = '{}/{}{}'.format(app.config['MUSIC_UPLOADS'], name, '.wav')

    #generating reverb file
    reverb = Reverb(song, app.config['IMPULSES'] + impulse).export()

    #removes user uploaded file and converted file
    os.remove(song)

    try:
        os.remove('{}/{}'.format(app.config['MUSIC_UPLOADS'], filename))
    except:
        pass

    return '{}slowed_reverbed.mp3'.format(name)


