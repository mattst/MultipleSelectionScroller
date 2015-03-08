
## Multiple Selection Scroller - Plugin for Sublime Text v.2 and v.3


### Features

A quick overview of what this plugin can do.

- Scroll to selection commands - center chosen selection on the middle line:
  1. Scroll to previous selection (backwards)
  2. Scroll to next selection (forwards)
  3. Scroll to first selection
  4. Scroll to last selection
- Clear to selection commands - clear all selections leaving a single cursor at:
  1. Clear to first selection
  2. Clear to last selection
  3. Clear to selection on, or nearest to, the middle line
- Automatic scroll cycling, from last selection to first and visa-versa.
- User feedback status messages, e.g. *scroll at selection: 5 of 11* or *cleared at selection: 3 of 5*

### Description

Multiple Selection Scroller is a Sublime Text plugin which provides commands to allow scrolling
forwards and backwards through the current selections by moving the visible region so that the
next/previous selection is centered on the middle line. Cycling from the last selection up to the
first and visa-versa is automatic. Commands to scroll straight to the first and to the last
selection complete its scrolling functionality.

Multiple Selection Scroller also provides commands to clear the selections whilst leaving a single
cursor at the first selection, at the last selection, or at the selection on, or nearest to, the
middle line (conceptually the *current* selection or the one most recently scrolled to).

By default user feedback is given in the form of status messages. This tells the user which
selection has just been placed on the middle line if scrolling (e.g. *scroll at selection: 5 of
11*), or at which selection the cursor has been left if clearing the selections (e.g. *cleared at
selection: 3 of 5*).

The plugin has settings to disable user feedback status messages and to prevent scroll cycling.

### Known Design Limitation (not a bug)

Please be aware that there is a known design limitation of the plugin. Selections above the middle
line on the first page of the buffer can not be moved to the middle line, Sublime Text has no
`scroll_above_beginning` setting. If the `scroll_past_end` setting is set to true, which it is by
default, then the first selection below the middle line on the last page of the buffer can be moved
to the middle line, but any subsequent selections can not be. In both cases any remaining selections
either above or below the middle line will be in the visible region on the screen and highlighted so
easy to spot. It should be noted that this limitation does not intefere with scroll cycling which
continues to work correctly. [In real-world usage I have not found this inconvenient when it occurs,
which is rarely.]


### Requirements / Tested

- Sublime Text v.2 or v.3
- ST v.2 (Build 2221) - tested and fully working.
- ST v.3 (Build 3065) - tested and fully working.


### Installation

