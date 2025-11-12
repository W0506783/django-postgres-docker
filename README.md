1. Initialize a Git repository in the empty directory

git init

2. Create .gitignore

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pyc
*.pkl
*.sqlite3

# Virtual environments
venv/
.env/
.env.bak/

# Django
/static/
media/

# VS Code
.vscode/
.code-workspace

# Docker
*.log
*.pid
*.seed
*.db
*.sock
docker-compose.override.yml

# System files
.DS_Store
Thumbs.db

3. Placeholder files

Dockerfile
docker-compose.yml
requirements.txt

Step 1 – Create the Django Project
make web
django-admin startproject core .
python manage.py startapp events
Update core/settings.py with database settings using environment variables from .env. Then migrate:

python manage.py makemigrations
python manage.py migrate


