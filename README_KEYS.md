
## Multiple Selection Scroller - Plugin for Sublime Text v2 and v3


## Setup — Keys

The Multiple Selection Scroller plugin does not provide a keymap file to set its keys. Choosing keys that will suit all users is not possible - the chosen keys will always interfere with the existing keys of some users.

Instead various suggested key mappings are shown below - these can be copied and pasted into your user `Default (OS).sublime-keymap` file and altered to suit your configuration.

The suggested key bindings below all use the `[` and `]` square bracket keys in a variety of key combinations for the plugin's various commands. The square bracket keys are already used for line indenting and code folding, using them for multiple selection scrolling and clearing seems both convenient and appropriate.

In some of the examples below there are key chords which do not use a modifier key for the second keypress, e.g. `"ctrl+k", "["`. Quite a lot of Sublime Text users are unaware that this can be done. It is a useful alternative to creating more and more complex key modifier chord sequences.

In some of the Linux/Windows examples `alt+k` is used as a key chord, e.g. `"alt+k", "alt+["`, in the clearing commands. This is so that the common process of scrolling to the desired selection and then clearing at that selection can be achieved without taking your finger off the `alt` key. Clearly these can easily be changed to use `ctrl+k`, e.g. `"ctrl+k", "ctrl+["` if you don't want to use `alt+k` as a key chord, as is shown in some of the other examples.

Users may want to consider utilizing whatever key is to the right of the `]` key on their keyboard, `#` in the UK, `\` in the US. I use that key for clearing the `visible_area`. None of the examples below demonstrate this because the key in that position varies quite a lot depending on the keyboard layout, and on laptops there is often no key there at all.

Only the '*Totally Full Setup*' in the examples below implements the clearing to the first selection command, `{"clear_to": "first_sel"}`. Clearing to the first selection is not really needed because you can just press the `escape` key. It has only been included in the plugin's functionality to allow users to assign that task to the same key groupings as the other selection scrolling commands and to avoid the complex context based bindings associated with the `escape` key which are in the system default `.sublime-keymap` file.

Choosing keys for OS X having never used Sublime Text on OS X is quite difficult. I have examined the `Default (OSX).sublime-keymap` file and chosen appropriate key combinations that are not used in that file. If they are not brilliantly chosen then my apologies to OS X users. Please feel free to create an issue on the GitHub page and place a comment or make alternative suggestions.


### Reference

Here is a table showing what all of the command argument and value pairings do.

    Command name: multiple_selection_scroller

    Either a scroll_to or a clear_to arg MUST be used in the command call.

    scroll_to - move the visible region centering the selection on the middle line.
    -------------------------------------------------------------------------------------
    Command Arg      Value                       Description
    -------------------------------------------------------------------------------------
    scroll_to        previous_sel      Scroll to previous selection (backwards)
    scroll_to        next_sel          Scroll to next selection (forwards)
    scroll_to        first_sel         Scroll to first selection
    scroll_to        last_sel          Scroll to last selection

    clear_to - clear the selections leaving a single cursor at the chosen location.
    -------------------------------------------------------------------------------------
    Command Arg      Value                       Description
    -------------------------------------------------------------------------------------
    clear_to         first_sel         Clear to first selection
    clear_to         last_sel          Clear to last selection
    clear_to         middle_sel        Clear to selection on/nearest the middle line
    clear_to         visible_area      Clear to the middle line of the visible region
                                       (regardless of selections, clear to current pos)
    -------------------------------------------------------------------------------------


### Minimal Setup

The Multiple Selection Scroller plugin has 8 different command argument and value pairings, quite a lot of new keys to add at once and remember.

Some users will not want to use all of the plugin's functionality. For instance the keys to scroll directly to the first and last selections can be omitted (although they can be useful) because you can get to those selections by repeated pressing of the scroll to the previous and next selection keys.

The commands most often used are:

- Scroll to previous selection
- Scroll to next selection
- Clear to last selection
- Clear to selection on, or nearest to, the middle line (conceptually the '*current*' selection)
- Clear to middle line of visible area (ignore selection positions, just put cursor on middle line)

Here are examples of what you could use for just those commands.

**Suggested Keys Linux/Windows - Minimal Setup #1:**

    // Scrolling to selections:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },

    // Clearing at selections:
    { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },
    { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["alt+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },

**Suggested Keys Linux/Windows - Minimal Setup #2:**

Note: No `alt+k` key chording.

    // Scrolling to selections:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },

    // Clearing at selections:
    { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },
    { "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["ctrl+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },

**Suggested Keys OS X - Minimal Setup:**

    // Scrolling to selections:
    { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },

    // Clearing at selections:
    { "keys": ["super+k", "super+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },
    { "keys": ["super+k", "super+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["super+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },


### Full Setup

Not quite a 'Full Setup' - in the example key bindings below only 'Totally Full Setup' implements the clearing to the first selection command. It is not really needed as you can just press the `escape` key. However if you want to have that functionality in the same key groupings as the other selection commands, then just add a key binding which sets `{"clear_to": "first_sel"}`, see '*Totally Full Setup*'.

**Suggested Keys Linux/Windows - Full Setup #1:**

    // Scrolling to selections:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },
    { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first_sel"} },
    { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last_sel"} },

    // Clearing at selections:
    { "keys": ["alt+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },
    { "keys": ["alt+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },

**Suggested Keys Linux/Windows - Full Setup #2:**

Note: No `alt+k` key chording.

    // Scrolling to selections:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },
    { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first_sel"} },
    { "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last_sel"} },

    // Clearing at selections:
    { "keys": ["ctrl+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },
    { "keys": ["ctrl+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["ctrl+k", "ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },

**Suggested Keys OS X - Full Setup:**

    // Scrolling to selections:
    { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },
    { "keys": ["super+k", "super+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first_sel"} },
    { "keys": ["super+k", "super+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last_sel"} },

    // Clearing at selections:
    { "keys": ["super+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },
    { "keys": ["super+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["super+k", "super+shift+["], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },

**Suggested Keys Linux/Windows - Totally Full Setup:**

Note: No `alt+k` key chording.

    // Scrolling to selections:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },
    { "keys": ["ctrl+k", "ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first_sel"} },
    { "keys": ["ctrl+k", "ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last_sel"} },

    // Clearing at selections:
    { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "first_sel"} },
    { "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },
    { "keys": ["ctrl+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["ctrl+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },

**Suggested Keys OS X - Totally Full Setup:**

    // Scrolling to selections:
    { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous_sel"} },
    { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next_sel"} },
    { "keys": ["super+k", "super+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first_sel"} },
    { "keys": ["super+k", "super+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last_sel"} },

    // Clearing at selections:
    { "keys": ["super+k", "super+["], "command": "multiple_selection_scroller", "args": {"clear_to": "first_sel"} },
    { "keys": ["super+k", "super+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last_sel"} },
    { "keys": ["super+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle_sel"} },

    // Clearing at middle line of visible area (regardless of selections, clear to current pos):
    { "keys": ["super+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "visible_area"} },