Using [PackageControl](https://sublime.wbond.net) the Sublime Text Package Manager. Open the
`Command Palette` in Sublime Text and select `Package Control: Install Package`. When the package
list has loaded just select `Multiple Selection Scroller`. [Note: This plugin has been submitted to
PackageControl but it may take a few days before it is available.]

Or install manually:

- Create a directory called `MultipleSelectionScroller` (or whatever you prefer) in your Sublime
  Text `Packages` directory.
- Put the files from this repository into that directory either by using `git` or by downloading
  the zip file on the [GitHub](https://github.com/mattst/sublime-multiple-selection-
  scroller) page, [direct link](https://github.com/mattst/sublime-multiple-selection-
  scroller). Sublime Text v.2 users will need to extract the files from the zip file.
- Clearly if you install manually then you will not receive automatic package updates.


### Setup — Settings

The Multiple Selection Scroller plugin has two optional settings with which the plugin's default
behaviour can be changed.

- By default, when scrolling, the plugin will cycle from the last selection up to the first, and
from the first down to the last. This can be disabled by setting the
`MultipleSelectionScroller.scroll_cycling` setting to `false`.
- By default user feedback is given in the form of status messages. This can be disabled by
setting the `MultipleSelectionScroller.quiet` setting to `true`.

Add these settings to the `Preferences.sublime-settings` file to disable scroll cycling or status
messages.

    // Disable scroll cycling:
    "MultipleSelectionScroller.scroll_cycling": false,

    // Disable user feedback status messages:
    "MultipleSelectionScroller.quiet": true,


### Setup — Keys

The Multiple Selection Scroller plugin does not provide a keymap file to set its keys. Choosing keys
that will suit all users is not possible - the chosen keys will always interfere with the existing
keys of some users. Various suggested key mappings are shown below - these can be copied and pasted
into your `Default (OS).sublime-keymap` file and altered to suit your configuation.

The `[` and `]` square bracket keys are already used for line indenting and code folding, using them
for multi-selection scrolling and clearing in various key combinations seems both convenient and
appropriate.


#### Suggested Keys Linux/Windows - Minimal Setup:

Notes:

- The commands most often used are: scroll to next selection, scroll to previous selection, clear
to last selection, and clear to selection on (or nearest to) the middle line. Below is an example
of what you could use for just those commands.
- The clearing commands below use `alt+k` as a key chord, e.g. `"alt+k", "alt+["`. This is so that
the common process of scrolling to the desired selection and then clearing at that selection can
be achieved without taking your finger off the `alt` key. Clearly these can easily be changed to
use `ctrl+k`, e.g. `"ctrl+k", "ctrl+["`.

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
    { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },


#### Suggested Keys OS X - Minimal Setup:

Notes:

- The commands most often used are: scroll to next selection, scroll to previous selection, clear
to last selection, and clear to selection on (or nearest to) the middle line. Below is an example
of what you could use for just those commands.
- Choosing commands for OS X having never used Sublime Text on OS X is difficult. I've examined
the `Default (OSX).sublime-keymap` file and chosen appropriate key combinations that are not used
in that file.

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["super+k", "super+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
    { "keys": ["super+k", "super+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },

Mac Key Notes:

Option+<alphanum> should not be used on any OS X key bindings (inserts non-ascii characters)

Note: Option == Alt

Indent line(s) (custom code see below)      Command + ]
Unindent line(s) (custom code see below)    Command + [
Fold                                        Command + Option + [
UnFold                                      Command + Option + ]
Comment line (custom code see below)        Command + \
Block Comment line (custom code see below)  Command + Shift + \

sublime text "Default (OSX).sublime-keymap"
https://github.com/d2s/Sublime-Text-2-User-Settings/blob/master/Default%20%28OSX%29.sublime-keymap

    { "keys": ["super+shift+["], "command": "prev_view" },
    { "keys": ["super+shift+]"], "command": "next_view" },

    { "keys": ["super+]"], "command": "indent" },
    { "keys": ["super+["], "command": "unindent" },

    { "keys": ["super+alt+["], "command": "fold" },
    { "keys": ["super+alt+]"], "command": "unfold" },



#### Suggested Keys Linux/Windows - Full Setup #1:

Notes:

- The clearing commands below do not use a modifier key for the 2nd keypress, e.g. `"alt+k", "["`.
This is done so that all the command's keys can use a single modifier key `alt`. If you don't like
that there are alternative suggestions below.
- In fact it is not quite a "Full Setup", clearing to the first selection is not set. As you know
pressing `escape` will do this. Using `"clear_to": "first"` differs only in that when clearing to
the first selection only the cursor remains at the first selection, rather than the first selection
remaining fully selected which is what pressing `escape` will do. If you want that functionality
add a key. [For clearing, I use `[` to first, `]` to last, `#` to middle - note `#` is to the right
of `]` on my keyboard layout although on most keyboards `\` is in that position. Hint: If using `\`
then that key needs to be escaped in the binding, e.g. `"alt+k", "\\"`.

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },
    { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first"} },
    { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["alt+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
    { "keys": ["alt+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },


#### Suggested Keys Linux/Windows - Full Setup #2:

Notes:

- If you do not like the way Setup #1 does not use a modifier key for the 2nd keypress, here is an
alternative.

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },
    { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first"} },
    { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "first"} },
    { "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },
    { "keys": ["ctrl+k", "ctrl+\\"], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },








    --------------------------------------------------------------------------------------
    scroll_to commands move the visible region centering the selection on the middle line.
    --------------------------------------------------------------------------------------
    Description                                    Arg          Value       Keys
    --------------------------------------------------------------------------------------
    Scroll to previous selection (backwards)       scroll_to    previous    alt+[
    Scroll to next selection (forwards)            scroll_to    next        alt+]
    Scroll to first selection                      scroll_to    first       alt+k,  alt+[
    Scroll to last selection                       scroll_to    last        alt+k,  alt+]

    --------------------------------------------------------------------------------------
    clear_to commands clear the selections leaving a single cursor at the chosen location.
    --------------------------------------------------------------------------------------
    Description                                    Arg          Value       Keys
    --------------------------------------------------------------------------------------
    Clear to first selection                       clear_to     first       ctrl+k, ctrl+[
    Clear to last selection                        clear_to     last        ctrl+k, ctrl+]
    Clear to selection (on/nearest) middle line    clear_to     middle      ctrl+k, ctrl+#
    --------------------------------------------------------------------------------------
    Alternative suggestions for: Clear to selection (on/nearest) middle line
    --------------------------------------------------------------------------------------
    ctrl+k, ctrl+/    ctrl+k, ctrl+shift+]    ctrl+k, ]    alk+k, ]
    --------------------------------------------------------------------------------------



### Reference

#### Command and Agruments:

    Command name: multiple_selection_scroller

    Either a scroll_to or a clear_to arg MUST be used in the command call.

    scroll_to - move the visible region centering the selection on the middle line.
    -------------------------------------------------------------------------------
    Command Arg      Value                 Description
    -------------------------------------------------------------------------------
    scroll_to        previous      Scroll to previous selection (backwards)
    scroll_to        next          Scroll to next selection (forwards)
    scroll_to        first         Scroll to first selection
    scroll_to        last          Scroll to last selection

    clear_to - clear the selections leaving a single cursor at the chosen location.
    -------------------------------------------------------------------------------
    Command Arg      Value                 Description
    -------------------------------------------------------------------------------
    clear_to         first         Clear to first selection
    clear_to         last          Clear to last selection
    clear_to         middle        Clear to selection on/nearest the middle line
    -------------------------------------------------------------------------------

#### Settings File:

    Two settings may optionally be used in the Preferences.sublime-settings file.

    MultipleSelectionScroller.quiet - control user feedback status messages.
    -------------------------------------------------------------------------------------
    Setting                                    Value         Description
    -------------------------------------------------------------------------------------
    MultipleSelectionScroller.quiet            true     Do not display status messages
    MultipleSelectionScroller.quiet            false    Display status messages (default)
    -------------------------------------------------------------------------------------

    MultipleSelectionScroller.scroll_cycling - control scroll cycling.
    -------------------------------------------------------------------------------------
    Setting                                    Value         Description
    -------------------------------------------------------------------------------------
    MultipleSelectionScroller.scroll_cycling   true     Enable scroll cycling (default)
    MultipleSelectionScroller.scroll_cycling   false    Disable scroll cycling








Mac Key Notes:

Option+<alphanum> should not be used on any OS X key bindings (inserts non-ascii characters)

Note: Option == Alt

Indent line(s) (custom code see below)      Command + ]
Unindent line(s) (custom code see below)    Command + [
Fold                                        Command + Option + [
UnFold                                      Command + Option + ]
Comment line (custom code see below)        Command + \
Block Comment line (custom code see below)  Command + Shift + \


User feedback can be disabled either with the use of a command argument or by
adding a setting to the `Preferences.sublime-settings file`.


Scroll to first/last using "alt+k", "alt+[" and "alt+k", "alt+]":

{ "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first"} },
{ "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last"} },

clear to first/last/middle using ctrl+k", "ctrl+[", "ctrl+k", "ctrl+]", and "ctrl+k", "ctrl+#":
{ "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "first"} },
{ "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },
{ "keys": ["ctrl+k", "ctrl+#"], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },

clear to middle (duplication) using "alt+k", "alt+#":
[clearing to middle is often used during scrolling, so using "alt+k" rather than moving the key
being held down to "ctrl" is both convenient and quicker.]

{ "keys": ["alt+k", "alt+#"], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },

the use of '#' in the two 'clear to middle' examples above is because the '#' key is to the right
of the ']' key on my (british) keyboard. on a usa keyboard the '\' key occupies that position, so
that should be substituted for '#'. on some mac keyboards there is no key at all on the right of
the ']' key. of course, these are just suggestions, use whatever you want. :)

Add the following keys line to your user Key Bindings file, altering the actual
keys specified below to whatever key combination you want to use. `ctrl+shift+b`
are the keys which I use (*Build - Run*, by default) but my build keys have been
changed to keys that suit me better.

    {"keys": ["ctrl+shift+b"], "command": "swap_boolean_polarity" },

I hope you find Multiple Selection Scroller useful.


### License

The MIT License (MIT)

Copyright (c) 2015 mattst@i-dig.info / https://github.com/mattst

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
