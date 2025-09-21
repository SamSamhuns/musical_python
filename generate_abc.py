# The make model and generate sequence functions are derived from the repo at
# https://github.com/gauravtheP/Music-Generation-Using-Deep-Learning
# The newer models independent of this original repo will consist of genre wise music generation
# And a model with a deeper layers
from tensorflow.keras.layers import LSTM, Dropout, Dense, Activation, Embedding
from tensorflow.keras.models import Sequential
import numpy as np
import os
import json


CHAR_INDEX_JSON_PATH = "static/json/char_to_index.json"


def make_model(unique_chars):
    model = Sequential()

    model.add(Embedding(input_dim=unique_chars, output_dim=512, input_length=1))

    model.add(LSTM(256, return_sequences=True, stateful=True))
    model.add(Dropout(0.2))

    model.add(LSTM(256, return_sequences=True, stateful=True))
    model.add(Dropout(0.2))

    model.add(LSTM(256, stateful=True))
    model.add(Dropout(0.2))

    model.add((Dense(unique_chars)))
    model.add(Activation("softmax"))

    return model


with open(os.path.join(CHAR_INDEX_JSON_PATH)) as f:
    char_to_index = json.load(f)
index_to_char = {i: ch for ch, i in char_to_index.items()}
unique_chars = len(index_to_char)

# backend.clear_session()
model = make_model(unique_chars)
model.build(input_shape=(1, 1))
model.load_weights("static/weights/Weights_90.h5")


def generate_sequence(initial_index, seq_length):
    sequence_index = [initial_index]

    for _ in range(seq_length):
        batch = np.zeros((1, 1))
        batch[0, 0] = sequence_index[-1]

        predicted_probs = model.predict_on_batch(batch).ravel()
        sample = np.random.choice(range(unique_chars), size=1, p=predicted_probs)

        sequence_index.append(sample[0])
    seq = "".join(index_to_char[c] for c in sequence_index)

    cnt = 0
    for i in seq:
        cnt += 1
        if i == "\n":
            break
    seq1 = seq[cnt:]

    cnt = 0
    for i in seq1:
        cnt += 1
        if i == "\n" and seq1[cnt] == "\n":
            break
    seq2 = seq1[:cnt]

    return seq2


def generate_abc_file(ar, ln, instrument_code):
    """
    ar = Any number between 0 to 86 which will be given as initial character to model for generating sequence
    ln = The length of generated music sequence. Typical number is between 300-600. Too small number will generate hardly generate any sequence
    instrument_code = The instrument code is detailed in static/csv/abcmidi_instrument_name
    """
    ar = max(ar % 87, 0)
    ln = max(ln, 600)
    instrument_code = max(instrument_code % 129, 1)

    music = generate_sequence(ar, ln)
    print("Music sequence generated:")

    with open("static/abc/generated.abc", "w") as abc:
        if music.find("X:") == -1:
            abc.write("X:1\n")
        if music.find("T:") == -1:
            abc.write("T:RNN generated\n")
        if music.find("M:") == -1:
            abc.write("M:3/4\n")
        if music.find("L:") == -1:
            abc.write("L:1/8\n")
        if music.find("Q:") == -1:
            abc.write("Q:1/4=120\n")
        if music.find("W:") == -1:
            abc.write("W:Generated music\n")
        if music.find("K:") == -1:
            abc.write("K:C\n")
        abc.write(f"%%MIDI program {instrument_code}\n")
        abc.write(music)
