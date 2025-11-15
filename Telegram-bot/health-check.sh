#!/bin/bash

echo "🏥 Mandadero Bot Health Check"
echo "============================"

APP_NAME="mandadero-telegram-bot"

# Check if PM2 is running
if ! command -v pm2 &> /dev/null; then
    echo "❌ PM2 is not installed"
    exit 1
fi

# Check bot status
echo "📊 Bot Status:"
pm2 status $APP_NAME

# Check if bot is running
if pm2 list | grep -q "$APP_NAME.*online"; then
    echo "✅ Bot is running"
else
    echo "❌ Bot is not running"
    echo "🔧 Attempting to restart..."
    pm2 restart $APP_NAME
fi

# Check recent logs for errors
echo ""
echo "📋 Recent Logs (last 10 lines):"
pm2 logs $APP_NAME --lines 10 --nostream

# Check memory usage
echo ""
echo "💾 Memory Usage:"
pm2 show $APP_NAME | grep -E "(memory usage|cpu usage)"

# Check database connectivity
echo ""
echo "🗄️ Testing Database Connection:"
python3 -c "
import sys
sys.path.append('app')
try:
    from services.database import engine
    with engine.connect() as conn:
        result = conn.execute('SELECT 1')
        print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

echo ""
echo "🏥 Health check completed!"