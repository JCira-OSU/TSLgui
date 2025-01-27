# TSLgui

A gui frontend for [TSLgenerator](https://github.com/alexorso/tslgenerator/).

## Installation

### Windows

Simply `git clone` and you're ready to run `TSLgui.py`. If you wish to use a
different instance of TSLgui per-project, you can copy TSLgui.py to your
project folder.

### Linux / Mac

Follow above steps, but you must also install tk/tcl. You can do this
either from your distribution's repositories (on Linux), brew, or with python's pip

> [!IMPORTANT]
> The directory `./data/` MUST exist relative to `TSLgui.py`  
> If this name conflicts with a project folder, you can change the paths in
> `TSLgui.py` lines 17-19.

## Usage

1. Paste the path to the TSLgenerator binary for your OS in the top box labeled
   'Enter path to binary'.
2. Press <Return/Enter>
3. If the file path is good (check spelling and executable status),
   then both 'Binary OK' and a 'Generate!' button will appear.
4. Write your TSLgenerator specs in this left column.
5. Click 'Generate!'
6. Your specs will be written to `./data/specs.txt` before being passed to the
   specified binary from step 1. The output of TSLgenerator will then be written
   to `./data/specs.tsl.txt` and then appear in the right column.

All stdout from TSLgenerator will be captured and displayed in
the in-window console, including all errors.

Your most recent input file, output file, and binary path will be
remembered and restored upon relaunching `TSLgui.py`! As stated above, this
data is kept in `./data/`

> [!TIP]
> After you input your binary path, you can also click 'Show Manpage' to
> see TSLgenerator's manpage.
