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
import math


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

        # Get the number of selections and abort if there aren't any, none to scroll through.

        sels_len = len(self.view.sel())

        if sels_len < 1:
            return

        # Store the scroll direction - set it to the value specified by the command's "forward"
        # argument or to the default (which is to scroll forwards).

        scroll_direction = self.set_scroll_direction(**kwargs)

        # Perform the scrolling.

        self.handle_scrolling(scroll_direction)

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


    def handle_scrolling(self, scroll_direction):

        # Scrolling forwards through the selections is done by moving the next selection which
        # occurs after the middle line of the visible region to the middle line of the visible
        # region. Scrolling backwards through the selections is done in the same way except by
        # moving the next selection which occurs before the middle line.
        #
        # It is not possible to do this in two cases:
        #
        # If a selection is near the top of the buffer, Sublime Text won't scroll the line it is
        # on to the centre of the visible region, there is no 'scroll_above_begining' setting.
        #
        # If a selection in near the bottom of the buffer and the setting 'scroll_past_end' has been
        # set to false (defaults to true) then again Sublime Text won't move the line it is on to
        # the centre of the visible region (although it will if 'scroll_past_end' is set to true).
        #
        # In both of these cases, although the selection will not be moved to the middle line of
        # the visible region, the selection will still be viewable on the screen.

        # Get the visible region, the list of visible lines, and the number of visible lines.
        visible_region = self.view.visible_region()
        visible_lines = self.view.lines(visible_region)
        visible_lines_len = len(visible_lines)

        # Just in case nothing is visible at all. Note that view.lines() will always return at least
        # one line (the top line) even if the visible_region is (0, 0). Note also that if two lines
        # are visible then the scrolling done by this plugin still works.
        if visible_lines_len < 2:
            return

        # Calculate which line is in the middle of the visible lines, converting to int floors it.
        middle_line_num = int(visible_lines_len / 2)

        # Store the region of the middle line.
        middle_line = visible_lines[middle_line_num]

        # Scroll forwards or backwards as appropriate.

        if scroll_direction == MultipleSelectionScrollerCommand.SCROLL_FORWARDS:
            self.scroll_forwards(middle_line)

        elif scroll_direction == MultipleSelectionScrollerCommand.SCROLL_BACKWARDS:
            self.scroll_backwards(middle_line)

    # End of def handle_scrolling()


    def scroll_forwards(self, middle_line):

        # Store the selections and the number of them.
        sels = self.view.sel()
        sels_len = len(sels)

        # Starting from the first selection, loop through all the selections looking for the next
        # selection to occur after the middle line.

        sel_index = 0
        found = False

        while sel_index < sels_len and not found:

            sel = sels[sel_index]

            # If a selection is found after the middle line.
            if sel.begin() > middle_line.end():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # All done, quit loop.
                found = True

            sel_index += 1

    # End of def scroll_forwards()


    def scroll_backwards(self, middle_line):

        # Store the selections and the number of them.
        sels = self.view.sel()
        sels_len = len(sels)

        # Starting from the last selection, loop through all the selections looking for the next
        # selection to occur before the middle line.

        sel_index = sels_len - 1
        found = False

        while sel_index >= 0 and not found:

            sel = sels[sel_index]

            # If a selection is found before the middle line.
            if sel.end() < middle_line.begin():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # All done, quit loop.
                found = True

            sel_index -= 1

    # End of def scroll_backwards()

# End of class MultipleSelectionScrollerCommand()

