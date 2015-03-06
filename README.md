
## Multiple Selection Scroller - Plugin for Sublime Text v.2 and v.3


Multiple Selection Scroller is a Sublime Text plugin which provides commands to allow scrolling
forwards and backwards through the current selections by moving the visible region so that the
next/previous selection is centered on the middle line. Cycling from the last selection up to the
first and visa-versa is automatic. Commands to scroll straight to the first and to the last
selection complete its scrolling functionality.

Multiple Selection Scroller also provides commands to clear the selections whilst leaving a single
cursor at the first selection, at the last selection, or at the selection on, or nearest to, the
middle line (conceptually the 'current' selection or the one most recently scrolled to).

By default user feedback is given in the form of status messages. This tells the user which
selection has just been placed on the middle line if scrolling (e.g. "scroll at selection: 5 of
11"), or at which selection the cursor has been left if clearing the selections (e.g. "cleared at
selection: 3 of 5"). User feedback can be disabled.

Please be aware that there is a known design limitation of the plugin. Selections above the middle
line on the first page of the buffer can not be moved to the middle line, Sublime Text has no
'scroll_above_beginning' setting. If the 'scroll_past_end' setting is set to true, which it is by
default, then the first selection below the middle line on the last page of the buffer can be moved
to the middle line, but any subsequent selections can not be. In both cases any remaining selections
either above or below the middle line will be in the visible region on the screen. It should be
noted that this limitation does not intefere with scroll cycling which continues to work correctly.
[In real-world usage I have not found this inconvenient when it occurs, which is rarely.]


#### Requirements / Tested

- Sublime Text v.2 or v.3
- ST v.2 (Build 2221) - tested and fully working.
- ST v.3 (Build 3065) - tested and fully working.


#### Installation

Using [PackageControl](https://sublime.wbond.net) the Sublime Text Package Manager. Open the
`Command Palette` in Sublime Text and select `Package Control: Install Package` when the package
list has loaded just select `Multiple Selection Scroller`. [Note: This plugin has been submitted to
PackageControl but it may take a few days before it is available.]

Or install manually:

- Create a directory called `MultipleSelectionScroller` (or whatever you prefer) in your Sublime
  Text `Packages` directory.
- Put the files from this repository into that directory either by using `git` or by downloading and
  extracting the zip file on the [GitHub](https://github.com/mattst/sublime-multiple-selection-
  scroller) page.
- Clearly if you install manually then you will not receive automatic package updates.


#### Setup

The Multiple Selection Scroller plugin intentionally does not provide a keymap file to set its keys.
This is for two reasons; there are now so many plugins which the chosen keys could conflict with and
one of the key combinations (in the recommended keys) is dependant on the user's keyboard layout.

The '[' and ']' keys are already used for line indenting and code folding, using them for multi-
selection scrolling and clearing in various key combinations seems both convenient and appropriate.

The final command in the table below is to clear the selections leaving a cursor at the selection
on, or nearest to, the middle line. The 'recommended' keys are: `ctrl+k, ctrl+#` The '#' key was
chosen bacause on my UK keyboard it is to the right of the ']' key - it was chosen for the
convenience of its location. On a USA keyboard and some other locales the '/' key occupies the
position to the right of the ']' key. For that layout clearly the '/' key makes more sense to use
than '#'. Some users may prefer to keep the keys limited to just the '[' and ']' keys in which
case they could use, say, `ctrl+k, ctrl+shift+]`, it is a personal preference.

Recommended keys:

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

    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },


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


#### License

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
