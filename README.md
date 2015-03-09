
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
- Automatic scroll cycling, from last selection to first and visa-versa
- User feedback status messages, e.g. *scroll at selection: 5 of 11* or *cleared at selection: 3 of 5*


### Description

Multiple Selection Scroller is a Sublime Text plugin which provides commands to allow scrolling
forwards and backwards through the current selections by moving the visible region so that the
next/previous selection is centered on the middle line. Cycling from the last selection up to the
first and visa-versa is automatic. Commands to scroll straight to the first and to the last
selection complete its scrolling functionality.

Multiple Selection Scroller also provides commands to clear the selections whilst leaving a single
cursor at the first selection, at the last selection, or at the selection on, or nearest to, the
middle line (conceptually the 'current' selection / the one you just scrolled to).

By default user feedback is given in the form of status messages. This tells the user which
selection has just been placed on the middle line if scrolling (e.g. *scroll at selection: 5 of
11*), or at which selection the cursor has been left if clearing the selections (e.g. *cleared at
selection: 3 of 5*).

The plugin has settings to disable user feedback status messages and to prevent scroll cycling.


### Known Design Limitation (Not a Bug)

Please be aware that there is a known design limitation of the plugin. Selections above the middle
line on the first page of the buffer can not be moved to the middle line, Sublime Text has no
`scroll_above_beginning` setting. If the `scroll_past_end` setting is set to true, which it is by
default, then the first selection below the middle line on the last page of the buffer can be moved
to the middle line, but any subsequent selections can not be. In both cases any remaining selections
either above or below the middle line will be in the visible region on the screen and highlighted so
easy to spot. It should be noted that this limitation does not interfere with scroll cycling which
continues to work correctly. [In real-world usage I have not found this inconvenient when it occurs,
which is rarely.]


### Demo

The scrolling in this demo does not appear very smooth, this is because a low frame rate was used
to keep this file size down.

The demo shows both selection scrolling and selection clearing functionality.

![Demo](http://picsee.net/upload/2015-03-09/96e742c55eff.gif)


### Requirements / Tested

- Sublime Text v.2 or v.3
- ST v.2 (Build 2221) - tested and working.
- ST v.3 (Build 3065) - tested and working.
- The plugin should work with all v.2 and v.3 releases.


### Installation

Using [PackageControl](https://sublime.wbond.net) the Sublime Text Package Manager. Open the
`Command Palette` in Sublime Text and select `Package Control: Install Package`. When the package
list has loaded just select `Multiple Selection Scroller`.  *[Note: This plugin has been submitted
to PackageControl but it may take a few days before it is available.]*

Or install manually:

- Create a directory called `MultipleSelectionScroller` (or whatever you prefer) in your Sublime
  Text `Packages` directory.
- Put the files from this repository into that directory either by using `git` or by downloading
  the zip file on the [GitHub](https://github.com/mattst/sublime-multiple-selection-
  scroller) page, [direct link to zip](https://github.com/mattst/sublime-multiple-selection-
  scroller). Sublime Text v.2 users must extract the files from the zip file, those using v.3
  can simply rename the file replacing `.zip` with `.sublime-package` or extract the files if
  preferred.
- Clearly if you install manually then you will not receive automatic package updates.
- If you are concerned that a keys file will be added that will interfere with your config, be
assured that no `Default (OS).sublime-keymap` will ever be added to the package.


### Setup — Settings

The Multiple Selection Scroller plugin has two optional settings with which the plugin's default
behaviour can be changed.

- By default, when scrolling, the plugin will cycle from the last selection up to the first, and
from the first down to the last. This can be disabled by setting the
`MultipleSelectionScroller.scroll_cycling` setting to `false`.
- By default user feedback is given in the form of status messages. This can be disabled by
setting the `MultipleSelectionScroller.quiet` setting to `true`.

Add these settings to your `Preferences.sublime-settings` file:

    // Disable scroll cycling:
    "MultipleSelectionScroller.scroll_cycling": false,

    // Disable user feedback status messages:
    "MultipleSelectionScroller.quiet": true,


### Setup — Keys

The Multiple Selection Scroller plugin does not provide a keymap file to set its keys. Choosing keys
that will suit all users is not possible - the chosen keys will always interfere with the existing
keys of some users. Various suggested key mappings are shown below - these can be copied and pasted
into your `Default (OS).sublime-keymap` file and altered to suit your configuration.

The `[` and `]` square bracket keys are already used for line indenting and code folding, using them
for multi-selection scrolling and clearing in various key combinations seems both convenient and
appropriate.


**Suggested Keys Linux/Windows - Minimal Setup:**

Notes:

- The commands most often used are: *scroll to next selection*, *scroll to previous selection*, *clear
to last selection*, and *clear to selection on (or nearest to) the middle line*. Below is an example
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


**Suggested Keys OS X - Minimal Setup:**

Notes:

- The commands most often used are: *scroll to next selection*, *scroll to previous selection*, *clear
to last selection*, and *clear to selection on (or nearest to) the middle line*. Below is an example
of what you could use for just those commands.
- Choosing keys for OS X having never used Sublime Text on OS X is quite difficult. I've examined
the `Default (OSX).sublime-keymap` file and chosen appropriate key combinations that are not used
in that file.

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["super+k", "super+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
    { "keys": ["super+k", "super+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },


**Suggested Keys Linux/Windows - Full Setup #1:**

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


**Suggested Keys Linux/Windows - Full Setup #2:**

Notes:

- Please read the notes in **Full Setup #1**.
- If you do not like the way **Full Setup #1** does not use a modifier key for the 2nd keypress,
here is an alternative.

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },
    { "keys": ["alt+k", "alt+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first"} },
    { "keys": ["alt+k", "alt+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["ctrl+k", "ctrl+["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
    { "keys": ["ctrl+k", "ctrl+]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },


**Suggested Keys OS X - Full Setup:**

- The clearing commands below do not use a modifier key for the 2nd keypress, e.g. `"super+k", "["`.
This is done so that the number of different keys in use can be kept to a minimum.
- Please read the notes in **Linux/Windows - Full Setup #1** about it being **not quite a "Full
Setup"**.
- There is only one set of suggested keys for OS X Full Setup - choosing keys for OS X having never
used Sublime Text on OS X is quite difficult (as already stated).

e.g.

    // Multiple Selection Scroller - Scrolling:
    { "keys": ["ctrl+shift+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "previous"} },
    { "keys": ["ctrl+shift+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "next"} },
    { "keys": ["super+k", "super+["], "command": "multiple_selection_scroller", "args": {"scroll_to": "first"} },
    { "keys": ["super+k", "super+]"], "command": "multiple_selection_scroller", "args": {"scroll_to": "last"} },

    // Multiple Selection Scroller - Clearing:
    { "keys": ["super+k", "["], "command": "multiple_selection_scroller", "args": {"clear_to": "middle"} },
    { "keys": ["super+k", "]"], "command": "multiple_selection_scroller", "args": {"clear_to": "last"} },


### Reference

**Command and Agruments:**

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

**Settings File:**

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
