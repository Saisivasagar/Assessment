#!/bin/bash

echo "Creating assessment conda environment. This will take some time (minutes)"

# Ensure Conda is initialized for the current shell
eval "$(conda shell.bash hook)"

# Create the Conda environment
conda env create -f conda_env.yml -n assessment 

# Clean up unnecessary files
conda clean -a --yes

# Initialize bashrc
conda init

# display environments
conda info --envs

# Add 'conda activate assessment' to ~/.bashrc if not already present
if ! grep -q "conda activate assessment" ~/.bashrc; then
    echo "Adding 'conda activate assessment' to ~/.bashrc"
    echo -e "\n# Activate the assessment conda environment by default\nconda activate assessment" >> ~/.bashrc
fi

# Activate the environment
conda activate assessment    

echo "Setup completed successfully!"
