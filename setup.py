import cx_Freeze
import sys
import os

# Configuração para incluir arquivos de recursos
include_files = []
recursos_path = os.path.join(os.getcwd(), "recursos")
for root, dirs, files in os.walk(recursos_path):
    for file in files:
        file_path = os.path.join(root, file)
        include_files.append(file_path)

# Configuração para pacotes necessários
build_options = {
    "packages": ["pygame", "pyttsx3", "encodings"],  # Adicionei 'encodings' explicitamente
    "include_files": include_files,
    "excludes": ["tkinter"],  # Pode excluir módulos não usados
    "optimize": 1
}

# Configuração base
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Para não mostrar console no Windows

executables = [
    cx_Freeze.Executable(
        script="main.py",
        base=base,
        icon="recursos/icon.ico",
        target_name="AtitusRunner.exe"
    )
]

cx_Freeze.setup(
    name="Atitus Runner",
    version="1.0",
    description="Jogo Atitus Runner",
    options={"build_exe": build_options},
    executables=executables
)