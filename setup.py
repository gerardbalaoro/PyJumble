"""Disutils Setup Script"""
import cx_Freeze, os.path 

PYTHON_INSTALL_DIR          = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY']   = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY']    = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6') 


executables = [
    cx_Freeze.Executable(
        script          = 'main.py',
        base            = 'Win32GUI', 
        targetName      = 'pyjumble.exe',
        icon            = 'assets/images/icon.ico',
        copyright       = 'Copyright (c) 2018 Gerard Balaoro',
        shortcutName    = 'PyJumble'
    )
]

shortcut_table = [
    (
        'DesktopShortcut',        # Shortcut
        'DesktopFolder',          # Directory_
        'PyJumble',               # Name
        'TARGETDIR',              # Component_
        '[TARGETDIR]pyjumble.exe',# Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
    ),
    (
        'StartMenuShortcut',        # Shortcut
        'StartMenuFolder',        # Directory_
        'PyJumble',               # Name
        'TARGETDIR',              # Component_
        '[TARGETDIR]pyjumble.exe',# Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
    )
]

cx_Freeze.setup(
    name    = 'PyJumble',
    version = '1.0.0',
    author  = 'Gerard Balaoro',
    url     = 'https://github.com/GerardBalaoro/PyJumble',
    options = {
        'build_exe': {
            'packages': ['pygame', 'random', 'math'],
            'includes': ['config', 'engine', 'sprites', 'interface'],
            'include_files': ['assets/', 'LICENSE.md', 'README.md'],
        },
        'bdist_msi': {
            'data': {
                'Shortcut': shortcut_table
            }
        }
    },
    executables = executables
)