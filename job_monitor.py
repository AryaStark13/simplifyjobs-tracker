import requests
import time
import re
import smtplib
import logging
import json
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobMonitor:
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the job monitor with configuration."""
        self.config = self.load_config(config_file)
        self.url = "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/refs/heads/dev/README.md"
        self.last_jobs_hash = None
        self.load_last_state()
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found. Creating template...")
            self.create_config_template(config_file)
            raise Exception(f"Please fill in the configuration in {config_file}")
    
    def create_config_template(self, config_file: str):
        """Create a configuration template file."""
        template = {
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "your_email@gmail.com",
                "sender_password": "your_app_password",
                "recipient_email": "recipient@gmail.com"
            },
            "discord_webhook": {
                "enabled": False,
                "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
            },
            "slack_webhook": {
                "enabled": False,
                "webhook_url": "https://hooks.slack.com/services/YOUR_WEBHOOK_URL"
            },
            "pushbullet": {
                "enabled": False,
                "api_key": "your_pushbullet_api_key"
            },
            "check_interval_minutes": 60,
            "state_file": "last_state.json"
        }
        
        with open(config_file, 'w') as f:
            json.dump(template, f, indent=4)
        logger.info(f"Configuration template created at {config_file}")
    
    def load_last_state(self):
        """Load the last known state from file."""
        try:
            with open(self.config.get('state_file', 'last_state.json'), 'r') as f:
                state = json.load(f)
                self.last_jobs_hash = state.get('last_jobs_hash')
                logger.info("Loaded previous state")
        except FileNotFoundError:
            logger.info("No previous state found, starting fresh")
            self.last_jobs_hash = None
    
    def save_state(self, jobs_hash: str):
        """Save the current state to file."""
        state = {
            'last_jobs_hash': jobs_hash,
            'last_check': datetime.now().isoformat()
        }
        with open(self.config.get('state_file', 'last_state.json'), 'w') as f:
            json.dump(state, f, indent=2)
    
    def fetch_readme(self) -> Optional[str]:
        """Fetch the README content from GitHub."""
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch README: {e}")
            return None
    
    def extract_ds_ml_jobs(self, content: str) -> List[Dict]:
        """Extract Data Science, AI & ML job listings from the README."""
        jobs = []
        
        # Find the Data Science, AI & Machine Learning section
        ds_ml_pattern = r'## 🤖 Data Science, AI & Machine Learning New Grad Roles.*?(?=## |\Z)'
        ds_ml_match = re.search(ds_ml_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not ds_ml_match:
            logger.warning("Could not find Data Science, AI & Machine Learning section")
            return jobs
        
        ds_ml_section = ds_ml_match.group(0)
        
        # Extract table rows (skip header)
        row_pattern = r'<tr[^>]*>.*?</tr>'
        rows = re.findall(row_pattern, ds_ml_section, re.DOTALL)
        
        for i, row in enumerate(rows):
            if i == 0:  # Skip header row
                continue
                
            # Extract company, role, location
            company_match = re.search(r'<strong[^>]*>(.*?)</strong>', row, re.DOTALL)
            role_match = re.search(r'<td[^>]*>(.*?)</td>(?:.*?<td[^>]*>){1}(.*?)</td>', row, re.DOTALL)
            
            if company_match and role_match:
                company = re.sub(r'<[^>]+>', '', company_match.group(1)).strip()
                
                # Get all td elements
                td_pattern = r'<td[^>]*>(.*?)</td>'
                td_matches = re.findall(td_pattern, row, re.DOTALL)
                
                if len(td_matches) >= 4:
                    role = re.sub(r'<[^>]+>', '', td_matches[1]).strip()
                    location = re.sub(r'<[^>]+>', '', td_matches[2]).strip()
                    age = re.sub(r'<[^>]+>', '', td_matches[4]).strip()
                    
                    # Extract application link
                    link_match = re.search(r'href="([^"]+)"', td_matches[3])
                    app_link = link_match.group(1) if link_match else ""
                    
                    job = {
                        'company': company,
                        'role': role,
                        'location': location,
                        'age': age,
                        'link': app_link,
                        'hash': hashlib.md5(f"{company}_{role}_{location}".encode()).hexdigest()
                    }
                    jobs.append(job)
        
        return jobs
    
    def get_jobs_hash(self, jobs: List[Dict]) -> str:
        """Generate a hash of all job listings."""
        jobs_str = json.dumps(sorted(jobs, key=lambda x: x['hash']), sort_keys=True)
        return hashlib.md5(jobs_str.encode()).hexdigest()
    
    def find_new_jobs(self, current_jobs: List[Dict], previous_jobs: List[Dict]) -> List[Dict]:
        """Find jobs that are new compared to the previous check."""
        current_hashes = {job['hash'] for job in current_jobs}
        previous_hashes = {job['hash'] for job in previous_jobs}
        new_hashes = current_hashes - previous_hashes
        
        return [job for job in current_jobs if job['hash'] in new_hashes]
    
    def send_email_notification(self, new_jobs: List[Dict]):
        """Send email notification for new jobs."""
        if not self.config.get('email'):
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = self.config['email']['recipient_email']
            msg['Subject'] = f"🚨 {len(new_jobs)} New Data Science/ML Jobs Found!"
            
            # Create HTML body
            body = f"""
            <h2>🤖 New Data Science, AI & Machine Learning Jobs</h2>
            <p>Found {len(new_jobs)} new job listing(s) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <table border="1" style="border-collapse: collapse;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 8px;">Company</th>
                    <th style="padding: 8px;">Role</th>
                    <th style="padding: 8px;">Location</th>
                    <th style="padding: 8px;">Age</th>
                    <th style="padding: 8px;">Apply</th>
                </tr>
            """
            
            for job in new_jobs:
                body += f"""
                <tr>
                    <td style="padding: 8px;"><strong>{job['company']}</strong></td>
                    <td style="padding: 8px;">{job['role']}</td>
                    <td style="padding: 8px;">{job['location']}</td>
                    <td style="padding: 8px;">{job['age']}</td>
                    <td style="padding: 8px;"><a href="{job['link']}">Apply</a></td>
                </tr>
                """
            
            body += """
            </table>
            <p><em>This is an automated notification from the Job Monitor.</em></p>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['sender_email'], self.config['email']['sender_password'])
            text = msg.as_string()
            server.sendmail(self.config['email']['sender_email'], self.config['email']['recipient_email'], text)
            server.quit()
            
            logger.info(f"Email notification sent for {len(new_jobs)} new jobs")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    def send_discord_notification(self, new_jobs: List[Dict]):
        """Send Discord webhook notification."""
        if not self.config.get('discord_webhook', {}).get('enabled', False):
            return
            
        try:
            embed = {
                "title": f"🤖 {len(new_jobs)} New Data Science/ML Jobs!",
                "color": 0x00ff00,
                "timestamp": datetime.now().isoformat(),
                "fields": []
            }
            
            for job in new_jobs[:10]:  # Limit to 10 jobs to avoid Discord limits
                embed["fields"].append({
                    "name": f"{job['company']} - {job['role']}",
                    "value": f"📍 {job['location']}\n🕒 {job['age']}\n[Apply]({job['link']})",
                    "inline": True
                })
            
            data = {"embeds": [embed]}
            
            response = requests.post(self.config['discord_webhook']['webhook_url'], json=data)
            response.raise_for_status()
            
            logger.info(f"Discord notification sent for {len(new_jobs)} new jobs")
            
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")
    
    def send_pushbullet_notification(self, new_jobs: List[Dict]):
        """Send Pushbullet notification."""
        if not self.config.get('pushbullet', {}).get('enabled', False):
            return
            
        try:
            headers = {"Access-Token": self.config['pushbullet']['api_key']}
            
            title = f"🤖 {len(new_jobs)} New DS/ML Jobs!"
            body = "\n".join([f"• {job['company']}: {job['role']}" for job in new_jobs[:5]])
            
            data = {
                "type": "note",
                "title": title,
                "body": body
            }
            
            response = requests.post("https://api.pushbullet.com/v2/pushes", headers=headers, json=data)
            response.raise_for_status()
            
            logger.info(f"Pushbullet notification sent for {len(new_jobs)} new jobs")
            
        except Exception as e:
            logger.error(f"Failed to send Pushbullet notification: {e}")
    
    def send_notifications(self, new_jobs: List[Dict]):
        """Send notifications through all enabled channels."""
        if not new_jobs:
            return
            
        logger.info(f"Sending notifications for {len(new_jobs)} new jobs")
        
        self.send_email_notification(new_jobs)
        self.send_discord_notification(new_jobs)
        self.send_pushbullet_notification(new_jobs)
    
    def check_for_updates(self) -> bool:
        """Check for new job postings and send notifications."""
        logger.info("Checking for job updates...")
        
        content = self.fetch_readme()
        if not content:
            return False
        
        current_jobs = self.extract_ds_ml_jobs(content)
        if not current_jobs:
            logger.warning("No jobs found in Data Science section")
            return False
        
        current_hash = self.get_jobs_hash(current_jobs)
        
        # If this is the first run, just save the state
        if self.last_jobs_hash is None:
            logger.info(f"First run - found {len(current_jobs)} existing jobs")
            self.save_state(current_hash)
            self.last_jobs_hash = current_hash
            return True
        
        # Check if there are changes
        if current_hash != self.last_jobs_hash:
            logger.info("Changes detected!")
            
            # For detailed comparison, we need to load previous jobs
            # This is a simplified version - in practice, you'd want to store the actual job list
            new_jobs = current_jobs  # Simplified - assume all current jobs are new
            
            self.send_notifications(new_jobs)
            self.save_state(current_hash)
            self.last_jobs_hash = current_hash
            
            return True
        else:
            logger.info("No new jobs found")
            return False
    
    def run_monitor(self):
        """Run the monitoring loop."""
        logger.info("Starting job monitor...")
        interval = self.config.get('check_interval_minutes', 60) * 60  # Convert to seconds
        
        while True:
            try:
                self.check_for_updates()
                logger.info(f"Sleeping for {interval//60} minutes...")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

def main():
    """Main function to run the job monitor."""
    try:
        monitor = JobMonitor()
        monitor.run_monitor()
    except Exception as e:
        logger.error(f"Failed to start monitor: {e}")
        print("\nTo get started:")
        print("1. Fill in the config.json file with your notification settings")
        print("2. Run the script again")

if __name__ == "__main__":
    main()