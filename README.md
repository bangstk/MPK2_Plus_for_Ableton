# Enhanced Ableton Integration for MPK249 by bangstk

SCRIPT IN DEVELOPMENT - NOT ALL FEATURES WORK YET - STAY TUNED

Akai MPK2 owners will note that the out-of-the-box Ableton integration with their keyboard is fairly lackluster, offering nothing more than pan knobs and faders mapped for 8 tracks only. Most of the keyboard's features are not utilized with the Ableton built-in MPK2 support.

I am developing Ableton control scripts which hopefully make these keyboards much more useful in the Ableton workflow, by implementing session box on pads and knob/button output selection that are offered by newer controllers that have Ableton integration.

These scripts were made for Ableton 10 and should work with 11.

# Implemented Features:
- See and control your Ableton Session on the 4x4 colored pads grid Bank A and DAW Control nav buttons

# Features In Development:
- Support for MPK225 and MPK261
- Drum Rack accessible through Pads Bank D
- Dedicated Master Volume fader on the rightmost fader
- Select whether mixer buttons do Arm, Solo, Mute, or Select
- Select whether knobs do Pan, Sends A-D, or Macros
- Knobs are infinite scrollers a la Push
- See which button and knob modes are active right on the MPK2's screen

# Installation:
Follow Ableton's instructions for script installation: https://help.ableton.com/hc/en-us/articles/209072009-Installing-third-party-remote-scripts

In Ableton's MIDi settings, select "MPK2_Plus_MPK249" instead of the default "MPK249" device to use this script.

On your MPK2, use the built-in Bitwig preset! This script is created for that mapping only. Do not use the LiveLite preset.

# Thanks To...

Thanks to the Ableton Live Scripts decompilation project.
https://github.com/gluon/AbletonLive10.1_MIDIRemoteScripts

All of my code was written using the MIDI Control Scripts from there as a reference for how the Ableton _Framework works.
