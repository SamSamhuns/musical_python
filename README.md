# musical_python

[![Updates](https://pyup.io/repos/github/SamSamhuns/musical_python/shield.svg)](https://pyup.io/repos/github/SamSamhuns/musical_python/)
[![Python 3](https://pyup.io/repos/github/SamSamhuns/musical_python/python-3-shield.svg)](https://pyup.io/repos/github/SamSamhuns/musical_python/)

Creating music though LSTM Recurrent Neural Networks.

<img src='img/laptop-macbook-apple-table-music-technology-1079002-pxhere.com.jpg'></img>

## Installation and setup

```bash
$ python -m pip install --upgrade pip
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Starting Django Server

-   Compile the `abc2midi` executable to convert abc notation files to midi

```shell
# change to top directory (`musical_python/`)
$ cd abcmidi
$ make
$ mv ./abc2midi ../
```

-   Migrate and start Django server

```shell
$ python manage.py migrate
$ python manage.py runserver
```

The application can now be accessed through the localhost.

**Important Note:** To make sure the midi files are playable, the <http://www.midijs.net/lib/midi.js> file must be allowed to run on the browser.

### Optional

**Midi web scraping information:** Pop music midi files are available in the data folder but to download midi files from other genres, use `python scrap_midi/ ./scrap_freemidi_org.py <genre> <Headless State 1/0>`

**Note:** Only for Chrome users:

For web scraping midi files with selenium, download ChromeDriver for the appropriate Chrome version here <https://sites.google.com/a/chromium.org/chromedriver/downloads> and save it to the `scrap_midi` folder.

_The author not be responsible for any issues with Copyright Infrigements that might come with downloading of midi files._

## Acknowledgements and References

<small>

-   I claim no rights to the abcmidi package. It was created by <a href='https://leesavide.github.io/'>leesavide</a> and is available at <https://github.com/leesavide/abcmidi>.
-   Classicial music ABC notation from the ABC version of the Nottingham Music Database maintained by James Allwright <http://abc.sourceforge.net/NMD/>
-   Midi sound samples for pop genre downloaded from <https://freemidi.org>
-   LSTM Networks inspired from Gaurav Sharma's GitHub repository
-   ABC music foundation for its documentation
-   Medium: Neural Nets for Generating Music: <https://medium.com/artists-and-machine-intelligence/neural-nets-for-generating-music-f46dffac21c0>
-   Medium: How to Generate Music using a LSTM Neural Network in Keras <https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5>
-   Website design acquired under a free open source license from <http://w3layouts.com>
-   Headline image under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication <https://pxhere.com/en/photo/1079002>
-   Background Photo credit: Rakutaro Ogiwara. Licensed under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication <https://www.flickr.com/photos/arselectronica/36350783815>

</small>
