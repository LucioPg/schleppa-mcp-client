#!/bin/bash

# Set these variables before running
DOCKER_USERNAME="LucioPg"
IMAGE_NAME="schleppa-mcp-client"
TAG="latest"

# Full image name
FULL_IMAGE_NAME="$DOCKER_USERNAME/$IMAGE_NAME:$TAG"

# Build the Docker image
echo "Building Docker image: $FULL_IMAGE_NAME"
docker build -t $FULL_IMAGE_NAME .

# Log in to Docker Hub (you'll be prompted for password)
echo "Logging in to Docker Hub as $DOCKER_USERNAME"
docker login -u $DOCKER_USERNAME

# Push the image to Docker Hub
echo "Pushing image to Docker Hub: $FULL_IMAGE_NAME"
docker push $FULL_IMAGE_NAME

echo "Done! Your image is now available at: $FULL_IMAGE_NAME" 