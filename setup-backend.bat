@echo off
echo Setting up AI Digest Backend...

:: Step 3 — Freeze Dependencies
echo Freezing python dependencies...
pip freeze > requirements.txt

:: Step 4 — Create Backend Structure
echo Creating base folders...
mkdir app\api\v1
mkdir app\core
mkdir app\db
mkdir app\dependencies
mkdir app\integrations
mkdir app\middleware
mkdir app\models
mkdir app\schemas
mkdir app\services
mkdir app\utils
mkdir tests
mkdir alembic

:: Step 5 — Create __init__.py files
echo Initializing Python packages...
type nul > app\__init__.py
type nul > app\api\__init__.py
type nul > app\api\v1\__init__.py
type nul > app\core\__init__.py
type nul > app\db\__init__.py
type nul > app\dependencies\__init__.py
type nul > app\integrations\__init__.py
type nul > app\middleware\__init__.py
type nul > app\models\__init__.py
type nul > app\schemas\__init__.py
type nul > app\services\__init__.py
type nul > app\utils\__init__.py

:: Step 6 — Environment Variables (.env.example)
echo Writing environment configuration variables...
(
echo SUPABASE_URL=
echo SUPABASE_KEY=
echo DATABASE_URL=
echo STRIPE_SECRET_KEY=
echo STRIPE_WEBHOOK_SECRET=
echo CLOUDINARY_CLOUD_NAME=
echo CLOUDINARY_API_KEY=
echo CLOUDINARY_API_SECRET=
echo FRONTEND_URL=http://localhost:3000
) > .env.example

:: Copy .env.example to .env
copy .env.example .env

:: Step 7 — Git Ignore
echo Generating .gitignore file...
(
echo .venv/
echo __pycache__/
echo .env
echo .pytest_cache/
echo *.pyc
echo .vscode/
) > .gitignore

:: Step 8 — Create minimal main.py for First Run
echo Creating starter main.py...
(
echo from fastapi import FastAPI
echo.
echo app = FastAPI^(title="AI Digest API", version="1.0.0"^)
echo.
echo @app.get^("/"^)
echo def read_root^(^):
echo     return {"status": "healthy", "message": "Welcome to AI Digest API"}
) > app\main.py

echo ----------------------------------------------------
echo Success! Your backend structure is ready.
echo To start your development server, run:
echo uvicorn app.main:app --reload
echo ----------------------------------------------------
pause