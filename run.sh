#!/bin/bash

# Default: don't build unless 'build' param is passed
SHOULD_BUILD=false
if [ "$1" == "build" ]; then
    SHOULD_BUILD=true
fi

# Ensure mentor.db exists as a valid SQLite file so Docker doesn't create it as a directory
if [ ! -f mentor.db ]; then
    echo "📝 mentor.db not found. Initializing valid SQLite database file..."
    python3 -c "import sqlite3; sqlite3.connect('mentor.db').close()"
fi

# Build if requested OR if the image doesn't exist yet
if [ "$SHOULD_BUILD" = true ] || [[ "$(docker images -q mentor-ai-app 2> /dev/null)" == "" ]]; then
    echo "🏗️  Building and starting containers..."
    docker compose up --build
else
    echo "🚀 Image found. Starting containers..."
    docker compose up
fi
