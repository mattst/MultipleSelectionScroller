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
# Last Edited:    2015-02-22
#
# Version:        n/a
#
# ST Command:     multiple_selection_scroller
#
# Arg Required:   Either scroll_to or clear_to must be used but not both.
#
# Arg:            scroll_to  : Scroll to where (placing on middle line):
# Value:          next       : Forwards to the next selection
# Value:          previous   : Backwards to the previous selection
# Value:          first      : To the first (top) selection
# Value:          last       : To the last (bottom) selection
#
# Arg:            clear_to   : Clear all selections, leaving a single cursor at:
# Value:          first      : The first (top) selection
# Value:          last       : The last (bottom) selection
# Value:          nearest    : The selection nearest the middle line
#
# Settings Examples:
#
# Default (OS).sublime-keymap file:
#
# { "keys": [""], "command": "multiple_selection_scroller", "args": {"scroll_to": ""} }
# { "keys": [""], "command": "multiple_selection_scroller", "args": {"clear_to": ""} }
#


import sublime
import sublime_plugin


class MultipleSelectionScrollerCommand(sublime_plugin.TextCommand):
    """
    The MultipleSelectionScrollerCommand class is a Sublime Text plugin which...

    """

    # Definitions of the various constants used:

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

    # For: Operational status - values are checked for in operational_status().

    MIN_NUM_SELECTIONS     = 1
    MIN_NUM_VISIBLE_LINES  = 1


    def run(self, edit, **kwargs):
        """
        run() is called when the command is run - it controls the plugin's flow of execution.
        """

        # Define the 5 instance variables (no other instance variables are used).

        # Holds the control mode - set by either: set_scroll_to() or set_clear_to()
        self.control_mode = None

        # Holds which scroll operation to perform (if any) - set by: set_scroll_to()
        self.scroll_to = None

        # Holds which clear operation to perform (if any) - set by: set_clear_to()
        self.clear_to = None

        # Holds the current selections.
        self.sels = self.view.sel()

        # Holds the length of the current selections.
        self.sels_len = len(self.sels)

        # Check to make sure that there are selections and visible lines.
        if not self.operational_status():
            return

        # Set the scroll_to instance variable if the command was called using the scroll_to arg,
        # if so then it will also set the control_mode instance variable to the constant SCROLL.
        self.set_scroll_to(**kwargs)

        # Set the clear_to instance variable if the command was called using the clear_to arg,
        # if so then it will also set the control_mode instance variable to the constant CLEAR.
        self.set_clear_to(**kwargs)

        # If control_mode has not been set, the command was called using invalid values.
        if self.control_mode is None:
            msg = "multiple_selection_scroller: invalid or missing command args"
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

        # Return false if there are no selections, clearly there is nothing for this plugin to do.

        if self.sels_len < MultipleSelectionScrollerCommand.MIN_NUM_SELECTIONS:
            msg = "multiple_selection_scroller: there are no selections"
            sublime.status_message(msg)
            return False

        # Get the the number of visible lines and return false if fewer than the minimum.
        # Note: There are design reasons for this check (calculating the middle line).

        visible_region = self.view.visible_region()
        visible_lines = self.view.lines(visible_region)
        visible_lines_len = len(visible_lines)

        if visible_lines_len < MultipleSelectionScrollerCommand.MIN_NUM_VISIBLE_LINES:
            msg = "multiple_selection_scroller: too few visible lines"
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
        control_scrolling() controls scrolling calling the appropriate method depending on what
        value the scroll_to instance variable has been set to.

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
        occur below the middle_line region. If there is no such selection it moves the visible
        region to centre on the first selection (i.e. cycles up to the first selection).
        """

        # Get the region of the middle line.
        middle_line = self.get_middle_line()

        # Get the viewport position. [Note: This is used to help with cycled scrolling.]
        vertical_axis_index = 1
        viewport_pos_before_centering = self.view.viewport_position()[vertical_axis_index]

        # Starting at the first selection, loop forwards through all the selections looking for the
        # first selection to occur below the middle line - if found centre on that selection.

        sel_index = 0
        found = False

        while sel_index < self.sels_len and not found:

            sel = self.sels[sel_index]

            # If a selection is found below the middle line.
            if sel.begin() > middle_line.end():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # Quit loop.
                found = True

            sel_index += 1

        # If no selection was found below the middle line, cycle up to the first selection.
        if not found:
            self.scroll_to_first_selection()
            return

        # IMPORTANT NOTE: Checking to see if the found variable is False can not always be relied
        # on for cycled scrolling because selections below the middle line on the final page of the
        # buffer do not trigger cycling up to the first selection. This is because of the way
        # view.show_at_center() behaves; it sensibly centres the given region in the viewport but
        # this means that selections can still exist below the middle visible line although only on
        # the final page of the buffer. This is a known design limitation of the plugin, it can not
        # scroll lower than the first selection below the middle line on the buffer's final page,
        # but any such selections are guaranteed to be in the visible region, and cycled scrolling
        # can still be achieved by examining the viewport's vertical axis position, so this is a
        # minor limitation. Suggestions on how to get around this would be most welcome. :)

        # Check for cycled scrolling for selections below the middle line on the last page.

        # Get the viewport position.
        viewport_pos_after_centering = self.view.viewport_position()[vertical_axis_index]

        # If the viewport's vertical axis position is unchanged, cycle up to the first selection.
        if viewport_pos_before_centering == viewport_pos_after_centering:
            self.scroll_to_first_selection()

    # End of def scroll_to_next_selection()


    def scroll_to_previous_selection(self):
        """
        scroll_to_previous_selection() moves the visible region to centre on the first selection to
        occur above the middle_line region. If there is no such selection it moves the visible
        region to centre on the last selection (i.e. cycles down to the last selection).
        """

        # Get the region of the middle line.
        middle_line = self.get_middle_line()

        # Get the viewport position. [Note: This is used to help with cycled scrolling.]
        vertical_axis_index = 1
        viewport_pos_before_centering = self.view.viewport_position()[vertical_axis_index]

        # Starting at the last selection, loop backwards through all the selections looking for the
        # first selection to occur above the middle line - if found centre on that selection.

        sel_index = self.sels_len - 1
        found = False

        while sel_index >= 0 and not found:

            sel = self.sels[sel_index]

            # If a selection is found above the middle line.
            if sel.end() < middle_line.begin():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # Quit loop.
                found = True

            sel_index -= 1

        # If no selection was found above the middle line, cycle down to the last selection.
        if not found:
            self.scroll_to_last_selection()
            return

        # IMPORTANT NOTE: Checking to see if the found variable is False can not always be relied
        # on for cycled scrolling because selections above the middle line on the first page of the
        # buffer do not trigger cycling down to the last selection. This is because of the way
        # view.show_at_center() behaves; it sensibly centres the given region in the viewport but
        # this means that selections can still exist above the middle visible line although only on
        # the first page of the buffer. This is a known design limitation of the plugin, it can not
        # scroll higher than the first selection above the middle line on the buffer's first page,
        # but any such selections are guaranteed to be in the visible region, and cycled scrolling
        # can still be achieved by examining the viewport's vertical axis position, so this is a
        # minor limitation. Suggestions on how to get around this would be most welcome. :)

        # Check for cycled scrolling for selections above the middle line on the first page.

        # Get the viewport position.
        viewport_pos_after_centering = self.view.viewport_position()[vertical_axis_index]

        # If the viewport's vertical axis position is unchanged, cycle down to the last selection.
        if viewport_pos_before_centering == viewport_pos_after_centering:
            self.scroll_to_last_selection()

    # End of def scroll_to_previous_selection()


    def scroll_to_first_selection(self):
        """
        scroll_to_first_selection() moves the visible region to centre on the first selection.
        """

        sel_first_index = 0
        self.scroll_to_selection_index(sel_first_index)

    # End of def scroll_to_first_selection()


    def scroll_to_last_selection(self):
        """
        scroll_to_last_selection() moves the visible region to centre on the last selection.
        """

        sel_last_index = self.sels_len - 1
        self.scroll_to_selection_index(sel_last_index)

    # End of def scroll_to_last_selection()


    def scroll_to_selection_index(self, sel_index):
        """
        scroll_to_selection_index() moves the visible region to centre on the selection specified
        by sel_index.
        """

        # Scroll the visible region to the line of the selection.
        sel = self.sels[sel_index]
        self.view.show_at_center(sel.begin())

    # End of def scroll_to_last_selection()


    def control_clearing(self):
        """
        control_clearing() controls clearing the selections and leaving a cursor at the selection
        specified by the value of the clear_to instance variable.
        """

        # Get the first selection and its index.
        if self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_FIRST:
            sel_index = 0
            sel = self.sels[sel_index]

        # Get the last selection and its index.
        elif self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_LAST:
            sel_index = self.sels_len - 1
            sel = self.sels[sel_index]

        # Get the selection nearest the middle visible line and its index.
        elif self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_NEAREST:
            sel_index = self.get_selection_index_nearest_middle_line()
            sel = self.sels[sel_index]

        # Get the cursor position of the chosen selection.
        cursor_pos = sel.b

        # Clear the selections.
        self.sels.clear()

        # Add a new selection at the cursor position.
        self.sels.add(cursor_pos)

        # Move the view to centre on the cursor position.
        self.view.show_at_center(cursor_pos)

    # End of def control_clearing()


    def get_selection_index_nearest_middle_line(self):
        """
        get_selection_index_nearest_middle_line() returns the index of the selection which is
        nearest to the middle line of the visible lines.
        """

        # Set the row index of the tuple returned by view.rowcol().
        row_index = 0

        # Get the region of the middle line and get its row number.
        middle_line = self.get_middle_line()
        middle_line_row = self.view.rowcol(middle_line.begin())[row_index]

        # Get the first selection to occur on or below the middle line, its index, and row number.
        # Note: If no selection on/below the middle line this will be set to the last selection.
        sel_index_first_below = self.get_selection_index_on_or_below_middle_line(middle_line)
        sel_first_below = self.sels[sel_index_first_below]
        sel_row_first_below = self.view.rowcol(sel_first_below.begin())[row_index]

        # Get the first selection to occur on or above the middle line, its index, and row number.
        # Note: If no selection on/above the middle line this will be set to the first selection.
        sel_index_first_above = self.get_selection_index_on_or_above_middle_line(middle_line)
        sel_first_above = self.sels[sel_index_first_above]
        sel_row_first_above = self.view.rowcol(sel_first_above.begin())[row_index]

        # Calculate the distance to the first below and to the first above.
        distance_to_first_below = sel_row_first_below - middle_line_row
        distance_to_first_above = middle_line_row - sel_row_first_above

        # Remove negative distances (for cases when there are no selections below or above).
        if distance_to_first_below < 0: distance_to_first_below *= -1
        if distance_to_first_above < 0: distance_to_first_above *= -1

        # Establish which selection is nearest the middle line and return its index.
        # Note: If the distances are equidistant the first above is returned.
        if distance_to_first_above <= distance_to_first_below:
            return sel_index_first_above
        else:
            return sel_index_first_below

    # End of def get_selection_index_nearest_middle_line()


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


    def get_selection_index_on_or_below_middle_line(self, middle_line):
        """
        get_selection_index_on_or_below_middle_line() returns the index of the selection that is
        either on or the first to occur below the middle line. If there is no selection on/below
        the middle line then the last selection is returned.
        """

        # Starting at the first selection, loop forwards through all the selections looking for the
        # first selection to occur on or below the middle line.

        sel_index = 0
        found = False

        while sel_index < self.sels_len and not found:

            sel = self.sels[sel_index]
            sel_index_first_on_or_below_or_last = sel_index

            # If a selection is found on or below the middle line, quit loop.
            if sel.begin() >= middle_line.begin():
                found = True

            sel_index += 1

        # The first selection to be found on or below the middle line is returned. If there is no
        # such selection then the last selection is returned.

        return sel_index_first_on_or_below_or_last

    # End of def get_selection_index_on_or_below_middle_line()


    def get_selection_index_on_or_above_middle_line(self, middle_line):
        """
        get_selection_index_on_or_above_middle_line() returns the index of the selection that is
        either on or the first to occur above the middle line. If there is no selection on/above
        the middle line then the first selection is returned.
        """

        # Starting at the last selection, loop backwards through all the selections looking for the
        # first selection to occur on or above the middle line.

        sel_index = self.sels_len - 1
        found = False

        while sel_index >= 0 and not found:

            sel = self.sels[sel_index]
            sel_index_first_on_or_above_or_first = sel_index

            # If a selection is found on or above the middle line, quit loop.
            if sel.begin() <= middle_line.end():
                found = True

            sel_index -= 1

        # The first selection to be found on or above the middle line is returned. If there is no
        # such selection then the first selection is returned.

        return sel_index_first_on_or_above_or_first

    # End of def get_selection_index_on_or_above_middle_line()

# End of class MultipleSelectionScrollerCommand()

