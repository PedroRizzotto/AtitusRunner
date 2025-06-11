import cx_Freeze
import sys
import os
from cx_Freeze import setup, Executable

# Configuração especial para garantir a execução
if sys.platform == "win32":
    base = "Win32GUI"
    # Isso força a criação do manifest
    additional_options = {
        "build_exe": {
            "include_msvcr": True,
            "silent": True
        }
    }
else:
    base = None
    additional_options = {}

# Configuração dos arquivos
def get_all_files():
    file_list = []
    for root, _, files in os.walk("recursos"):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

setup(
    name="Atitus Runner",
    version="1.0",
    description="Jogo de Corrida",
    options={
        "build_exe": {
            "packages": ["pygame", "pyttsx3","encodings"],
            "includes": ["pygame._sdl2"],
            "include_files": get_all_files(),
            "optimize": 2
        },
        **additional_options
    },
    executables=[
        Executable(
            "main.py",
            base=base,
            icon="recursos/icon.ico",
            target_name="AtitusRunner.exe",
            # Configurações extras para Windows
            uac_admin=True if sys.platform == "win32" else False)])