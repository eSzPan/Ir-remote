[app]
title = Pilot IR
package.name = irremote
package.domain = org.pydroid.ir
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Wymagane biblioteki
requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# KLUCZOWE: Pozwolenia i funkcje sprzętowe dla diody IR
android.permissions = TRANSMIT_IR
android.features = android.hardware.consumerir

[buildozer]
log_level = 2
warn_on_root = 1
