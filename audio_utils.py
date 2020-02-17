# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:49:31 2020

@author: Sean Nichols

audio_utils build on the speech_recognition, jellyfish, and difflib for
comparing audio with predetermined sets of words/phrases
"""

from word2number import w2n
from difflib import get_close_matches
from jellyfish import soundex
import speech_recognition as sr

def listen():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    
    try:
        sound = r.recognize_google(audio)
    except:
        sound = []
    
    return sound

def match_to_lib(sound, sound_lib):
    
    # Find the closest match of numbers 1-10
    n_closest = get_close_matches(sound, sound_lib, 1)
    
    # No direct match from the sound_lib
    #  Check if the sound "sounds like" any lib sounds 
    if not n_closest:
        
        # Convert the sounds into what they sound like
        sound_lib_ex = [soundex(x) for x in sound_lib]
        sound_ex = soundex(sound)
        
        # Find the closest match for "sounds like"
        closest_sound = get_close_matches(sound_ex, sound_lib_ex, 1)
        
        # Sounds like something in the sound_lib
        if closest_sound:
            closest_sound = closest_sound[0]
            n_closest = sound_lib[sound_lib_ex.index(closest_sound)]
            
        # Doesn't sound like anything in sound_lib
        else:
            n_closest = []
    else:
        n_closest = n_closest[0]
        
    return n_closest

def collect_sounds(n_coms=1):
    
    print('Ready for {} sound(s)'.format(n_coms))
    commands = []
    
    for com in range(n_coms):
        
        print('Listening for sound: {}/{}'.format(com + 1, n_coms))
        c = listen()
        if c:
            commands.append(c)
        else:
            print('Did not hear sound {}'.format(com + 1))
        
    return commands
    
def set_n_commands():
    
    c_full = listen()
    n_com = c_full.split()[0]
    
    # If the first word is interpreted as a written number
    if not n_com.isdigit():
        n_lib = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        
        # Match sound to provided sound library
        n_closest = match_to_lib(n_com, n_lib)
        
        if n_closest:
            n_coms = w2n.word_to_num(n_closest)
        else:
            print('No number match found for command "{}"'.format(c_full))
            return
    # First number interpreted as a digit (str)
    else:
        n_coms = int(n_com)
    
    collect_sounds(n_coms=n_coms)  
    




