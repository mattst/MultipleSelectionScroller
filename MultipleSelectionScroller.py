#
# Name:           MultipleSelectionScroller
#
# File:           MultipleSelectionScroller.py
#
# Requirements:   Plugin for Sublime Text v.2 and v.3
#
# Tested:         ST v.3 build 3065 - tested and working
#                 ST v.2 build 2221 - tested and working
#                 Tests done on Linux 64 bit OS
#
# Written by:     Matthew Stanfield
#
# Last Edited:    2015-02-28
#
# Version:        n/a
#
# ST Command:     multiple_selection_scroller
#
# Arg Required:   Either scroll_to OR clear_to must be used but not both.
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
# Value:          middle     : The selection on, or nearest to, the visible middle line
#
# Optional Arg:   feedback   : Controls whether to display status messages:
# Value:          true       : Display status messages (default)
# Value:          false      : Do not display status messages
#
# Settings File:  Optionally status messages can also be set in a settings file.
# Setting:        MultipleSelectionScroller.feedback
# Value:          true       : Display status messages (default)
# Value:          false      : Do not display status messages
#
# Suggested keys for Default (OS).sublime-keymap file (the ones I use):
#
# Scroll to previous/next using "alt+[" and "alt+]":
#
# [The '[' and ']' keys are already used for line indenting and code folding, using them for
# multi-selection scrolling in conjunction with alt seems both convenient and appropriate.]
#
# { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
# { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },
#
# Scroll to first/last using "alt+k", "alt+[" and "alt+k", "alt+]":
#
# { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first"} },
# { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last"} },
#
# Clear to first/last/middle using ctrl+k", "ctrl+[", "ctrl+k", "ctrl+]", and "ctrl+k", "ctrl+#":
#
# { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "first"} },
# { "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },
# { "keys": ["ctrl+k", "ctrl+#"], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
#
# Clear to middle (duplication) using "alt+k", "alt+#":
#
# [Clearing to middle is often used during scrolling, so using "alt+k" rather than moving the key
# being held down to "ctrl" is both convenient and quicker.]
#
# { "keys": ["alt+k", "alt+#"], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
#
# The use of '#' in the two 'clear to middle' examples above is because the '#' key is to the right
# of the ']' key on my (British) keyboard. On a USA keyboard the '\' key occupies that position, so
# that should be substituted for '#'. On some Mac keyboards there is no key at all on the right of
# the ']' key. Of course, these are just suggestions, use whatever you want. :)
#


import sublime
import sublime_plugin


