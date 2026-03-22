@echo off
REM cleanup_old_code.bat - Safely delete old root-level code files
REM This script will backup old files before deletion

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Therapeutic AI Chatbot - Old Code Cleanup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo Error: This script must be run from the project root directory
    echo Current path: %cd%
    exit /b 1
)

echo Files to remove:
echo.

REM Count existing files
set count=0
for %%F in (behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py) do (
    if exist "%%F" (
        echo   - %%F
        set /a count+=1
    )
)

if %count% equ 0 (
    echo.
    echo Already clean - no old files found!
    exit /b 0
)

echo.
echo Found %count% old files to remove
echo.
set /p response="Create backup folder and move files? (y/n): "

if /i not "%response%"=="y" (
    echo Cancelled
    exit /b 0
)

REM Create backup folder with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set BACKUP_DIR=old_code_backup_%mydate%_%mytime%

mkdir "%BACKUP_DIR%"
echo.
echo Created backup folder: %BACKUP_DIR%
echo.

REM Move files
for %%F in (behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py) do (
    if exist "%%F" (
        move "%%F" "%BACKUP_DIR%\%%F" >nul
        echo [OK] Moved %%F
    )
)

echo.
echo ========================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Run tests: pytest
echo 2. Test imports: python -c "from app.main import app; print('✓ OK')"
echo 3. Start server: uvicorn app.main:app --reload
echo 4. Delete backup: rmdir /s /q %BACKUP_DIR%
echo.
pause
