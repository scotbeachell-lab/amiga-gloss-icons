#!/bin/sh
# Rebuild AmigaGloss and install it for the current user, then refresh KDE caches.
set -e
cd "$(dirname "$0")/gen"
python3 build.py "$HOME/.local/share/icons/AmigaGloss"
rm -f "$HOME"/.cache/icon-cache.kcache
gtk-update-icon-cache -q -f "$HOME/.local/share/icons/AmigaGloss" 2>/dev/null || true
echo "Apply with: /usr/libexec/plasma-changeicons AmigaGloss   (or System Settings > Colours & Themes > Icons)"
