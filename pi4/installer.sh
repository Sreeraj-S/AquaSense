#!/bin/bash

REPO_URL="https://github.com/Sreeraj-S/AquaSense.git"
LOCAL_DIR="AquaSense"
DOCKER_IMAGE="AquaSenseImg"

# Check if the directory already exists
if [ -d "$LOCAL_DIR" ]; then
    echo "Repository already exists. Checking for changes..."
    cd "$LOCAL_DIR"/pi4 || exit
    git fetch origin
    if git diff --quiet origin/dev; then
        echo "No changes detected. Starting Docker container..."
        docker compose up
    else
        echo "Changes detected. Building Docker image..."
        git checkout dev
        git pull origin dev
        docker compose up --build
    fi
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$LOCAL_DIR"
    cd "$LOCAL_DIR"/pi4 || exit
    git checkout dev
    git pull
    ls
    docker compose up
fi

