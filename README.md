LunaVisualiser.py - An audio visualiser built in Python
=======================================================

## DESCRIPTION

LunaVisualiser is a work-in-progress audio visualiser that allows the user to monitor specific frequencies and amplitudes of live audio.

Each of these monitors can then be assigned or passed to generic visualiser modules - to be written at a later date.

My initial inspiration for creating this project was to replicate visualisers I had previously written in Processing, and to see if it was possible to duplicate the effect with a more powerful and varied language such as Python.

## INSTALLATION

LunaVisualiser currently uses the following python libraries:

* opengl
* pyaudio
* numpy
* aubio
* psutil
* pymad
* pyao

And you can install all of these in Ubuntu using this handy single line:

    sudo apt-get install python-opengl python-pyaudio python-numpy python-aubio python-psutil python-pymad python-pyao

## USAGE

To start the visualiser, enter the following on the command line:

    python LunaVisualiser.py
