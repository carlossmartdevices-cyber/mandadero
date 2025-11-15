#!/bin/bash

echo "Setting up Mandadero Telegram Bot with PostgreSQL"
echo "================================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your actual values"
fi

echo "Starting PostgreSQL database..."
docker-compose up -d postgres

echo "Waiting for PostgreSQL to be ready..."
sleep 10

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To start the bot:"
echo "1. Make sure PostgreSQL is running: docker-compose up -d postgres"
echo "2. Run the bot: python app/main.py"
echo ""
echo "Or run everything with Docker:"
echo "docker-compose up"