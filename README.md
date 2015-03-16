
## Multiple Selection Scroller - Plugin for Sublime Text


### Features

A summary of what this plugin can do:

- Compatible with Sublime Text v.2 and v.3
- Scroll to selection commands - center chosen selection on the middle line:
  1. Scroll to previous selection (backwards)
  2. Scroll to next selection (forwards)
  3. Scroll to first selection
  4. Scroll to last selection
- Automatic scroll cycling, from last selection to first and visa-versa
- Clear to selection commands - clear all selections leaving a single cursor at:
  1. Clear to first selection (not really needed, see '*Description*' section)
  2. Clear to last selection
  3. Clear to selection on, or nearest to, the middle line (conceptually the '*current*' selection)
  4. Clear to middle line of visible area (ignore selection positions, just put cursor on middle line)
- User feedback status messages, e.g. *"scroll at selection: 5 of 11"* or *"cleared at selection: 3 of 5"*
- Settings to disable user feedback status messages and to prevent scroll cycling


### Description

Multiple Selection Scroller is a Sublime Text plugin which provides commands to allow scrolling forwards and backwards through the current selections by moving the visible region so that the next/previous selection is centered on the middle line. Cycling from the last selection up to the first and visa-versa is automatic. Commands to scroll straight to the first and to the last selection complete its scrolling functionality.

Multiple Selection Scroller also provides commands to clear the selections whilst leaving a single cursor at the first selection, at the last selection, or at the selection on, or nearest to, the middle line (conceptually the '*current*' selection / the one you just scrolled to) and moving the visible region so that the single cursor is centered on the middle line. It also has a command to clear the selections whilst leaving a single cursor at the end of the middle line of the visible region (this ignores the positions of the selections and does not move the visible region) - in other words clear the selections and leave a cursor on the middle line of the current scroll position.

Note: Clearly the selection clearing command which leaves a cursor at the first selection is not really needed as the same thing is performed by pressing the `escape` key. It has only been included in the plugin's functionality to allow users to assign that task to the same key groupings as the other selection scrolling commands and to avoid the complex context based bindings associated with the `escape` key which are in the system default `.sublime-keymap` file.

User feedback is given in the form of status messages. This tells the user which selection has just been placed on the middle line if scrolling (e.g. *"scroll at selection: 5 of 11"*), or at which selection the cursor has been left if clearing the selections (e.g. *"cleared at selection: 3 of 5"*).

The plugin has settings to disable user feedback status messages and to prevent scroll cycling.


### Known Design Limitation (Not a Bug)

Please be aware that there is a known design limitation of the plugin. Selections above the middle line on the first page of the buffer can not be moved to the middle line, Sublime Text has no `scroll_above_beginning` setting. If the `scroll_past_end` setting is set to true, which it is by default, then the first selection below the middle line on the last page of the buffer can be moved to the middle line, but any subsequent selections can not be. In both cases any remaining selections either above or below the middle line will be in the visible region on the screen so easy to spot. It should be noted that this limitation does not interfere with scroll cycling which continues to work correctly. [*In real-world usage I have not found this inconvenient when it occurs, which is rarely.*]


### Demo

The scrolling in this demo does not appear very smooth, this is because a low frame rate was used to keep the demo's file size down. The scrolling performed by the plugin is done by Sublime Text and it will be just as smooth as your usual scrolling is.

The demo shows both selection scrolling and selection clearing functionality.

![Demo](https://cloud.githubusercontent.com/assets/835623/6656762/542d4362-cb2c-11e4-812c-43d9e75591ad.gif)


### Requirements / Tested

- Sublime Text v.2 or v.3
- Tested using: ST v.2 Build 2221 (Linux 64 bit).
- Tested using: ST v.3 Build 3065 (Linux 64 bit).


### Installation

Recommended: Using [PackageControl](https://sublime.wbond.net) the *Sublime Text Package Manager*.

- Open the `Command Palette` in Sublime Text and select `Package Control: Install Package`.
- When the package list has loaded, select `MultipleSelectionScroller`.

Not Recommended: Install Manually:

- Create a directory called `MultipleSelectionScroller` (or whatever you prefer) in your Sublime Text `Packages` directory.
- Put the files from this repository into that directory either by using `git` or by downloading the zip file on the [GitHub](https://github.com/mattst/MultipleSelectionScroller) page.
- Sublime Text v.2 users must extract the files from the zip file.
- Sublime Text v.3 users can simply rename the file replacing `.zip` with `.sublime-package` or extract the files if preferred.
- Clearly if you install manually then you will not receive automatic package updates, inconvenient if a bug is found.
- Note: If you are concerned that a keys file will be added that will interfere with your config, be assured that no `.sublime-keymap` will ever be added to this package.


### Setup — Settings

The Multiple Selection Scroller plugin has two optional settings with which the plugin's default behaviour can be altered.

- By default, when scrolling, the plugin will cycle from the last selection up to the first, and from the first down to the last. This can be disabled by setting the `MultipleSelectionScroller.scroll_cycling` setting to `false`.
- By default user feedback is given in the form of status messages. This can be disabled by setting the `MultipleSelectionScroller.quiet` setting to `true`.

e.g. Add these settings to your `Preferences.sublime-settings` file:

    // Disable scroll cycling:
    "MultipleSelectionScroller.scroll_cycling": false,

    // Disable user feedback status messages:
    "MultipleSelectionScroller.quiet": true,


### Setup — Keys

The Multiple Selection Scroller plugin does not provide a `.sublime-keymap` file to set its keys.

Choosing keys that will suit all users is not possible - the chosen keys will always interfere with the existing keys of some users. The `README_KEYS.md` file, linked below, contains suggestions and examples of various key bindings that can be copied and pasted into your user `Default (OS).sublime-keymap` file and altered to suit your configuration.

Please follow this link to read the [README_KEYS.md](https://github.com/mattst/MultipleSelectionScroller/blob/master/README_KEYS.md) file.


### Reference

**Command and Arguments:**

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

**Settings File:**

    Two settings may optionally be used in the Preferences.sublime-settings file.

    MultipleSelectionScroller.quiet - control user feedback status messages.
    -------------------------------------------------------------------------------------
    Setting                                    Value           Description
    -------------------------------------------------------------------------------------
    MultipleSelectionScroller.quiet            true     Do not display status messages
    MultipleSelectionScroller.quiet            false    Display status messages (default)
    -------------------------------------------------------------------------------------

    MultipleSelectionScroller.scroll_cycling - control scroll cycling.
    -------------------------------------------------------------------------------------
    Setting                                    Value           Description
    -------------------------------------------------------------------------------------
    MultipleSelectionScroller.scroll_cycling   true     Enable scroll cycling (default)
    MultipleSelectionScroller.scroll_cycling   false    Disable scroll cycling


### License

The MIT License (MIT)

Copyright (c) 2015 mattst@i-dig.info / https://github.com/mattst

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
