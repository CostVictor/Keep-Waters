import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="Keep Waters",
    options={'build_exe': {'packages': ['openpyxl', 'moviepy', 'pandas', 'pyautogui', 'numpy', 'pygame'], 
                           'include_files': ['Data', 'Script']}},
    executables = executables
)
