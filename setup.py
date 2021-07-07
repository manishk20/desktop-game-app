import cx_Freeze
from cx_Freeze import *
setup(
    name = "myfirstapp",
    options = {'build_exe':{'packages' : ['pygame']}},
    executables=[
        Executable(
            "myfirstapp.py",
            )
        ]

    )
