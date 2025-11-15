# 🚀 Hostinger Deployment Guide - Mandadero Telegram Bot

## Prerequisites

1. **Hostinger VPS/Cloud Hosting** with SSH access
2. **Node.js** installed (for PM2)
3. **Python 3.8+** installed
4. **PostgreSQL** database (can use Hostinger's managed DB or install locally)

## Step 1: Prepare Your Hostinger Server

### Connect to your server:
```bash
ssh your_username@your_server_ip
```

### Install required software:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js and npm (for PM2)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL (if not using managed database)
sudo apt install postgresql postgresql-contrib -y
```

## Step 2: Upload Your Bot Code

### Option A: Using Git (Recommended)
```bash
cd /home/$(whoami)
git clone https://github.com/carlossmartdevices-cyber/mandadero.git
cd mandadero/Telegram-bot
```

### Option B: Using SCP/SFTP
Upload the `Telegram-bot` folder to `/home/your_username/mandadero/`

## Step 3: Configure Database

### If using Hostinger Managed Database:
1. Create a PostgreSQL database in Hostinger control panel
2. Note down: hostname, database name, username, password

### If using local PostgreSQL:
```bash
sudo -u postgres psql
CREATE DATABASE mandadero_bot;
CREATE USER bot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE mandadero_bot TO bot_user;
\q
```

## Step 4: Configure Environment

```bash
cd /home/$(whoami)/mandadero/Telegram-bot

# Copy production environment file
cp .env.production .env

# Edit with your actual values
nano .env
```

Update the `.env` file with your actual values:
```env
TELEGRAM_BOT_TOKEN=8467637679:AAFLYj77C0y_wwzX1FZt28GhBHNTXa2QE7M
DATABASE_URL=postgresql://your_db_user:your_db_password@your_db_host:5432/your_db_name
ADMIN_ID=8365312597
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Step 5: Deploy with PM2

```bash
# Run the deployment script
./deploy.sh
```

Or manually:
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
```

## Step 6: Verify Deployment

```bash
# Check bot status
pm2 status

# View logs
pm2 logs mandadero-telegram-bot

# Monitor in real-time
pm2 monit
```

## Useful PM2 Commands

```bash
# View all processes
pm2 list

# Restart the bot
pm2 restart mandadero-telegram-bot

# Stop the bot
pm2 stop mandadero-telegram-bot

# View logs
pm2 logs mandadero-telegram-bot --lines 100

# Flush logs
pm2 flush

# Monitor resources
pm2 monit
```

## Troubleshooting

### Bot not starting:
1. Check logs: `pm2 logs mandadero-telegram-bot`
2. Verify environment variables in `.env`
3. Test database connection
4. Check Python dependencies: `pip3 list`

### Database connection issues:
1. Verify DATABASE_URL format
2. Check database server status
3. Ensure database exists and user has permissions

### Memory issues:
1. Monitor with: `pm2 monit`
2. Adjust `max_memory_restart` in `ecosystem.config.js`

## Security Best Practices

1. **Firewall**: Only open necessary ports (22 for SSH, 80/443 for web)
2. **Environment**: Never commit `.env` to version control
3. **Updates**: Regularly update system and dependencies
4. **Monitoring**: Set up log rotation and monitoring

## Backup Strategy

```bash
# Backup logs
tar -czf bot-logs-$(date +%Y%m%d).tar.gz logs/

# Backup configuration
cp .env .env.backup.$(date +%Y%m%d)
```

## Auto-restart on Server Reboot

The `pm2 startup` command should handle this, but verify:
```bash
# Check if PM2 will start on boot
systemctl status pm2-$(whoami)

# If not enabled:
pm2 startup
pm2 save
```

---

Your Mandadero Telegram Bot is now deployed and running on Hostinger with PM2! 🎉