#!/bin/bash

# Set variables
IMAGE_NAME="flower-v2"
IMAGE_TAG="latest"
CONTAINER_NAME="flower-v2"
PORT="1338"

# Build the Docker image
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

# Check if the image was built successfully
if [ $? -ne 0 ]; then
  echo "Error: Failed to build Docker image."
  exit 1
fi

# Display a message indicating that the build was successful
echo "Docker image '$IMAGE_NAME:$IMAGE_TAG' was built successfully."

# Run the Docker container
docker run -d --rm --name "$CONTAINER_NAME" -p "$PORT:80" "$IMAGE_NAME:$IMAGE_TAG"

# Check if the container is running
if [ $? -ne 0 ]; then
  echo "Error: Failed to start Docker container."
  exit 1
fi

# Display a message indicating that the container was started successfully
echo "Docker container '$CONTAINER_NAME' is running on port $PORT."
