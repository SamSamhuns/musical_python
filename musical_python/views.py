from django.shortcuts import render
from django.contrib import messages

import generate_abc
import subprocess
import random
import os


def home(request):
    return render(request, "main/index.html")


def instruments(request):
    return render(request, "main/instruments.html")


def references(request):
    return render(request, "main/references.html")


def abc_to_midi(abc_file: str, midi_file: str = "static/midi/music.midi") -> None:
    """Convert abc to midi"""
    os.makedirs(os.path.dirname(midi_file), exist_ok=True)
    cmd = ["./abc2midi", abc_file, "-o", midi_file]
    subprocess.run(cmd, check=True)


def submit(request):
    """Func called after Form Submit button to convert abc to midi and play it"""
    starting_seq = random.randint(0, 87)
    duration = {"1": 500,"2": 700,"3": 900}.get(request.POST["duration"], random.randint(500, 900))
    instrument = int(request.POST["instrument"])

    generate_abc.generate_abc_file(starting_seq, duration, instrument)

    abc_to_midi("static/abc/generated.abc")
    messages.success(
        request, "You can press PLAY now! (You might have to press PLAY twice)"
    )
    return render(request, "main/index.html", {"random_number": random.randint(0, 1e9)})
