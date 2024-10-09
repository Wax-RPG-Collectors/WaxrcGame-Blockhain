#!/bin/bash

# Criar e ativar um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar o pacote
pip install .

# Iniciar o nó
crypto_game_node