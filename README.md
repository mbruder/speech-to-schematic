speech-to-schematic
===================

This code intends to solve the problem of finding components in schematics (in PDF) we export 
from Altium using speech recognition.

Usage
-----

You must have one PDF opened with Preview. 
Write at the terminal: 
python speech_to_find.py
You'll have a few seconds until it says "* done recording" to say what you want to look for.

Configuration
-------------

Changelog
---------

[+] Remove hard coded variables
[+] Add function to parse Google's response.

Credits
-------
Main functions are based in jeysonmc / python-google-speech-scripts.