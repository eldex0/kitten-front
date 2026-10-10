@echo off
title KITTEN FRONT
cd /d "%~dp0"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
  "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" main.py
) else (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 main.py
  ) else (
    where python >nul 2>nul
    if not errorlevel 1 (
      python main.py
    ) else (
      echo Python 3 est requis. Installez-le depuis https://www.python.org/downloads/
      pause
    )
  )
)
