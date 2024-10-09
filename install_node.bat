@echo off

:: Criar e ativar um ambiente virtual
python -m venv venv
call venv\Scripts\activate

:: Instalar o pacote
pip install .

:: Iniciar o nó
crypto_game_node