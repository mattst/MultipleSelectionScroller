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

    # Class variable definitions of the various constants used:

    # For: control mode - assigned to the control_mode instance variable.

    SCROLL                 = 10
    CLEAR                  = 20

    # For: scrolling to selections - assigned to the scroll_to instance variable.

    SCROLL_TO_PREVIOUS     = 30
    SCROLL_TO_NEXT         = 40
    SCROLL_TO_FIRST        = 50
    SCROLL_TO_LAST         = 60

    # For: cursor position after clearing selections - assigned to the clear_to instance variable.

    CLEAR_TO_FIRST         = 70
    CLEAR_TO_LAST          = 80
    CLEAR_TO_NEAREST       = 90

    # For: Operational status.

    MIN_NUM_SELECTIONS     = 1
    MIN_NUM_VISIBLE_LINES  = 2


    def run(self, edit, **kwargs):
        """
        run() is called when the command is run - it controls the plugin's flow of execution.
        """

        # Define the 3 instance variables (no other instance variables are used).

        # Storage for the control mode.
        self.control_mode = None

        # Storage for which scroll operation to perform.
        self.scroll_to = None

        # Storage for which clear operation to perform.
        self.clear_to = None

        # Check to make sure there are selections and visible lines.
        if not self.operational_status():
            return

        # Set scroll_to, clear_to, and control_mode according to the argument used in the command
        # call. Note that if the command was called correctly then either scroll_to or clear_to
        # will remain set to None but control_mode will be definitely set.

        self.set_scroll_to(**kwargs)
        self.set_clear_to(**kwargs)

        # If control_mode has not been set, the command was called using invalid values.
        if self.control_mode is None:
            msg = "multiple_selection_scroller command: missing or invalid command args"
            print(msg)
            sublime.status_message(msg)
            return

        # Perform the required scrolling operation.
        elif self.control_mode == MultipleSelectionScrollerCommand.SCROLL:
            self.control_scrolling()

        # Perform the required clearing operation.
        elif self.control_mode == MultipleSelectionScrollerCommand.CLEAR:
            self.control_clearing()

    # End of def run()


    def operational_status(self):
        """
        operational_status() checks that the number of selections and the number of visible lines
        are both greater than the required minimum, displaying a status message and returning false
        if not.
        """

        # Get the number of selections and return false if fewer than the minimum (1).
        # Clearly there is nothing for this plugin to do.

        sels = self.view.sel()
        sels_len = len(sels)

        if sels_len < MultipleSelectionScrollerCommand.MIN_NUM_SELECTIONS:
            msg = "multiple_selection_scroller command: no selections"
            sublime.status_message(msg)
            return False

        # Get the the number of visible lines and return false if fewer than the minimum (2).
        # Note that there are design reasons for this check (calculating the middle line).

        visible_region = self.view.visible_region()
        visible_lines = self.view.lines(visible_region)
        visible_lines_len = len(visible_lines)

        if visible_lines_len < MultipleSelectionScrollerCommand.MIN_NUM_VISIBLE_LINES:
            msg = "multiple_selection_scroller command: too few visible lines"
            sublime.status_message(msg)
            return False

        # All okay.
        return True

    # End of def operational_status()


    def set_scroll_to(self, **kwargs):
        """
        set_scroll_to() sets the scroll_to instance variable according to the value held by
        "scroll_to" in the kwargs dictionary and sets the control_mode instance variable.
        """

        # If available get the command's "scroll_to" arg from the kwargs dictionary.
        if "scroll_to" in kwargs:
            scroll_to_arg_val = kwargs.get("scroll_to")

        # "scroll_to" is not in the dictionary.
        else:
            return

        # Convert to a string in case some other type was used in error.
        scroll_to_arg_val = str(scroll_to_arg_val)

        # Set the scroll_to instance variable.

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

        # Set the control_mode instance variable.
        self.control_mode = MultipleSelectionScrollerCommand.SCROLL

    # End of def set_scroll_to()


    def set_clear_to(self, **kwargs):
        """
        set_clear_to() sets the clear_to instance variable according to the value held by
        "clear_to" in the kwargs dictionary and sets the control_mode instance variable.
        """

        # If available get the command's "clear_to" arg from the kwargs dictionary.
        if "clear_to" in kwargs:
            clear_to_arg_val = kwargs.get("clear_to")

        # "clear_to" is not in the dictionary.
        else:
            return

        # Convert to a string in case some other type was used in error.
        clear_to_arg_val = str(clear_to_arg_val)

        # Set the clear_to instance variable.

        if clear_to_arg_val.lower() == "first":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_FIRST

        elif clear_to_arg_val.lower() == "last":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_LAST

        elif clear_to_arg_val.lower() == "nearest":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_NEAREST

        # "clear_to" is set to an invalid value.
        else:
            return

        # Set the control_mode instance variable.
        self.control_mode = MultipleSelectionScrollerCommand.CLEAR

    # End of def set_clear_to()


    def control_scrolling(self):
        """
        control_scrolling() controls scrolling calling the appropriate method depending on what the
        value of the scroll_to instance variable has been set to.

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

    # End of def control_scrolling()


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


    def control_clearing(self):
        """
        control_clearing() ...
        """

        # Get the selections and the length of the selections' list.
        sels = self.view.sel()
        sels_len = len(sels)

        # Get the cursor position of the first selection.
        if self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_FIRST:
            first_sel_index = 0
            first_sel = sels[first_sel_index]
            cursor_pos = first_sel.b

        # Get the cursor position of the last selection.
        elif self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_LAST:
            last_sel_index = sels_len - 1
            last_sel = sels[last_sel_index]
            cursor_pos = last_sel.b

        # Get the cursor position of the selection nearest the middle visible line.
        elif self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_NEAREST:
            cursor_pos = self.get_cursor_pos_selection_nearest_middle_line(sels, sels_len)

        # Clear the selections.
        sels.clear()

        # Add a new selection at the cursor position.
        sels.add(cursor_pos)

        # Move the view to centre on the cursor position.
        self.view.show_at_center(cursor_pos)

    # End of def control_clearing()


    def get_cursor_pos_selection_nearest_middle_line(self, sels, sels_len):

        # Get the region of the middle line and get its row number.
        middle_line = self.get_middle_line()
        middle_line_row, col = self.view.rowcol(middle_line.begin())

        # Get the first selection to occur on or below the middle line and get its row number.
        sel = self.get_first_selection_on_or_below_middle_line(sels, sels_len, middle_line)
        sel_first_below_middle_line = sel
        sel_first_below_middle_line_row, col = self.view.rowcol(sel.begin())

        # Get the first selection to occur on or above the middle line and get its row number.
        sel = self.get_first_selection_on_or_above_middle_line(sels, sels_len, middle_line)
        sel_first_above_middle_line = sel
        sel_first_above_middle_line_row, col = self.view.rowcol(sel.begin())

        # Calculate the distance to the first below and to the first above.
        distance_to_first_below = sel_first_below_middle_line_row - middle_line_row
        distance_to_first_above = middle_line_row - sel_first_above_middle_line_row

        # In case there are no selections below or no selections above the middle line make sure
        # that there are no negative distances by multiplying by -1.
        if distance_to_first_below < 0: distance_to_first_below *= -1
        if distance_to_first_above < 0: distance_to_first_above *= -1

        # Establish which selection is nearest the middle line.
        if distance_to_first_below <= distance_to_first_above:
            sel_nearest_middle_line = sel_first_below_middle_line
        else:
            sel_nearest_middle_line = sel_first_above_middle_line

        # Return the cursor position of the selection nearest the middle line.
        return sel_nearest_middle_line.b

    # End of def get_cursor_pos_selection_nearest_middle_line()


    def get_middle_line(self):
        """
        get_middle_line() returns the region of the middle line of the visible lines.
        """

        # Get the visible region, the list of visible lines, and the number of visible lines.

        visible_region = self.view.visible_region()
        visible_lines = self.view.lines(visible_region)
        visible_lines_len = len(visible_lines)

        # Calculate which line is in the middle of the visible lines, converting to int floors it.
        middle_line_num = int(visible_lines_len / 2)

        # Store the region of the middle line.
        middle_line = visible_lines[middle_line_num]

        return middle_line

    # End of def get_middle_line()


    def get_first_selection_on_or_below_middle_line(self, sels, sels_len, middle_line):

        # Starting at the first selection, loop forwards through all the selections looking for the
        # first selection to occur on or below the middle line.

        sel_index = 0
        found = False

        while sel_index < sels_len and not found:

            sel = sels[sel_index]

            # If a selection is found on or below the middle line, quit loop.
            if sel.begin() >= middle_line.begin():
                found = True

            sel_index += 1

        # The first selection to be found on or below the middle line is returned. If there is no
        # such selection then the last selection is returned.

        return sel

    # End of def get_first_selection_on_or_below_middle_line()


    def get_first_selection_on_or_above_middle_line(self, sels, sels_len, middle_line):

        # Starting at the last selection, loop backwards through all the selections looking for the
        # first selection to occur on or above the middle line.

        sel_index = sels_len - 1
        found = False

        while sel_index >= 0 and not found:

            sel = sels[sel_index]

            # If a selection is found on or above the middle line, quit loop.
            if sel.begin() <= middle_line.end():
                found = True

            sel_index -= 1

        # The first selection to be found on or above the middle line is returned. If there is no
        # such selection then the first selection is returned.

        return sel

    # End of def get_first_selection_on_or_above_middle_line()

# End of class MultipleSelectionScrollerCommand()

