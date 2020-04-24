import subprocess
from web_scripts import *
from conversions import *
import math
import os
import time

def convert_time(time):
    """
    This function converts time in a form of integers to a hh:mm:ss format
    Returns an array | Ex: 01:32:34
    """
    time_list = [60*60,60,1]
    output_list = []

    for i in time_list:
        amount, remainder = divmod(time, i)
        if len(str(amount)) < 2:
            output_list.append(f'0{str(amount)}')
        else:
            output_list.append(str(amount))
        time = remainder
    return ':'.join(output_list)

def clean_file(string):
    """
    This function cleans out unnecessary characters from subprocess.Popen() outputs.
    If an output is a numerical value, it will round it down and return same else
    it will return the string value
    """
    keep_list = [str(num) for num in range(0,10)] + ['.','x']
    for char in string:
        if char not in keep_list:
            string = string.replace(char, "")
    try:
        return math.floor(float(string))
    except:
        return string

def cleanup():
    """
    This function uses os.remove() to clean out all the temoprary values created from
    our code. Whenever we generate a temporary file, it will have the string "_temp" in front of it.
    Therefore, it will delete files that start with that along with any files copied by the code.
    """
    for file in os.listdir():
        if file[:5] == '_temp':
            os.remove(file)
    try:
        f = open('list.txt','r')
        line = f.readline()[5:-1].rstrip('\n').replace("'","")
        while line:
            os.remove(line)
            line = f.readline()[5:].rstrip('\n').replace("'","")
        f.close()
        os.remove('list.txt')
    except:
        pass

class Media:
    def __init__(self, media_file):
        self.file = media_file

    def __str__(self):
        return self.file

    def duration(self):
        """
        This function uses FFMPEG to parse through a video/music file and returns the duration of the file
        into Python using subprocess.Popen()

        It then calls function clean_file to convert the output into an integer that represents seconds
        Returns an integer | Ex: 251
        """
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {self.file}'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]

        return clean_file(str(output))

    def size(self):
        """
        This function uses FFMPEG to parse through an image/video file and returns the size (width & height) of the file
        into Python using subprocess.Popen()

        It then calls function clean_file to convert the output into integers representing width & height.
        Returns an array of two integers | Ex: [720,320]
        """
        cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=height,width -of csv=s=x:p=0 {self.file}'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]

        size =  clean_file(str(output))
        dimension_list = size.split('x')

        return [int(num) for num in dimension_list]

    def set_size(self, size_list):
        """
        This function uses FFMPEG to set the dimensions of a video/file according to the user's preferences.
        It outputs '_temp' + self.file and points self.file to the newly generated file
        """
        width = size_list[0]
        height = size_list[1]
        cmd = f'ffmpeg -y -i {self.file} -s {width}x{height} -c:a copy {"_temp" + self.file}'
        subprocess.call(cmd.split(' '))

        self.file = f'_temp{self.file}'

    def set_duration(self, duration, target_name=None):
        time = convert_time(duration)

        if target_name:
            cmd = f'ffmpeg -y -ss 00:00:00 -i {self.file} -t {time} -map 0 -vcodec copy -acodec copy {target_name}'
            subprocess.call(cmd.split(' '))
            self.file = target_name
        else:
            cmd = f'ffmpeg -y -ss 00:00:00 -i {self.file} -t {time} -map 0 -vcodec copy -acodec copy {"_temp" + self.file}'
            subprocess.call(cmd.split(' '))
            self.file = '_temp' + self.file

    def loop(self, target_duration):
        curr = self.duration()
        repeat = math.ceil(target_duration/curr)
        f = open('list.txt','w')
        for i in range(repeat):
            f.write(f"file '{file_types(self.file)[1]}{i}.{file_types(self.file)[0]}'\n")
            #make sure to change depending on operating system
            cmd = f'copy {self.file} {f"{file_types(self.file)[1]}{i}.{file_types(self.file)[0]}"}'
            subprocess.call(cmd.split(' '), shell=True)
        f.close()
        time.sleep(1)
        cmd = f'ffmpeg -y -f concat -safe 0 -i list.txt -c copy {"_temp" + self.file}'
        subprocess.call(cmd.split(' '))
        self.file = '_temp' + self.file

    def overlay(self, video, image):
        cmd = f'ffmpeg -y -i {image} -i {video} -filter_complex [1:v]colorkey=0x000000:0.5:0.5[ckout];[0:v][ckout]overlay[out] -map [out] -c:a copy -c:v libx264 {"_temp" + video}'
        subprocess.call(cmd.split(' '))
        self.file = "_temp" + video
