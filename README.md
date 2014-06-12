Capstone Design Project - Jennifer Schror & John Moffitt

A moving platform consisting of a servomotor, load sensors, and an arduino aids in physical therapy for the wrist. See pptx for more info and pics.

Arduino code:

This backend initializes serial connection. Controls servomotor position and consistently polls for load sensor values. Also converts data read from Python in order to interface correctly.

Python code:

GUI created with wxPython allows user to initialize exercise test.  The user is instructed to move the platform by increasing and decreasing palm pressure.