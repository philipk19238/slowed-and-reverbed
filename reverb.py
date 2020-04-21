from scipy.io.wavfile import read, write
from scipy import signal
import numpy as np
import subprocess
from conversions import convert_wav, convert_mp3, find_name

class Reverb:

    def __init__(self, music, impulse='impulses/French 18th Century Salon.wav'):
        self.music_location = music
        self.impulse_location = impulse
        self.read_rate = None

    def import_music(self):
        """
        This function reads in a '.wav' song and converts it into
        a numpy array with values between 1 and 0

        Returns an array | Ex: [[0,0.23,.95],[0.82,0.25,0.22]]
        """
        audio = read(self.music_location)
        audio_arr =  np.array(audio[1], dtype='float')
        #sets the sample rate as a class variable
        self.read_rate = audio[0]
        return audio_arr

    def import_impulse(self):
        """
        This function reads in a '.wav' impulse and converts it into
        a numpy array.

        Afterwards, it standardizes the array to values between 1 and 0

        Returns a multi-dimensional array | Ex: [[0,0.23,.95],[0.82,0.25,0.22]]
        """
        impulse = read(self.impulse_location)
        impulse_arr =  np.array(impulse[1], dtype='float')
        impulse_arr = np.multiply(impulse_arr, 1.0/np.max(impulse_arr))
        return impulse_arr

    def convert_reverb(self):
        """
        This function reads in the numpy arrays of both the song and the impulse.

        It then uses Fast Fourier Transform to convolve the two arrays, thus generating
        the reverb effect.

        Afterwards, it normalizes the array to values between 1 and 0

        Returns a multi-dimensional array | Ex: [[0,0.23,.95],[0.82,0.25,0.22]]
        """
        music = self.import_music()
        impulse = self.import_impulse()
        filtered = signal.convolve(music, impulse, mode='same', method='fft')
        filtered = np.multiply(filtered, 1.0/np.max(np.abs(filtered)))
        return filtered

    def export(self):
        """
        This function converts the convolved array into a WAV file and slows down
        the sample rate by 10%.

        It then converts the WAV file into an MP3 file using FFMPEG
        """
        final = self.convert_reverb()
        music_name = find_name(self.music_location)
        write(music_name + '.wav', rate=int(self.read_rate * 0.9), data=final)
        #addes 'slowed_reverbed' to song name
        convert_mp3(music_name, 'slowed_reverbed')

