from django.shortcuts import render
from django.contrib import messages

import generate_abc
import subprocess
import random
import os

os.system('chmod u+rwx abc2midi')  # Make abc2midi executable

# Create your views here.


def home(request):
    return render(request, 'main/index.html')


def instruments(request):
    return render(request, 'main/instruments.html')


def references(request):
    return render(request, 'main/references.html')


def abc_to_midi(abc_file):
    '''Convert abc to midi'''
    cmd = "./abc2midi " + abc_file + " -o static/midi/music.midi"
    subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                     stdout=subprocess.PIPE)


def submit(request):
    '''Func called after Form Submit button to convert abc to midi and play it'''
    instrument = request.POST['instrument']
    duration = request.POST['duration']
    starting_seq = random.randint(0, 87)

    if duration == '1':
        duration = 500
    elif duration == '2':
        duration = 700
    elif duration == '3':
        duration = 900
    else:
        duration = random.randint(500, 900)

    generate_abc.generate_abc_file(starting_seq, duration, int(instrument))

    abc_to_midi("static/abc/generated.abc")
    messages.success(
        request, 'You can press PLAY now! (You might have to press PLAY twice)')
    return render(request, 'main/index.html')
