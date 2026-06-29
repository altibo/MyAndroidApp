[app]

title = MyAndroidApp
package.name = myandroidapp
package.domain = io.github.altibo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = .git,.github,site,tests,venv,.venv

version.regex = __version__ = ["'](.*)["']
version.filename = %(source.dir)s/main.py

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 24
android.ndk = 27c
android.ndk_api = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
