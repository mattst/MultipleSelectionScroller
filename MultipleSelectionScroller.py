# Name:           MultipleSelectionScroller
#
# File:           MultipleSelectionScroller.py
#
# Requirements:   Plugin for Sublime Text v.2 and v.3
#
# Tested:         ST v.3 build 3065 - not tested
#                 ST v.2 build 2221 - not tested
#
# Written by:     Matthew Stanfield
#
# Last Edited:    2015-02-17
#
# Version:        n/a
#
# ST Command:     multiple_selection_scroller
#
# Optional Arg:   forward : Multiple selection scroll direction
# Arg Value:      true    : Scroll forwards through selections
# Arg Value:      false   : Scroll backwards through selections
#
# Settings Examples:
#
# Default (OS).sublime-keymap file:
#
# { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"forward": false} }
# { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"forward": true} }
#


import sublime
import sublime_plugin


class MultipleSelectionScrollerCommand(sublime_plugin.TextCommand):
    """
    The MultipleSelectionScrollerCommand class is a Sublime Text plugin which...
    """


    # Constants to set the scroll direction to.

    SCROLL_FORWARDS  = 1
    SCROLL_BACKWARDS = 2


    def run(self, edit, **kwargs):
        """
        run() is called when the command is run - it controls the plugin's flow of execution.
        """

        # Holds the scroll direction. Set to the default or to the value specified by the command's
        # "forward" arg.
        scroll_direction = self.set_scroll_direction(**kwargs)

        print("scroll_direction: " + str(scroll_direction))

    # End of def run()


    def set_scroll_direction(self, **kwargs):
        """
        set_scroll_direction() returns the value to set the scroll_direction variable to. If the
        command's "forward" arg is available then that will be used, otherwise the default.
        """

        # Set the default.
        scroll_direction_default = MultipleSelectionScrollerCommand.SCROLL_FORWARDS

        # If available get the "forward" arg from the kwargs dictionary.
        if "forward" in kwargs:
            forward_arg_val = kwargs.get("forward")

        # "forward" is not in the dictionary - return the default.
        else:
            return scroll_direction_default

        # Warning to display as a status message and in the console if 'forward' is not boolean.
        msg =  "multiple_selection_scroller command: 'forward' arg can be set to 'true' or 'false'"

        # If not set to a boolean value - display warning and return the default.
        if not isinstance(forward_arg_val, bool):
            print(msg)
            sublime.status_message(msg)
            return scroll_direction_default

        # Return the appropriate constant.

        if forward_arg_val == True:
            return MultipleSelectionScrollerCommand.SCROLL_FORWARDS

        elif forward_arg_val == False:
            return MultipleSelectionScrollerCommand.SCROLL_BACKWARDS

        # "forward" is set to an invalid value - display warning and return the default.
        else:
            print(msg)
            sublime.status_message(msg)
            return scroll_direction_default

    # End of def set_scroll_direction()

# End of class MultipleSelectionScrollerCommand()
