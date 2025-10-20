# CCSD_Second_Midterm
Web application for the second midter on a course Cloud Computing and Software Development at Singidunum University

### Deployment script example:

```bash
#!/bin/bash

APP_DIR="CCSD_Second_Midterm"
REPO_URL="https://github.com/medwedizaa/CCSD_Second_Midterm.git"
SERVICE_NAME="flask-cat"

echo "=== Updating Flask Cat App ==="

# If the app directory exists, update it; otherwise clone it
if [ -d "$APP_DIR/.git" ]; then
    echo "Repository found. Pulling latest changes..."
    cd $APP_DIR
    git pull origin main
else
    echo "Repository not found. Cloning from GitHub..."
    rm -rf $APP_DIR
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# Activate or create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source ./venv/bin/activate

# Update dependencies (if requirements.txt changed)
pip install -r src/requirements.txt --upgrade

# Restart the systemd service
echo "Restarting the service..."
sudo systemctl restart $SERVICE_NAME

echo "=== Deployment complete! ==="
~~~
