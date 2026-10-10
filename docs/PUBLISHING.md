# Publishing KITTEN FRONT on GitHub

The repository is prepared for GitHub, but publishing remains under the owner's control.

## 1. Create the GitHub repository

Create a public repository named `kitten-front`. Do not ask GitHub to add a README, license, or `.gitignore`, because these files already exist locally.

Suggested description:

> An experimental, AI-assisted strategy game about living front lines, dot armies, and command decisions.

## 2. Publish the local repository

Open PowerShell in the KITTEN FRONT folder and replace `YOUR-NAME` with the GitHub account name:

```powershell
git branch -M main
git add .
git commit -m "Initial public release"
git remote add origin https://github.com/YOUR-NAME/kitten-front.git
git push -u origin main
```

The Windows build workflow will test the game and provide a downloadable artifact on every push to `main`.

## 3. Create a downloadable release

Create and push a version tag:

```powershell
git tag v0.1.0
git push origin v0.1.0
```

GitHub Actions will then build both files and attach them to a new GitHub Release:

- `KITTEN FRONT.exe`: portable version;
- `KITTEN-FRONT-Setup.exe`: Windows installer.

## Before each release

1. Update `VERSION`.
2. Add the release notes to `CHANGELOG.md`.
3. Run `python -m unittest -v`.
4. Run `./build_installer.ps1` on Windows when Inno Setup 6 is installed.
5. Launch the packaged game and visually check the presentation, menu, settings, and one match.

## Repository settings worth enabling

- Require the `Windows build` check before merging pull requests.
- Enable Dependabot security alerts.
- Keep GitHub Issues enabled for the included bug and feature forms.
- Protect the `main` branch once collaboration begins.
