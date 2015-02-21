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
# Last Edited:    2015-02-20
#
# Version:        n/a
#
# ST Command:     multiple_selection_scroller
#
# Required Arg:   scroll     : Scroll to where:
# Arg Value:      next       : Scroll forwards to the next selection
# Arg Value:      previous   : Scroll backwards to the previous selection
# Arg Value:      first      : Scroll to the first (top) selection
# Arg Value:      last       : Scroll to the last (bottom) selection
#
# Settings Examples:
#
# Default (OS).sublime-keymap file:
#
# { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll": ""} }
# { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll": ""} }
#


import sublime
import sublime_plugin


class MultipleSelectionScrollerCommand(sublime_plugin.TextCommand):
    """
    The MultipleSelectionScrollerCommand class is a Sublime Text plugin which...

    """

    # Definitions of the various constants used:

    # For mode control, assigned to the mode class variable.

    SCROLL             = 1
    CLEAR              = 2

    # For scrolling to selections, assigned to the scroll_to class variable.

    SCROLL_TO_PREVIOUS = 3
    SCROLL_TO_NEXT     = 4
    SCROLL_TO_FIRST    = 5
    SCROLL_TO_LAST     = 6

    # For cursor position after clearing selections, assigned to the clear_to class variable.

    CLEAR_TO_FIRST     = 7
    CLEAR_TO_LAST      = 8
    CLEAR_TO_NEAREST   = 9


    def run(self, edit, **kwargs):
        """
        run() is called when the command is run - it controls the plugin's flow of execution.
        """

        # Get the number of selections and abort if there aren't any, nothing to do.

        sels_len = len(self.view.sel())

        if sels_len < 1:
            return

        self.mode = None

        # Set the scroll direction to the value specified by the command's "scroll" argument.

        self.scroll_to = None

        self.set_scroll_to(**kwargs)

        self.clear_to = None

        self.set_clear_to(**kwargs)

        print("mode: " + str(self.mode))
        print("scroll_to: " + str(self.scroll_to))
        print("clear_to: " + str(self.clear_to))

        if self.mode is None:
            msg = "multiple_selection_scroller command: missing or invalid command args"
            print(msg)
            sublime.status_message(msg)
            return

        # Perform the scrolling.

        self.handle_scrolling()

    # End of def run()


    def set_scroll_to(self, **kwargs):
        """
        set_scroll_to() sets the scroll_to class variable according to the value held by "scroll_to"
        in the kwargs dictionary and sets the mode class variable.
        """

        # If available get the command's "scroll_to" arg from the kwargs dictionary.
        if "scroll_to" in kwargs:
            scroll_to_arg_val = kwargs.get("scroll_to")

        # "scroll_to" is not in the dictionary.
        else:
            return

        # Convert to a string in case some other type was used in error.
        scroll_to_arg_val = str(scroll_to_arg_val)

        # Set the scroll_to class variable.

        if scroll_to_arg_val.lower() == "next":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_NEXT

        elif scroll_to_arg_val.lower() == "previous":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_PREVIOUS

        elif scroll_to_arg_val.lower() == "first":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_FIRST

        elif scroll_to_arg_val.lower() == "last":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_LAST

        # "scroll_to" is set to an invalid value.
        else:
            return

        self.mode = MultipleSelectionScrollerCommand.SCROLL

    # End of def set_scroll_to()


    def set_clear_to(self, **kwargs):
        """
        set_clear_to() sets the clear_to class variable according to the value held by "clear_to"
        in the kwargs dictionary and sets the mode class variable.
        """

        # If available get the command's "clear_to" arg from the kwargs dictionary.
        if "clear_to" in kwargs:
            clear_to_arg_val = kwargs.get("clear_to")

        # "clear_to" is not in the dictionary.
        else:
            return

        # Convert to a string in case some other type was used in error.
        clear_to_arg_val = str(clear_to_arg_val)

        # Set the clear_to class variable.

        if clear_to_arg_val.lower() == "first":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_FIRST

        elif clear_to_arg_val.lower() == "last":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_LAST

        elif clear_to_arg_val.lower() == "nearest":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_NEAREST

        # "clear_to" is set to an invalid value.
        else:
            return

        self.mode = MultipleSelectionScrollerCommand.CLEAR

    # End of def set_clear_to()


    def handle_scrolling(self):
        """
        handle_scrolling() controls scrolling calling the appropriate method depending on what the
        value of the scroll_to class variable has been set to.

        This method also provides important notes about how this plugin handles the scrolling.
        """

        # Scrolling forwards through the selections is done by moving the first selection to occur
        # below the middle line of the visible region to the middle line of the visible region.
        #
        # Scrolling backwards through the selections is done by moving the first selection to occur
        # above the middle line of the visible region to the middle line of the visible region.
        #
        # Repeated pressing of the command's keys allow scrolling backwards and forwards through all
        # the selections.
        #
        # Scrolling is performed by calling view.show_at_center(point) - there are two cases when
        # Sublime Text will not honour calls made to that method and move the visible region:
        #
        # 1) If a selection is near the top of the buffer, Sublime Text won't scroll the line it is
        # on to the centre of the visible region, there is no 'scroll_above_beginning' setting.
        #
        # 2) If a selection in near the bottom of the buffer and the setting 'scroll_past_end' has
        # been set to false (defaults to true) then again Sublime Text won't move the line it is on
        # to the centre of the visible region (however it will if 'scroll_past_end' is set to true).
        #
        # In both of these cases the next/previous selection will not be moved to the middle line
        # of the visible region, however all remaining selections whether below the middle line (if
        # scrolling forwards) or above the middle line (if scrolling backwards) will definitely be
        # in the visible region on the screen.

        # # Get the visible region, the list of visible lines, and the number of visible lines.
        # visible_region = self.view.visible_region()
        # visible_lines = self.view.lines(visible_region)
        # visible_lines_len = len(visible_lines)

        # # Abort in the unlikely event that fewer than 2 lines are visible.
        # visible_lines_minimum = 2

        # if visible_lines_len < visible_lines_minimum:
        #     return

        # # Calculate which line is in the middle of the visible lines, converting to int floors it.
        # middle_line_num = int(visible_lines_len / 2)
        # print("middle_line_num: " + str(middle_line_num))

        # # Store the region of the middle line.
        # middle_line = visible_lines[middle_line_num]


        # Perform the appropriate Scrolling.

        if self.scroll_to == MultipleSelectionScrollerCommand.SCROLL_TO_NEXT:
            self.scroll_to_next_selection()

        elif self.scroll_to == MultipleSelectionScrollerCommand.SCROLL_TO_PREVIOUS:
            self.scroll_to_previous_selection()

        elif self.scroll_to == MultipleSelectionScrollerCommand.SCROLL_TO_FIRST:
            self.scroll_to_first_selection()

        elif self.scroll_to == MultipleSelectionScrollerCommand.SCROLL_TO_LAST:
            self.scroll_to_last_selection()

    # End of def handle_scrolling()


    def get_middle_line(self):
        """
        get_middle_line() returns the region of the middle line of the visible lines.
        """

        # Get the visible region, the list of visible lines, and the number of visible lines.
        visible_region = self.view.visible_region()
        visible_lines = self.view.lines(visible_region)
        visible_lines_len = len(visible_lines)

        # Abort in the unlikely event that fewer than 2 lines are visible.
        # visible_lines_minimum = 2

        # if visible_lines_len < visible_lines_minimum:
        #     return

        # Calculate which line is in the middle of the visible lines, converting to int floors it.
        middle_line_num = int(visible_lines_len / 2)
        print("middle_line_num: " + str(middle_line_num))

        # Store the region of the middle line.
        middle_line = visible_lines[middle_line_num]

        return middle_line

    # End of def get_middle_line()


    def scroll_to_next_selection(self):
        """
        scroll_to_next_selection() moves the visible region to centre on the first selection to
        occur below the middle_line region, if there is such a selection.
        """

        # Get the selections and the number of them.
        sels = self.view.sel()
        sels_len = len(sels)

        # Get the region of the middle line.
        middle_line = self.get_middle_line()

        # Starting at the first selection, loop forwards through all the selections looking for the
        # first selection to occur below the middle line.

        sel_index = 0
        found = False

        while sel_index < sels_len and not found:

            sel = sels[sel_index]

            # If a selection is found below the middle line.
            if sel.begin() > middle_line.end():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # All done, quit loop.
                found = True

            sel_index += 1

    # End of def scroll_to_next_selection()


    def scroll_to_previous_selection(self):
        """
        scroll_to_previous_selection() moves the visible region to centre on the first selection to
        occur above the middle_line region, if there is such a selection.
        """

        # Get the selections and the number of them.
        sels = self.view.sel()
        sels_len = len(sels)

        # Get the region of the middle line.
        middle_line = self.get_middle_line()

        # Starting at the last selection, loop backwards through all the selections looking for the
        # first selection to occur above the middle line.

        sel_index = sels_len - 1
        found = False

        while sel_index >= 0 and not found:

            sel = sels[sel_index]

            # If a selection is found above the middle line.
            if sel.end() < middle_line.begin():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # All done, quit loop.
                found = True

            sel_index -= 1

    # End of def scroll_to_previous_selection()


    def scroll_to_first_selection(self):
        """
        scroll_to_first_selection() moves the visible region to centre on the first selection.
        """

        # Get the first selection.
        sels = self.view.sel()
        sel_first_index = 0
        sel_first = sels[sel_first_index]

        # Scroll the visible region to the line the first selection begins on.
        self.view.show_at_center(sel_first.begin())

    # End of def scroll_to_first_selection()


    def scroll_to_last_selection(self):
        """
        scroll_to_last_selection() moves the visible region to centre on the last selection.
        """

        # Get the last selection.
        sels = self.view.sel()
        sel_last_index = len(sels) - 1
        sel_last = sels[sel_last_index]

        # Scroll the visible region to the line the last selection begins on.
        self.view.show_at_center(sel_last.begin())

    # End of def scroll_to_last_selection()

# End of class MultipleSelectionScrollerCommand()

