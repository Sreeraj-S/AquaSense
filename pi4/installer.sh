#!/bin/bash

REPO_URL="https://github.com/Sreeraj-S/AquaSense.git"
LOCAL_DIR="AquaSense"
DOCKER_IMAGE="AquaSenseImg"

# Check if the directory already exists
if [ -d "$LOCAL_DIR" ]; then
    echo "Repository already exists. Pulling latest changes..."
    cd "$LOCAL_DIR"/pi4 || exit
    git checkout dev
    git fetch origin
    git pull origin dev
    echo "Changes detected. Building Docker image..."
    docker compose up --build
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$LOCAL_DIR"
    cd "$LOCAL_DIR"/pi4 || exit
    git checkout dev
    git pull
    ls
    docker compose up --build
fi

