# Contributing to KITTEN FRONT

Thanks for helping improve the project. Issues and pull requests may be written in English or French.

## Local setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe main.py
```

## Pull requests

1. Keep each change focused and preserve existing save compatibility when possible.
2. Add or update tests for gameplay and persistence changes.
3. Run the full test suite before opening the pull request.
4. Do not commit `.deps`, `build`, `dist`, settings or save files.
5. Include a screenshot for visible interface changes.

The project is experimental and AI-assisted. Contributors remain responsible for reviewing submitted code and assets.
