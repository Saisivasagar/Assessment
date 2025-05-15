#!/bin/bash

echo "Creating uv environment."

# install uv and venv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

echo "Setup completed successfully!"
