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

    def run(self, edit, **kwargs):
        """
        run() is called when the command is run - it controls the plugin's flow of execution.
        """


    # End of def run()

# End of class MultipleSelectionScrollerCommand()
