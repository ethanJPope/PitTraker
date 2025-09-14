# 🔧 Pit Tracker

A Django-based tool management system for robotics teams to track loaned tools and equipment.

![Pit Tracker Screenshot](screenshot.png)

## 🚀 Features

- **User Authentication**: Secure login system with email-based authentication
- **Tool Tracking**: Record, edit, and return tool loans
- **User Management**: Admin users can create and manage other users
- **Dark Theme**: Modern, responsive interface optimized for pit environments
- **Real-time Statistics**: Track active loans, returned tools, and usage metrics
- **Admin Controls**: Separate permissions for regular users and administrators

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in auth system with custom user model
- **Deployment**: Gunicorn + Nginx

## 📋 Requirements

- Python 3.11+
- Git
- Virtual environment (recommended)

## 🚀 Quick Start (Development)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/PitTraker.git
cd PitTraker
```

## 🌐 Production Deployment

### Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+
- PostgreSQL
- Nginx
- Supervisor (for process management)

### 1. Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx supervisor git -y

# Create application user
sudo adduser pittracker
sudo usermod -aG sudo pittracker
```

### 2. Database Setup

```bash
# Switch to postgres user and create database
sudo -u postgres psql
CREATE DATABASE pittracker_db;
CREATE USER pittracker_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pittracker_db TO pittracker_user;
\q
```

### 3. Application Deployment

```bash
# Switch to application user
sudo su - pittracker

# Clone repository
git clone https://github.com/yourusername/PitTraker.git
cd PitTraker

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Create production settings
cp .env.example .env
```

### 4. Environment Configuration

Edit the `.env` file with production values:

```bash
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DATABASE_URL=postgresql://pittracker_user:your_secure_password@localhost:5432/pittracker_db
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,server-ip-address
```

### 5. Database Migration & Static Files

```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 6. Gunicorn Configuration

Create `/home/pittracker/PitTraker/gunicorn.conf.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
```

### 7. Supervisor Configuration

Create `/etc/supervisor/conf.d/pittracker.conf`:

```ini
[program:pittracker]
command=/home/pittracker/PitTraker/venv/bin/gunicorn --config /home/pittracker/PitTraker/gunicorn.conf.py pit_tracker.wsgi:application
directory=/home/pittracker/PitTraker
user=pittracker
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/pittracker.log
```

### 8. Nginx Configuration

Create `/etc/nginx/sites-available/pittracker`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location /static/ {
        alias /home/pittracker/PitTraker/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/pittracker/PitTraker/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 9. Enable and Start Services

```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/pittracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start supervisor services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start pittracker
```

### 10. SSL Certificate (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 🔄 Updates and Maintenance

To update the application:

```bash
# Switch to application user
sudo su - pittracker
cd PitTraker

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo supervisorctl restart pittracker
```

### 🔒 Security Considerations

- Change default passwords and secret keys
- Configure firewall (UFW): `sudo ufw enable && sudo ufw allow ssh && sudo ufw allow 'Nginx Full'`
- Regularly update system packages
- Monitor application logs: `sudo tail -f /var/log/pittracker.log`
- Set up automated backups for PostgreSQL database

## 🍎 Production Deployment (Intel Mac)

### Prerequisites

- macOS 10.15+ (Catalina or newer)
- Homebrew package manager
- Xcode Command Line Tools

### 1. Install Dependencies

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.11 postgresql nginx git
brew services start postgresql
```

### 2. Database Setup

```bash
# Create database and user
createdb pittracker_db
psql pittracker_db -c "CREATE USER pittracker_user WITH PASSWORD 'your_secure_password';"
psql pittracker_db -c "GRANT ALL PRIVILEGES ON DATABASE pittracker_db TO pittracker_user;"
psql pittracker_db -c "ALTER USER pittracker_user CREATEDB;"
```

### 3. Application Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/PitTraker.git
cd PitTraker

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Create production settings
cp .env.example .env
```

### 4. Environment Configuration

Edit the `.env` file with production values:

```bash
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DATABASE_URL=postgresql://pittracker_user:your_secure_password@localhost:5432/pittracker_db
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost,127.0.0.1
```

### 5. Database Migration & Static Files

```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 6. Gunicorn Configuration

Create `gunicorn.conf.py` in the project root:

```python
bind = "127.0.0.1:8000"
workers = 2
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
```

### 7. Launch Agent Configuration (macOS Service)

Create `~/Library/LaunchAgents/com.pittracker.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pittracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/PitTraker/venv/bin/gunicorn</string>
        <string>--config</string>
        <string>/path/to/PitTraker/gunicorn.conf.py</string>
        <string>pit_tracker.wsgi:application</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/PitTraker</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/pittracker.log</string>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/pittracker.log</string>
</dict>
</plist>
```

Replace `/path/to/PitTraker` with your actual project path.

### 8. Nginx Configuration

Create `/usr/local/etc/nginx/servers/pittracker.conf`:

```nginx
server {
    listen 80;
    server_name localhost your-domain.com;

    location /static/ {
        alias /path/to/PitTraker/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/PitTraker/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Replace `/path/to/PitTraker` with your actual project path.

### 9. Start Services

```bash
# Load and start the launch agent
launchctl load ~/Library/LaunchAgents/com.pittracker.plist
launchctl start com.pittracker

# Test nginx configuration and start
sudo nginx -t
brew services start nginx
```

### 10. SSL Certificate (Optional for Local Development)

For local development with HTTPS:

```bash
# Install mkcert for local SSL certificates
brew install mkcert
mkcert -install

# Generate certificate for localhost
mkcert localhost 127.0.0.1

# Update nginx configuration to use SSL
```

### 🔄 Updates and Maintenance (macOS)

To update the application:

```bash
cd PitTraker

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
launchctl stop com.pittracker
launchctl start com.pittracker
```

### 🔒 Security Considerations (macOS)

- Change default passwords and secret keys
- Configure macOS firewall in System Preferences > Security & Privacy
- Regularly update Homebrew packages: `brew update && brew upgrade`
- Monitor application logs: `tail -f /usr/local/var/log/pittracker.log`
- Set up Time Machine backups for the database and application
