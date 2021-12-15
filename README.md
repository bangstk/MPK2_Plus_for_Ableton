# Enhanced Ableton Integration for Akai MPK2: MPK249 and MPK261, by bangstk

SCRIPT IN DEVELOPMENT - NOT ALL FEATURES WORK YET - STAY TUNED

Akai MPK2 owners will note that the out-of-the-box Ableton integration with their keyboard is fairly lackluster, offering nothing more than pan knobs and faders mapped for 8 tracks only. Most of the keyboard's features are not utilized with the Ableton built-in MPK2 support.

I am developing Ableton control scripts which hopefully make these keyboards much more useful in the Ableton workflow, by implementing session box on pads and knob/button output selection that are offered by newer controllers that have Ableton integration.

These scripts were made for Ableton 10 and should work with 11.

# Implemented Features:
- Support for MPK249 and MPK261
- See and control your Ableton Session on the 4x4 colored pads grid Bank A and DAW Control nav buttons
- Transport buttons
- All 3 Control Banks of the Mixer section are now automapped for control of up to 24 tracks or macros/parameters
    - Faders mapped to Volume
    - Mixer buttons mapped to Arming
    - Knobs mapped to Macros/Parameters
        - Knobs now properly work as infinite scrollers, like Push
        - Control the additional paramaters in Ableton 11's 16 Macro racks by using Bank B
        - Use Bank B and C to control up to 24 parameters, for example when bluehanding a VST with many parameters mapped out in the Ableton instrument rack


# Features In Development:
- Support for MPK225
- Drum Rack accessible through Pads Bank D
- Dedicated Master Volume fader on the rightmost fader
- Select whether mixer buttons do Arm, Solo, Mute, or Select
- Select whether knobs do Pan, Sends A-D, or Macros
- See which button and knob modes are active right on the MPK2's screen

# Installation:
Follow Ableton's instructions for script installation: https://help.ableton.com/hc/en-us/articles/209072009-Installing-third-party-remote-scripts

In Ableton's MIDi settings, select "MPK2_Plus_MPK249" instead of the default "MPK249" device to use this script.

On your MPK2, use the built-in Bitwig preset! This script is created for that mapping only. Do not use the LiveLite preset.

# Thanks To...

Thanks to the Ableton Live Scripts decompilation project.
https://github.com/gluon/AbletonLive10.1_MIDIRemoteScripts

All of my code was written using the MIDI Control Scripts from there as a reference for how the Ableton _Framework works.

# Help me out!
I'm not yet a great performer, so I am seeking feedback from anyone who has any ideas on what could help their workflow if it is not listed above.
Feel free to make suggestions in the Issues tab.

I have ideas for mapping the MPK225 well for extra functionality, but I do not have one to test with. If anyone has one and is willing to be a guinea pig, contact me and I will get this script running on MPK225 in short order.