import subprocess

def convert_wav(musicName, add_title=None):
    """
    This function converts a MP3 file to a WAV file using FFMPEG

    It also has the option of adding text to the converted file
    """
    cmd = f"ffmpeg -i {musicName}.mp3 -vn -ar 44100 -ac 2 -b:a 192k {musicName}.wav"
    if add_title:
        cmd = f"ffmpeg -i {musicName}.mp3 -vn -ar 44100 -ac 2 -b:a 192k {musicName + add_title}.wav"
    subprocess.call(cmd.split(' '))

def convert_mp3(musicName, add_title=None):
    """
     This function converts a WAV file to a MP3 file using FFMPEG

     It also has the option of adding text to the converted file
    """
    cmd = f"ffmpeg -i {musicName}.wav -vn -ar 44100 -ac 2 -b:a 192k {musicName}.mp3"
    if add_title:
        cmd = f"ffmpeg -i {musicName}.wav -vn -ar 44100 -ac 2 -b:a 192k {musicName + add_title}.mp3"
    subprocess.call(cmd.split(' '))

def find_name(file):
    """
    This function returns the name of the file without an extension

    Returns a string | Ex: 'travis_scott'
    """
    for index in range(len(file)):
        if file[::-1][index] == '.':
            index += 1
            break
    return file[:-index]

def add_music(video_file,music_file):
    """
    This function combines video and audio using FFMPEG
    """
    output_file = find_name(music_file) + '_slow_and_reverbed.mp4'
    cmd = f'ffmpeg -y -i {video_file} -i {music_file} -c copy -map 0:v:0 -map 1:a:0 {output_file}'
    subprocess.call(cmd.split(' '))
