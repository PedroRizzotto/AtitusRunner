# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/icon.ico") ]
cx_Freeze.setup(
    name = "Atitus Runner",
    options={
        "build_exe":{
            "packages":["pygame","pyttsx3","comtypes"],
            "include_files":["recursos"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
