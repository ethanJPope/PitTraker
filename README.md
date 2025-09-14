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