class MultipleSelectionScrollerCommand(sublime_plugin.TextCommand):
    """
    The MultipleSelectionScrollerCommand class is a Sublime Text plugin which provides commands to
    allow scrolling forwards and backwards through the current selections, by moving the visible
    region so that the next/previous selection is centered on the middle line. Cycling from the last
    selection up to the first and visa-versa is automatic. Commands to scroll straight to the first
    and to the last selection complete its scrolling functionality.

    The class also provides commands to clear the selections whilst leaving a single cursor at the
    first selection, the last selection, or at the selection on, or nearest to, the middle line.

    User feedback is given in the form of status messages, telling the user which selection has just
    been placed on the middle line (e.g. "5 of 11") if scrolling, or at which selection the cursor
    has been left if clearing the selections. User feedback can be disabled.

    There is a known design limitation of the plugin. To move selections to the middle line it uses
    the Sublime View class method show_at_center(). Under some circumstances that method will not
    move the visible region; if a selection is above the middle line on the first page or below the
    middle line on the last page and the 'scroll_past_end' setting has been set to false (defaults
    to true), then show_at_center() will not move the visible region. In both cases all selections
    either above the middle line on the first page or below on the last page are guaranteed to be in
    the visible region on the screen. Neither of these cases prevent scroll cycling. A more detailed
    explanation of this limitation is made in code comments in the scrolling methods of this class.
    Unfortunately there does not seem to be any way around this with the current Sublime Text API
    and without the addition of a new 'scroll_above_beginning' setting.
    """

    # Definitions of the various constants used:

    # For: control mode - assigned to the control_mode instance variable.

    SCROLL_TO              = 100
    CLEAR_TO               = 110

    # For: scrolling to selections - assigned to the scroll_to instance variable.

    SCROLL_TO_PREVIOUS     = 120
    SCROLL_TO_NEXT         = 130
    SCROLL_TO_FIRST        = 140
    SCROLL_TO_LAST         = 150

    # For: cursor position after clearing selections - assigned to the clear_to instance variable.

    CLEAR_TO_FIRST         = 160
    CLEAR_TO_LAST          = 170
    CLEAR_TO_MIDDLE        = 180

    # For: user feedback status messages - assigned to the user_feedback instance variable.

    FEEDBACK_VERBOSE       = 190
    FEEDBACK_QUIET         = 200

    # For: Operational status - values are checked for in operational_status().

    MIN_NUM_SELECTIONS     = 1
    MIN_NUM_VISIBLE_LINES  = 3


    def run(self, edit, **kwargs):
        """
        run() is called when the command is run - it controls the plugin's flow of execution.
        """

        # Define the 6 instance variables (no other instance variables are used).

        # Holds the control mode - set by either: set_scroll_to() or set_clear_to()
        self.control_mode = None

        # Holds which scroll operation to perform (if any) - set by: set_scroll_to()
        self.scroll_to = None

        # Holds which clear operation to perform (if any) - set by: set_clear_to()
        self.clear_to = None

        # Holds whether to display user feedback (status messages) - set by: set_user_feedback()
        self.user_feedback = None

        # Holds the current selections.
        self.sels = self.view.sel()

        # Holds the length of the current selections.
        self.sels_len = len(self.sels)

        # Handle command args and settings, and check them.

        # Set the scroll_to instance variable if the command was called using the scroll_to arg,
        # if so then it will also set the control_mode instance variable.
        self.set_scroll_to(**kwargs)

        # Set the clear_to instance variable if the command was called using the clear_to arg,
        # if so then it will also set the control_mode instance variable.
        self.set_clear_to(**kwargs)

        # Set the user_feedback instance variable. In order of priority: to the value given in the
        # command's args, to the value given in the user's settings file, or to the default.
        self.set_user_feedback(**kwargs)

        # Check to make sure that control_mode has been set and that there are both selections and
        # visible lines.
        if not self.operational_status():
            return

        # All present and correct - proceed to...

        # Perform the required scrolling operation.
        if self.control_mode == MultipleSelectionScrollerCommand.SCROLL_TO:
            self.control_scrolling()

        # Perform the required clearing operation.
        elif self.control_mode == MultipleSelectionScrollerCommand.CLEAR_TO:
            self.control_clearing()

    # End of def run()


    def operational_status(self):
        """
        operational_status() checks that everything is in place to proceed with the selection
        scrolling or clearing. It displays a status warning message and returns false if there's a
        problem, otherwise it returns true. It checks that control_mode has been set, and that the
        number of selections and the number of visible lines are greater than the required minimum.
        """

        # Return false if control_mode has not been set, invalid command args were used.
        # In this case also output msg to the console - to aid user investigation.

        if self.control_mode is None:
            msg = "multiple_selection_scroller: invalid or missing command args"
            print(msg)
            sublime.status_message(msg)
            return False

        # Return false if there are no selections, clearly there is nothing for this plugin to do.

        if self.sels_len < MultipleSelectionScrollerCommand.MIN_NUM_SELECTIONS:
            msg = "multiple_selection_scroller: there are no selections"
            sublime.status_message(msg)
            return False

        # Return false if the number of visible lines is fewer than the minimum.
        # Note: There are design reasons for this check (calculating the middle line).
        # This check also prevents the plugin from running in a panel or the command palette.

        visible_region = self.view.visible_region()
        visible_lines_len = len(self.view.lines(visible_region))

        if visible_lines_len < MultipleSelectionScrollerCommand.MIN_NUM_VISIBLE_LINES:
            msg = "multiple_selection_scroller: too few visible lines"
            sublime.status_message(msg)
            return False

        # All OK.
        return True

    # End of def operational_status()


    def set_scroll_to(self, **kwargs):
        """
        set_scroll_to() sets the scroll_to instance variable according to the value held by
        "scroll_to" in the kwargs dictionary and sets the control_mode instance variable.
        """

        # Set the scroll_to arg name.
        scroll_to_arg_name = "scroll_to"

        # If available get the command's scroll_to arg from the kwargs dictionary.
        if scroll_to_arg_name in kwargs:
            scroll_to_arg_val = kwargs.get(scroll_to_arg_name)

        # The scroll_to arg is not in the dictionary.
        else:
            return

        # Convert to a string in case some other type was used in error and to lowercase.
        scroll_to_arg_val = str(scroll_to_arg_val)
        scroll_to_arg_val = scroll_to_arg_val.lower()

        # Set the scroll_to instance variable.

        if scroll_to_arg_val == "next":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_NEXT

        elif scroll_to_arg_val == "previous":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_PREVIOUS

        elif scroll_to_arg_val == "first":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_FIRST

        elif scroll_to_arg_val == "last":
            self.scroll_to = MultipleSelectionScrollerCommand.SCROLL_TO_LAST

        # "scroll_to" is set to an invalid value.
        else:
            return

        # Set the control_mode instance variable.
        self.control_mode = MultipleSelectionScrollerCommand.SCROLL_TO

    # End of def set_scroll_to()


    def set_clear_to(self, **kwargs):
        """
        set_clear_to() sets the clear_to instance variable according to the value held by
        "clear_to" in the kwargs dictionary and sets the control_mode instance variable.
        """

        # Set the clear_to arg name.
        clear_to_arg_name = "clear_to"

        # If available get the command's clear_to arg from the kwargs dictionary.
        if clear_to_arg_name in kwargs:
            clear_to_arg_val = kwargs.get(clear_to_arg_name)

        # The clear_to arg is not in the dictionary.
        else:
            return

        # Convert to a string in case some other type was used in error and to lowercase.
        clear_to_arg_val = str(clear_to_arg_val)
        clear_to_arg_val = clear_to_arg_val.lower()

        # Set the clear_to instance variable.

        if clear_to_arg_val == "first":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_FIRST

        elif clear_to_arg_val == "last":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_LAST

        elif clear_to_arg_val == "middle":
            self.clear_to = MultipleSelectionScrollerCommand.CLEAR_TO_MIDDLE

        # "clear_to" is set to an invalid value.
        else:
            return

        # Set the control_mode instance variable.
        self.control_mode = MultipleSelectionScrollerCommand.CLEAR_TO

    # End of def set_clear_to()


    def set_user_feedback(self, **kwargs):
        """
        set_user_feedback() sets the user_feedback instance variable to the value held by "feedback"
        in the kwargs dictionary, to the value held by the "MultipleSelectionScroller.feedback"
        setting in the user's settings file, or to the default, in that order of priority.
        """

        # Set the default.
        feedback_default = True

        # First check if the feedback arg was used in the command's args, this has top priority.

        # Set the feedback arg name.
        feedback_arg_name = "feedback"

        # If available get the command's feedback arg from the kwargs dictionary.
        if feedback_arg_name in kwargs:

            feedback_arg_val = kwargs.get(feedback_arg_name)

            # If the arg was assigned a boolean value, set user_feedback and return, all done.
            if isinstance(feedback_arg_val, bool):

                if feedback_arg_val:
                    self.user_feedback = MultipleSelectionScrollerCommand.FEEDBACK_VERBOSE
                    return
                else:
                    self.user_feedback = MultipleSelectionScrollerCommand.FEEDBACK_QUIET
                    return

        # If the feedback arg was not in the kwargs dictionary or not set to a boolean value,
        # then check if the user has used the feedback setting in their settings.

        # Set the feedback settings name.
        feedback_setting_name = "MultipleSelectionScroller.feedback"

        # Get the user's feedback setting, if not in settings then use the default.
        feedback_setting = self.view.settings().get(feedback_setting_name, feedback_default)

        # Check the setting was assigned a boolean value, if not then use the default.
        if not isinstance(feedback_setting, bool):
            feedback_setting = feedback_default

        # Finally set user_feedback.
        if feedback_setting:
            self.user_feedback = MultipleSelectionScrollerCommand.FEEDBACK_VERBOSE
        else:
            self.user_feedback = MultipleSelectionScrollerCommand.FEEDBACK_QUIET

    # End of def set_user_feedback()


    def control_scrolling(self):
        """
        control_scrolling() controls scrolling by calling the appropriate method depending on what
        value the scroll_to instance variable has been set to.

        This method also provides important notes about how this plugin handles the scrolling.
        """

        # Scrolling forwards - scroll_to_next_selection() - through the selections is done by moving
        # the first selection to occur below the middle line of the visible region to the middle
        # line of the visible region. If there is no selection below the middle line then cycling up
        # to the first selection is done.
        #
        # Scrolling backwards - scroll_to_previous_selection() -  through the selections is done by
        # moving the first selection to occur above the middle line of the visible region to the
        # middle line of the visible region. If there is no selection above the middle line then
        # cycling down to the last selection is done.
        #
        # Scrolling to the first and last selections simply moves the first or last selection to the
        # middle line of the visible region.
        #
        # Repeated pressing of the command's keys allow scrolling backwards and forwards through all
        # the selections.
        #
        # Scrolling is performed by calling view.show_at_center(point) - there are two cases when
        # Sublime Text will not honour calls made to that method and move the visible region:
        #
        # 1) If a selection is above the middle line on the first page of the buffer, Sublime Text
        # won't scroll the line it is on to the center of the visible region, there is no setting
        # for 'scroll_above_beginning' (I'd like to see that setting added).
        #
        # 2) If a selection is below the middle line on the last page of the buffer and the setting
        # 'scroll_past_end' has been set to false (defaults to true) then again Sublime Text won't
        # move the line it is on to the center of the visible region (however it will if the setting
        # 'scroll_past_end' is set to true).
        #
        # In both of these cases the next/previous selection will not be moved to the middle line
        # of the visible region, however all remaining selections whether below the middle line (if
        # scrolling forwards) or above the middle line (if scrolling backwards) will definitely be
        # in the visible region on the screen. The scroll to next/previous selection methods have
        # information about how scroll cycling is achieved in these cases.

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
        scroll_to_next_selection() moves the visible region to center on the first selection to
        occur below the middle_line region. If there is no such selection it moves the visible
        region to center on the first selection (i.e. cycles up to the first selection).
        """

        # Get the region of the middle line.
        middle_line = self.get_middle_line()

        # Get the viewport position. [Note: This is used to help with cycled scrolling.]
        vertical_axis_index = 1
        viewport_pos_before_centering = self.view.viewport_position()[vertical_axis_index]

        # Starting at the first selection, loop forwards through all the selections looking for the
        # first selection to occur below the middle line - if found center on that selection.

        sel_index = 0
        found = False

        while sel_index < self.sels_len and not found:

            sel = self.sels[sel_index]

            # If a selection is found below the middle line.
            if sel.begin() > middle_line.end():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # Give user feedback about the current selection scroll position.
                self.status_message_scroll_to(sel_index)

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
        # view.show_at_center() behaves; it sensibly centers the given region in the viewport but
        # this means that selections can still exist below the middle visible line although only on
        # the final page of the buffer. This is a known design limitation of the plugin, it can not
        # scroll lower than the first selection below the middle line on the buffer's final page,
        # but any such selections are guaranteed to be in the visible region, and cycled scrolling
        # can still be achieved by examining the viewport's vertical axis position, so this is a
        # minor limitation.

        # Check for cycled scrolling for selections below the middle line on the last page.

        # Get the viewport position.
        viewport_pos_after_centering = self.view.viewport_position()[vertical_axis_index]

        # If the viewport's vertical axis position is unchanged, cycle up to the first selection.
        # i.e. A selection was found below the middle line but the viewport position did not get
        # changed, so view.show_at_center() did not move the selection's line to the center,
        # therefore the selection must be below the middle line on the buffer's final page and it
        # can not be scrolled to, so cycle up to the first selection.

        if viewport_pos_before_centering == viewport_pos_after_centering:
            self.scroll_to_first_selection()

    # End of def scroll_to_next_selection()


    def scroll_to_previous_selection(self):
        """
        scroll_to_previous_selection() moves the visible region to center on the first selection to
        occur above the middle_line region. If there is no such selection it moves the visible
        region to center on the last selection (i.e. cycles down to the last selection).
        """

        # Get the region of the middle line.
        middle_line = self.get_middle_line()

        # Get the viewport position. [Note: This is used to help with cycled scrolling.]
        vertical_axis_index = 1
        viewport_pos_before_centering = self.view.viewport_position()[vertical_axis_index]

        # Starting at the last selection, loop backwards through all the selections looking for the
        # first selection to occur above the middle line - if found center on that selection.

        sel_index = self.sels_len - 1
        found = False

        while sel_index >= 0 and not found:

            sel = self.sels[sel_index]

            # If a selection is found above the middle line.
            if sel.end() < middle_line.begin():

                # Scroll the visible region to the line the selection begins on.
                self.view.show_at_center(sel.begin())

                # Give user feedback about the current selection scroll position.
                self.status_message_scroll_to(sel_index)

                # Quit loop.
                found = True

            sel_index -= 1

        # If no selection was found above the middle line, cycle down to the last selection.
        if not found:
            self.scroll_to_last_selection()
            return

        # IMPORTANT NOTE: Checking to see if the found variable is False can not always be relied on
        # for cycled scrolling because selections above the middle line on the first page of the
        # buffer do not trigger cycling down to the last selection. This is because of the way
        # view.show_at_center() behaves; it sensibly centers the given region in the viewport but
        # this means that selections can still exist above the middle visible line although only on
        # the first page of the buffer. This is a known design limitation of the plugin, it can not
        # scroll higher than selections on or below the middle line on the buffer's first page, but
        # any such selections are guaranteed to be in the visible region, and cycled scrolling can
        # still be achieved by examining the viewport's vertical axis position, so this is a minor
        # limitation.

        # Check for cycled scrolling for selections above the middle line on the first page.

        # Get the viewport position.
        viewport_pos_after_centering = self.view.viewport_position()[vertical_axis_index]

        # If the viewport's vertical axis position is unchanged, cycle down to the last selection.
        # i.e. A selection was found above the middle line but the viewport position did not get
        # changed, so view.show_at_center() did not move the selection's line to the center,
        # therefore the selection must be above the middle line on the buffer's first page and it
        # can not be scrolled to, so cycle down to the last selection.

        if viewport_pos_before_centering == viewport_pos_after_centering:
            self.scroll_to_last_selection()

    # End of def scroll_to_previous_selection()


    def scroll_to_first_selection(self):
        """
        scroll_to_first_selection() moves the visible region to center on the first selection.
        """

        sel_first_index = 0
        self.scroll_to_selection_index(sel_first_index)

    # End of def scroll_to_first_selection()


    def scroll_to_last_selection(self):
        """
        scroll_to_last_selection() moves the visible region to center on the last selection.
        """

        sel_last_index = self.sels_len - 1
        self.scroll_to_selection_index(sel_last_index)

    # End of def scroll_to_last_selection()


    def scroll_to_selection_index(self, sel_index):
        """
        scroll_to_selection_index() moves the visible region to center on the selection specified
        by sel_index.
        """

        # Scroll the visible region to the line of the selection.
        sel = self.sels[sel_index]
        self.view.show_at_center(sel.begin())

        # Give user feedback about the current selection scroll position.
        self.status_message_scroll_to(sel_index)

    # End of def scroll_to_selection_index()


    def control_clearing(self):
        """
        control_clearing() controls clearing the selections and leaving a cursor at the selection
        specified by the value of the clear_to instance variable.
        """

        # Set the index of the first selection.
        if self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_FIRST:
            sel_index = 0

        # Set the index of the last selection.
        elif self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_LAST:
            sel_index = self.sels_len - 1

        # Get the index of the selection nearest the middle visible line.
        elif self.clear_to == MultipleSelectionScrollerCommand.CLEAR_TO_MIDDLE:
            sel_index = self.get_selection_index_nearest_middle_line()

        # Get the chosen selection.
        sel = self.sels[sel_index]

        # Get the cursor position of the chosen selection.
        cursor_pos = sel.b

        # Clear the selections.
        self.sels.clear()

        # Add a new selection at the cursor position.
        self.sels.add(cursor_pos)

        # Move the view to center on the cursor position.
        self.view.show_at_center(cursor_pos)

        # Give user feedback about the selection clearing position.
        self.status_message_clear_to(sel_index)

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

        # Calculate the distance from the middle row to the row of the first selection below and
        # the first selection above.
        distance_to_first_below = sel_row_first_below - middle_line_row
        distance_to_first_above = middle_line_row - sel_row_first_above

        # Convert negative distances to positive (no selection below or above).
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

        # IMPORTANT NOTE: It is essential to the operation of this plugin that the middle line
        # calculated below corresponds exactly, or at least very closely, with the position used by
        # the Sublime View Class show_at_center() method when centering lines - if it does not then
        # scrolling can get 'stuck' on a selection.
        #
        # It has been established that subtracting 1 from odd numbers, before the division by 2,
        # works perfectly. When the number of visible lines is odd, there will be an equal number of
        # lines above and below the middle line, when the number of visible lines is even there will
        # be an extra line above. Consider the following (noting that visible_lines is 0 indexed):
        #
        # visible_lines_len = 10    ...    middle_line_num = 10 / 2 = 5
        # Indexes 0 to 4 == 5 (lines above middle_line)
        # Indexes 6 to 9 == 4 (lines below middle_line)
        #
        # visible_lines_len = 11    ...    middle_line_num = (11 - 1) / 2 = 5
        # Indexes 0 to 4  == 5 (lines above middle_line)
        # Indexes 6 to 10 == 5 (lines below middle_line)
        #
        # Regardless of this discrepancy it works flawlessly in both Sublime Text 2 and 3; however
        # getting it right did cause a few minor problems (rounding failed dismally), and a proper
        # explanation was thought worthy of inclusion to aid future development.

        # Get the visible region, the list of visible lines, and the number of visible lines.

        visible_region = self.view.visible_region()
        visible_lines = self.view.lines(visible_region)
        visible_lines_len = len(visible_lines)

        # Calculate which line is in the middle of the visible lines.

        # Subtract 1 from odd numbers only.
        if  visible_lines_len % 2 == 1:
            visible_lines_len -= 1

        middle_line_num = int(visible_lines_len / 2)

        # Return the region of the middle line.
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


    def status_message_scroll_to(self, sel_index):
        """
        status_message_scroll_to() displays a status message showing the scroll selection position.
        """

        # Don't display the status message if the user doesn't want feedback.
        if self.user_feedback == MultipleSelectionScrollerCommand.FEEDBACK_QUIET:
            return

        # sel_index is indexed from 0, add 1 for user readability.
        sel_index += 1

        # Build and display the user feedback status message.

        msg = "multiple_selection_scroller - scroll at selection: {0} of {1}"
        msg = msg.format(str(sel_index), str(self.sels_len))

        sublime.status_message(msg)

    # End of def status_message_scroll_to()


    def status_message_clear_to(self, sel_index):
        """
        status_message_clear_to() displays a status message showing the cleared selection position.
        """

        # Don't display the status message if the user doesn't want feedback.
        if self.user_feedback == MultipleSelectionScrollerCommand.FEEDBACK_QUIET:
            return

        # sel_index is indexed from 0, add 1 for user readability.
        sel_index += 1

        # Build and display the user feedback status message.

        msg = "multiple_selection_scroller - cleared at selection: {0} of {1}"
        msg = msg.format(str(sel_index), str(self.sels_len))

        sublime.status_message(msg)

    # End of def status_message_clear_to()

# End of class MultipleSelectionScrollerCommand()

