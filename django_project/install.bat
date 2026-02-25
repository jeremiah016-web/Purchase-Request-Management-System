@echo off
echo ============================================================
echo PR Management System - Installation Script
echo ============================================================
echo.

echo [1/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo.

echo [2/5] Running migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error running migrations!
    pause
    exit /b 1
)
echo.

echo [3/5] Creating superuser...
echo Please create an admin account:
python manage.py createsuperuser
echo.

echo [4/5] Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and add your Google OAuth credentials
echo 2. Run: python setup_oauth.py (to configure Google OAuth)
echo 3. Run: python manage.py runserver
echo 4. Visit: http://localhost:8000
echo.
echo For Google OAuth setup, see GOOGLE_OAUTH_SETUP.md
echo.
pause
