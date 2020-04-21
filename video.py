from moviepy.editor import *
from moviepy.video.fx.all import fadein, loop
from conversions import add_music
import random
import math

class Generator:
    def __init__(self, video, music, overlay='assets/grainoverlay.mp4'):
        self.video = video
        self.music = music
        self.overlay = overlay

    def generate_overlay(self):
        #setting overlay_duration as the duration of the music
        overlay_duration = self.video.duration
        #initializing overlay, resizing, and setting opacity
        overlay = self.overlay.subclip().resize(self.video.size).set_opacity(0.50)
        #loops overlay if it is too short
        if overlay.duration < overlay_duration:
            overlay = loop(overlay, duration=overlay_duration)
        else:
            overlay = overlay.set_duration(overlay_duration)
        return overlay

    def shuffle(self):
        #cutting the first and last 5 seconds to prevent using intro & outro clips
        overlay = self.generate_overlay()
        video = self.video.subclip(5, math.floor(self.video.duration) -5)
        clip = []
        curr = 0
        while curr < video.duration:
            #ends loop to prevent adding nonexistent clips
            if video.duration - curr <= 8:
                clip.append(CompositeVideoClip([video.subclip(curr, video.duration),
                                                overlay.subclip(curr, video.duration)]))
                break
            else:
                #generate random cut length
                cut = random.randint(3,5)
                sub = video.subclip(curr, curr + cut)
                sub = CompositeVideoClip([sub, overlay.subclip(curr, curr + cut)])
                #adds fade in transition if cut > 3
                if cut > 3:
                    sub = fadein(sub,3)
                clip.append(sub)
                curr += cut
        #shuffles the index in-place by switching current index with random index
        for index in range(len(clip)):
            rand_index = random.randint(0, len(clip) - 1)
            clip[index], clip[rand_index] = clip[rand_index], clip[index]
        #combining invidual clips into video
        final = concatenate_videoclips(clip).set_duration(self.music.duration)

    def create(self):
        final = CompositeVideoClip([self.shuffle(), self.generate_overlay()])
        final.write_videofile('output.mp4', audio=False)
        self.music.close()
        self.video.close()
        self.overlay.close()







