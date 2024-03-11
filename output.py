#!/usr/bin/env python3

import sys     # to get argc
import time    # to use sleep()
import socket  # to get host name

from ev3dev2.display import Display
from PIL             import Image  # to load the image
from ev3dev2         import fonts
from ev3dev2.sound   import Sound
from ev3dev2.led     import Leds

### Works both in console and started from the brick.
### Main def. based on docs.python.org/fr/3/library/__main__.html
 
# Applying usual naming conventions
#  (cf python.org/dev/peps/pep-0008/#naming-conventions):
# * class names uses upper case to separate words,
# * variable names are all in lower case, words separated by _,
# * function and method names are like variables.

# === This class is for the robot output =============================

class RobotOutput:
    """Handles the output (image or text and sound) of the robot."""

    # --- Constructor ------------------------------------------------
    def __init__(self, noise):
        """Defines output to text or brick display, according to
           the arguments (arguments -> console = text), 
           and speak only if noise is true or argument = 'n'.

           :param bool noise:    speech output (True) or silent.
        """
        self.display  = Display()
        self.sound    = Sound()
        self.leds     = Leds()
        self.text_out = (len(sys.argv) > 1)
        self.font     = fonts.load('helvR14')
        self.noisy    = noise or ( self.text_out
                                   and (sys.argv[1] == 'n') )
        
    # --- Ouput method -----------------------------------------------
    def new_output(self, text, name, msg) -> None:
        """ Prints a text on console or the image of given name
            in the display, and tells the message if not silent. 

           :param str text:  the text printed if in console.
           :param str name:  the displayed image's name otherwise.
           :param str msg:   the message told if not silent.
        """
        if (self.text_out):
            print(text)
        else:
            self.display.image.paste( Image.open('/home/robot/images/'
                                                 +name+'.bmp'),
                                      (0, 0) )
            self.display.update()

        if (self.noisy):
            self.sound.speak(msg)
        
    # --- Text only ouput method -------------------------------------
    def new_text(self, text, pos=(0,0), speak=False) -> None:
        """ Prints a text either on console or in display
            (depending on the object creation), at given position
            in pixels if in display, and tells the text if speak
            is true and the object not silent.

           :param str text:  the text to print.
           :param tuple(float,float) pos:  the position in pixels.
           :param bool speak:  wether to tell the text or not.
        """
        
        if (self.text_out):
            print(text)
        else:
            self.display.clear()
            self.display.text_pixels(text, True, pos[0], pos[1])
            self.display.update()

        if (self.noisy and speak):
            self.sound.speak(text)

    # --- Setting leds -----------------------------------------------
    def set_leds(self, right_color, left_color) -> None:
        """Sets the leds to the given colors.

           :param str right_color:  the right led's color.
           :param str left_color:   the left led's color.
        """
        self.leds.set_color('RIGHT', right_color)
        self.leds.set_color('LEFT',  left_color)

    # --- Flashing leds ----------------------------------------------
    def flash_leds(self, color, leds=('LEFT', 'RIGHT'), block=False,
                   duration=5, timestep=0.5) -> None:
        """Turns the indicated leds on/off with color every timestep
           seconds for duration seconds (or forever if duration is 
            None), and waits (?) for the end of the animation if block
           is True or returns immediately.

           :param str   color:     the leds' color.
           :param str   leds:      the leds concerned.
           :param bool  block:     wait for the end of the animation?
           :param float duration:  duration of the animation.
           :param float timestep:  duration of each cycle.
        """
        # default values are OK, but not the order (IMHO)
        self.leds.animate_flash(color, leds,
                                timestep, duration, block)
    
    # --- Turn the leds off ------------------------------------------
    def leds_off(self) -> None:
        """Turns the leds off."""
        self.leds.all_off()
    
# === Main function and module call ==================================

# Using a main function is cleaner than having global variables
# and function calls.

def main(noisy = False) -> int:
    """Checks the robot output (simple)."""
    # defines the robot output:
    # adding an argument in console prevents displaying the images
    robot_out = RobotOutput(noisy)

    robot_out.set_leds('AMBER', 'AMBER')
    host_letter = socket.gethostname()[4]
    robot_out.new_output('Console test on EV3-' + host_letter + '!',
                         'Thumbs up',
                         'Hello, I am E V 3 ' + host_letter)
    
    time.sleep(0.1)

    robot_out.new_text('Flashing leds', (5, 25), True)
    robot_out.flash_leds('YELLOW', ('LEFT', 'RIGHT'), True)
    
    robot_out.leds_off()
    return 0
    
# When this module is called, it starts the main function.
if __name__ == "__main__":
    sys.exit( main() )

# Checked led setting and output in silent and noisy console,
#                                and in silent brick display.
# Checked led flasshing and text in same situations.
