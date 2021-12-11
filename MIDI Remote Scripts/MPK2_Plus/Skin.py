#
#   Skin.py
#   Define Ableton skin - maps Ableton actions to pad colors
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from .Colors import MPK2PadColors, MPK2PadBlinkColors

class Colors:

    class Session:
        # Clip
        ClipEmpty = MPK2PadColors.BLACK
        ClipStopped = MPK2PadColors.ORANGE

        # Clip playing
        ClipTriggeredPlay = MPK2PadBlinkColors.YELLOW_GREEN
        ClipStarted = MPK2PadBlinkColors.GREEN

        # Clip recording
        RecordButton = MPK2PadColors.RED
        ClipTriggeredRecord = MPK2PadBlinkColors.HOT_PINK
        ClipRecording = MPK2PadColors.RED_BLINK

        # Clip stopping row
        StopClip = MPK2PadColors.RED
        StopClipTriggered = MPK2PadBlinkColors.RED
        StoppedClip = MPK2PadColors.BLACK

        # Scene column
        NoScene = MPK2PadColors.BLACK
        Scene = MPK2PadColors.GREEN
        SceneTriggered = MPK2PadBlinkColors.GREEN

    class DrumGroup:
        # pads with no sound on them
        PadInvisible = MPK2PadColors.BLACK
        PadEmpty = MPK2PadColors.BLACK

        # pads not pressed
        PadFilled = MPK2PadColors.ORANGE
        PadSoloed = MPK2PadColors.LT_BLUE
        PadMuted = MPK2PadColors.YELLOW
        
        # pads being pressed
        PadSelected = MPK2PadColors.RED
        PadSoloedSelected = MPK2PadColors.HOT_PINK
        PadSelectedNotSoloed = MPK2PadColors.BLUE
        PadMutedSelected = MPK2PadColors.BLACK

def make_default_skin():
    return Skin(Colors)