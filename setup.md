# 🤖 Data Science Job Monitor Setup Guide

This guide will help you set up automated monitoring for new Data Science, AI & Machine Learning job postings.

## 📋 Requirements

Install Python dependencies:
```bash
pip install requests
```

## 🔧 Setup Instructions

### 1. Download the Monitor Script
Save the Python script as `job_monitor.py`

### 2. First Run (Creates Configuration)
```bash
python job_monitor.py
```
This will create a `config.json` template file.

### 3. Configure Notifications

Edit the `config.json` file with your preferred notification methods:

#### 📧 Email Setup (Recommended)
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "recipient@gmail.com"
  }
}
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Use the app password (not your regular password)

#### 💬 Discord Setup (Optional)
```json
{
  "discord_webhook": {
    "enabled": true,
    "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
  }
}
```

**To get Discord webhook:**
1. Go to your Discord server
2. Server Settings → Integrations → Webhooks
3. Create New Webhook → Copy URL

#### 📱 Pushbullet Setup (Optional)
```json
{
  "pushbullet": {
    "enabled": true,
    "api_key": "your-pushbullet-api-key"
  }
}
```

**To get Pushbullet API key:**
1. Sign up at [Pushbullet.com](https://www.pushbullet.com)
2. Go to Settings → Account → Access Tokens
3. Create Access Token

### 4. Test the Monitor
```bash
python job_monitor.py
```

## 🌐 Running 24/7 - Deployment Options

### Option 1: VPS/Cloud Server (Recommended)
**Best for:** Reliable 24/7 monitoring

**Services to consider:**
- **DigitalOcean Droplet** ($4-6/month)
- **AWS EC2 t2.micro** (Free tier available)
- **Google Cloud Compute Engine** (Free tier available)
- **Linode** ($5/month)

**Setup:**
```bash
# On your VPS
git clone [your-repo] 
cd job-monitor
pip install requests
nohup python job_monitor.py > monitor.log 2>&1 &
```

### Option 2: Raspberry Pi
**Best for:** Home setup, low cost

**Setup:**
```bash
# Install Python on Pi
sudo apt update
sudo apt install python3 python3-pip
pip3 install requests

# Set up as systemd service
sudo nano /etc/systemd/system/job-monitor.service
```

**Service file content:**
```ini
[Unit]
Description=Job Monitor Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/job-monitor
ExecStart=/usr/bin/python3 job_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable job-monitor
sudo systemctl start job-monitor
```

### Option 3: Heroku (Free/Paid)
**Best for:** Easy deployment, no server management

**Setup:**
1. Create `Procfile`:
```
worker: python job_monitor.py
```

2. Create `requirements.txt`:
```
requests==2.31.0
```

3. Deploy:
```bash
heroku create your-job-monitor
git push heroku main
heroku ps:scale worker=1
```

### Option 4: GitHub Actions (Limited)
**Best for:** Free, simple setup

**Limitations:** Maximum 6 hours runtime per job

Create `.github/workflows/monitor.yml`:
```yaml
name: Job Monitor
on:
  schedule:
    - cron: '0 */1 * * *'  # Every hour
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install requests
    - name: Run monitor
      env:
        CONFIG_JSON: ${{ secrets.CONFIG_JSON }}
      run: |
        echo "$CONFIG_JSON" > config.json
        python job_monitor.py
```

### Option 5: Your Local Computer
**Setup for Windows:**
1. Create a batch file `start_monitor.bat`:
```batch
@echo off
cd /d "C:\path\to\your\monitor"
python job_monitor.py
pause
```

2. Add to Windows Task Scheduler:
- Open Task Scheduler
- Create Basic Task
- Set trigger: "When the computer starts"
- Set action: Start the batch file

**Setup for Mac/Linux:**
Add to crontab:
```bash
crontab -e
# Add this line:
@reboot cd /path/to/monitor && python job_monitor.py
```

## 🔧 Configuration Options

### Timing
```json
{
  "check_interval_minutes": 60
}
```
- **15-30 minutes:** Very responsive, higher server load
- **60 minutes:** Recommended balance  
- **120+ minutes:** Conservative, might miss very short-lived postings

### Multiple Notifications
You can enable multiple notification methods simultaneously:
```json
{
  "email": { "...": "..." },
  "discord_webhook": { "enabled": true, "...": "..." },
  "pushbullet": { "enabled": true, "...": "..." }
}
```

## 📊 Monitoring & Logs

### Check if it's running:
```bash
# On Linux/Mac
ps aux | grep job_monitor

# On Windows
tasklist | findstr python
```

### View logs:
```bash
tail -f monitor.log
```

### Monitor performance:
The script creates a `last_state.json` file showing the last check time.

## 🚨 Troubleshooting

### Common Issues:

1. **Email not sending:**
   - Check app password is correct
   - Verify 2FA is enabled on Gmail
   - Check spam folder

2. **Script stops running:**
   - Check logs for errors
   - Ensure stable internet connection
   - Add restart mechanism

3. **False positives:**
   - The first run establishes baseline
   - Subsequent runs only notify on new additions

### Getting Help:
- Check the log files for error messages
- Verify your config.json syntax
- Test email settings with a simple script first

## 🎯 Next Steps

1. **Test the setup** with a short interval (5 minutes) first
2. **Verify notifications** are working
3. **Deploy to your preferred 24/7 solution**
4. **Monitor the logs** for the first few days
5. **Adjust timing** based on your needs

## 📝 Advanced Features

You can extend the script to:
- Filter by specific companies
- Add location filtering
- Include salary information
- Send weekly summaries
- Connect to job application APIs

## 🔒 Security Notes

- Never commit your `config.json` to version control
- Use environment variables for sensitive data in production
- Keep your API keys secure
- Consider using encrypted storage for credentials