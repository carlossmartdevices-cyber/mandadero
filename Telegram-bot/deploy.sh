#!/bin/bash

echo "🚀 Deploying Mandadero Telegram Bot to Hostinger with PM2"
echo "========================================================="

# Set variables
APP_NAME="mandadero-telegram-bot"
APP_DIR="/home/$(whoami)/mandadero/Telegram-bot"
LOG_DIR="$APP_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📂 Setting up directories...${NC}"

# Create logs directory
mkdir -p "$LOG_DIR"

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo -e "${RED}❌ PM2 is not installed. Installing PM2...${NC}"
    npm install -g pm2
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install PM2. Please install it manually: npm install -g pm2${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    exit 1
fi

# Create and activate virtual environment
echo -e "${YELLOW}🔧 Creating Python virtual environment...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi

# Activate virtual environment and install dependencies
echo -e "${YELLOW}📦 Installing Python dependencies in virtual environment...${NC}"
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install Python dependencies${NC}"
    exit 1
fi
deactivate

# Stop existing PM2 process if running
echo -e "${YELLOW}🛑 Stopping existing bot instance...${NC}"
pm2 stop $APP_NAME 2>/dev/null || echo "No existing instance found"
pm2 delete $APP_NAME 2>/dev/null || echo "No existing instance to delete"

# Update ecosystem config with current path
sed -i "s|/home/\[YOUR_USERNAME\]/mandadero/Telegram-bot|$APP_DIR|g" ecosystem.config.js

# Start the bot with PM2
echo -e "${YELLOW}🚀 Starting bot with PM2...${NC}"
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on system boot
pm2 startup
echo -e "${GREEN}✅ PM2 startup configuration created. Please run the command shown above as root if prompted.${NC}"

# Show status
echo -e "${GREEN}📊 Bot Status:${NC}"
pm2 status

echo -e ""
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${YELLOW}📋 Useful PM2 commands:${NC}"
echo -e "   pm2 status                 - Show all processes"
echo -e "   pm2 logs $APP_NAME         - Show logs"
echo -e "   pm2 restart $APP_NAME      - Restart bot"
echo -e "   pm2 stop $APP_NAME         - Stop bot"
echo -e "   pm2 monit                  - Monitor all processes"
echo -e ""
echo -e "${YELLOW}📁 Log files location: $LOG_DIR${NC}"