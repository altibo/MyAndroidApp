# MyAndroidApp

Eine minimale Android-App in Python mit Kivy, ein reproduzierbarer
Buildozer-Build und eine Download-Seite über GitHub Pages.

## App lokal starten

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python main.py
```

## APK lokal bauen

Buildozer benötigt Linux. Unter Windows eignet sich WSL 2; das Repository
sollte für den Build im Linux-Dateisystem liegen.

```bash
python -m pip install --upgrade buildozer
buildozer android debug
```

Die APK landet anschließend im Verzeichnis `bin/`.

## Version veröffentlichen

Releases werden ausschließlich aus Tags im Format `MAJOR.MINOR.PATCH` gebaut:

```bash
git tag 1.0.0
git push origin 1.0.0
```

Der Workflow:

1. übernimmt den Tag als App-Version,
2. baut eine installierbare, debug-signierte APK,
3. legt ein GitHub Release mit dem Tag an und
4. lädt die Datei als `MyAndroidApp.apk` hoch.

Der konstante Download-Link lautet:

```text
https://github.com/altibo/MyAndroidApp/releases/latest/download/MyAndroidApp.apk
```

## Website

Der Inhalt aus `site/` wird bei Änderungen auf `main` automatisch über
GitHub Pages veröffentlicht. Die Seite fragt das neueste Release über die
GitHub API ab und verlinkt dessen APK.

In den Repository-Einstellungen muss unter **Settings → Pages → Build and
deployment → Source** einmalig **GitHub Actions** ausgewählt sein.
