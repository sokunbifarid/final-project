#!/bin/bash 

# Exits Immediately If a Command Fails 
set -e 

# Creating a Virtual Environment 
echo "Setting up python environment" 
python -m venv .venv 
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
	source .venv/Scripts/activate
else
	source .venv/bin/activate
fi


# Installing Dependencies 
echo "Installing requirements" 
pip install -r requirements.txt 

# Running Python Application 
echo "Starting flask application" 
python -m flask run
