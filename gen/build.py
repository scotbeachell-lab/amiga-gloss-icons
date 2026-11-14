#!/usr/bin/env python3
"""Build the AmigaGloss KDE icon theme.

usage: build.py OUTDIR
"""
import os
import shutil
import sys

from lib import *
from art import *
from objects import folder, document, tile, obj, with_badge

REG = {}        # (ctx, name) -> fn(ic) -> body
ALIAS = []      # (ctx, alias, target)


def R(ctx, names, fn):
    names = names.split() if isinstance(names, str) else names
    REG[(ctx, names[0])] = fn
    for a in names[1:]:
        ALIAS.append((ctx, a, names[0]))


# ------------------------------------------------------------ builders
def F(e=None, c=DRAWER, opened=False):
    return lambda ic: folder(ic, c, e(ic) if e else None, opened)


def D(accent=BLUE, e=None, label=None):
    return lambda ic: document(ic, accent, e(ic) if e else None, label)


def O(e, s=1.0):
    return lambda ic: obj(ic, e(ic), True, s)


def T(c, e):
    return lambda ic: tile(ic, c, e(ic))


def B(base, badge, pos='br', s=.45):
    return lambda ic: with_badge(ic, base(ic), badge(ic), pos, s)


def P(e):          # bare pictogram, no shadow (actions)
    return lambda ic: e(ic)


# ============================================================ PLACES
R('places', 'folder inode-directory folder-blue folder-default folder_home2 folder-new-symbolic-alt', F())
for nm, col in (('red', RED), ('orange', ORANGE), ('yellow', YELLOW), ('green', GREEN), ('cyan', CYAN),
                ('violet', PURPLE), ('magenta', MAGENTA), ('grey', GREY), ('brown', BROWN), ('black', DARK),
                ('navy', NAVY), ('teal', TEAL), ('pink', PINK), ('skyblue', BLUE), ('white', SILVER)):
    R('places', 'folder-' + nm, F(c=col))
R('places', 'folder-open inode-directory-open folder-drag-accept', F(opened=True))
R('places', 'folder-documents folder-txt folder-text', F(e_lines))
R('places', 'folder-download folder-downloads', F(e_download))
R('places', 'folder-music folder-sound folder-audio', F(e_note))
R('places', 'folder-pictures folder-images folder-image folder-photo', F(e_picture))
R('places', 'folder-videos folder-video folder-movies', F(e_film))
R('places', 'folder-desktop user-desktop desktop', F(e_monitor))
R('places', 'folder-templates', F(e_pencil))
R('places', 'folder-public folder-publicshare folder-share', F(e_people))
R('places', 'folder-remote folder-network network-workgroup folder-remote-symbolic-alt', F(e_globe))
R('places', 'folder-development folder-code folder-git folder-projects folder-script', F(e_code))
R('places', 'folder-games', F(e_gamepad))
R('places', 'folder-important folder-favorites folder-bookmark folder-bookmarks', F(e_star))
R('places', 'folder-locked folder-encrypted folder-root', F(e_lock))
R('places', 'folder-cloud folder-dropbox folder-nextcloud folder-owncloud folder-gdrive', F(e_cloud))
R('places', 'folder-recent folder-temp document-open-recent-folder', F(e_clock))
R('places', 'folder-html folder-www', F(e_globe, CYAN))
R('places', 'folder-tar folder-archive folder-zip', F(e_box))
R('places', 'folder-book folder-books folder-library', F(e_book))
R('places', 'folder-mail', F(e_mail))
R('places', 'folder-print', F(e_printer))
R('places', 'folder-activities', F(e_grid))
R('places', 'folder-appimage folder-apps folder-applications', F(e_rocket))
R('places', 'folder-steam', F(e_steam))
R('places', 'folder-wine', F(e_wine))
R('places', 'folder-vbox folder-vm', F(e_vm))
R('places', 'folder-torrent', F(e_download, TEAL))
R('places', 'folder-unity folder-gamedev', F(e_gamepad, PURPLE))
R('places', 'folder-amiga', F(e_amiga, BLUE))
R('places', 'folder-backup', F(e_refresh))
R('places', 'folder-tags folder-tag', F(e_bookmark))
R('places', 'user-home folder-home go-home-place', F(e_house))
R('places', 'user-trash trash-empty user-trash-empty emptytrash', O(lambda ic: e_trash(ic, False)))
R('places', 'user-trash-full trash-full', O(lambda ic: e_trash(ic, True)))
R('places', 'start-here start-here-kde start-here-kde-plasma distributor-logo start-here-fedora fedora-logo-icon '
            'kde plasma plasmashell start-here-symbolic-alt start-here-amiga amiga-ball boing-ball about_kde about-kde '
            'start-here-kde-symbolic start-here-kde-plasma-symbolic start-here-symbolic',
  O(e_ball))
R('places', 'network-server server-database', O(e_server))
R('places', 'bookmarks bookmarks-bookmarked', O(e_bookmark))
R('places', 'user-identity avatar-default system-users user', O(e_user))
R('places', 'network-workgroup-alt network', O(e_globe))
R('places', 'favorites folder-favorite', O(e_heart))
R('places', 'tag', O(e_bookmark))
R('places', 'folder-snapshot', F(e_camera))
R('places', 'folder-sync', F(e_refresh))

# ============================================================ DEVICES
R('devices', 'drive-harddisk drive-harddisk-root drive-harddisk-system drive-multidisk harddrive', O(e_hdd))
R('devices', 'drive-harddisk-solidstate drive-harddisk-ssd', O(e_ssd))
R('devices', 'drive-harddisk-usb drive-removable-media drive-removable-media-usb drive-removable-media-usb-pendrive '
             'media-removable media-flash-memory-stick', O(e_usb))
R('devices', 'drive-optical drive-cdrom drive-dvd media-optical media-optical-cd media-optical-dvd media-optical-recordable '
             'media-optical-blu-ray media-optical-data application-x-cd-image-device', O(e_disc))
R('devices', 'media-optical-audio audio-cd', B(lambda ic: obj(ic, e_disc(ic)), lambda ic: e_note(ic)))
R('devices', 'media-optical-video media-optical-dvd-video', B(lambda ic: obj(ic, e_disc(ic)), lambda ic: e_film(ic)))
R('devices', 'media-floppy drive-removable-media-floppy media-floppy-3.5', O(e_floppy))
R('devices', 'media-flash media-flash-sd-mmc media-flash-smart-media media-flash-compact-flash', O(e_sdcard))
R('devices', 'media-tape', O(e_tape))
R('devices', 'computer computer-desktop system', O(e_computer))
R('devices', 'computer-laptop laptop', O(e_laptop))
R('devices', 'computer-amiga', O(e_amiga))
R('devices', 'video-display monitor display video-display-symbolic-alt preferences-desktop-display', O(e_monitor))
R('devices', 'video-television tv', O(e_tv))
R('devices', 'input-keyboard input-keyboard-virtual keyboard', O(e_keyboard))
R('devices', 'input-mouse mouse', O(e_mouse))
R('devices', 'input-gaming input-gamepad applications-games-device', O(e_gamepad))
R('devices', 'input-tablet tablet input-pen', O(e_tablet))
R('devices', 'input-touchpad touchpad', O(e_touchpad))
R('devices', 'printer printer-network printer-local', O(e_printer))
R('devices', 'scanner', O(e_scanner))
R('devices', 'camera-photo camera digital-camera', O(e_camera))
R('devices', 'camera-web webcam camera-video', O(lambda ic: e_camera(ic, '#3a3d4c')))
R('devices', 'phone smartphone phone-android', O(e_phone))
R('devices', 'pda multimedia-player media-player', O(e_pda))
R('devices', 'audio-card', O(e_soundcard))
R('devices', 'audio-speakers audio-speakers-symbolic-alt', O(e_speakerbox))
R('devices', 'audio-headphones', O(e_headphones))
R('devices', 'audio-headset', O(lambda ic: e_headphones(ic) + place(e_mic(ic), 22, 30, .45)))
R('devices', 'audio-input-microphone microphone', O(e_mic))
R('devices', 'network-wired network-card', O(e_network))
R('devices', 'network-wireless network-wireless-connected-100 wireless', O(e_wifi))
R('devices', 'network-modem modem', O(e_modem))
R('devices', 'bluetooth preferences-system-bluetooth bluetooth-active', O(e_bluetooth))
R('devices', 'battery battery-good battery-full', O(e_battery))
R('devices', 'battery-low', O(lambda ic: e_battery(ic, .25, RED)))
R('devices', 'battery-charging', O(lambda ic: e_battery(ic) + place(e_lightning(ic), 18, 14, .45)))
R('devices', 'cpu processor computer-cpu', O(e_chip))
R('devices', 'media-memory memory', O(e_chip))
R('devices', 'uninterruptible-power-supply', O(e_ups))
R('devices', 'thunderbolt', O(e_lightning))

# ============================================================ MIMETYPES
R('mimetypes', 'unknown application-octet-stream application-x-zerosize', D(GREY, e_question))
R('mimetypes', 'text-plain text-x-generic text-x-readme text-x-log text-x-nfo text-x-changelog', D(BLUE, e_lines))
R('mimetypes', 'text-markdown text-x-markdown', D(DARK, None, 'MD'))
R('mimetypes', 'text-html application-xhtml+xml text-xhtml+xml', D(ORANGE, e_globe, 'HTML'))
R('mimetypes', 'text-css', D(BLUE, None, 'CSS'))
R('mimetypes', 'text-xml application-xml text-x-xml application-rss+xml', D(TEAL, e_code, 'XML'))
R('mimetypes', 'application-json application-x-json text-x-json', D(AMBER, None, '{ }'))
R('mimetypes', 'application-javascript text-javascript application-x-javascript text-x-javascript', D(YELLOW, None, 'JS'))
R('mimetypes', 'application-x-typescript text-x-typescript', D(BLUE, None, 'TS'))
R('mimetypes', 'text-x-python text-x-python3 application-x-python-bytecode', D(BLUE, e_code, 'PY'))
R('mimetypes', 'text-x-csrc text-x-c', D(NAVY, e_code, 'C'))
R('mimetypes', 'text-x-chdr', D(PURPLE, e_code, 'H'))
R('mimetypes', 'text-x-c++src text-x-c++hdr text-x-cpp', D(MAGENTA, e_code, 'C++'))
R('mimetypes', 'text-x-java application-x-java', D(RED, e_code, 'JAVA'))
R('mimetypes', 'text-rust text-x-rust', D(ORANGE, e_code, 'RS'))
R('mimetypes', 'text-x-go', D(CYAN, e_code, 'GO'))
R('mimetypes', 'text-x-lua', D(NAVY, e_code, 'LUA'))
R('mimetypes', 'text-x-gdscript application-x-godot-project application-x-godot-resource', D(BLUE, e_gamepad, 'GD'))
R('mimetypes', 'text-x-csharp', D(GREEN, e_code, 'C#'))
R('mimetypes', 'text-x-asm text-x-assembly', D(DARK, e_chip, 'ASM'))
R('mimetypes', 'text-x-makefile text-x-cmake', D(BROWN, e_wrench, 'MAKE'))
R('mimetypes', 'text-x-script application-x-shellscript text-x-sh application-x-perl text-x-perl application-x-ruby '
               'text-x-ruby application-x-fishscript text-x-amigados-script', D(DARK, e_terminal))
R('mimetypes', 'text-x-patch text-x-diff', D(GREEN, None, 'DIFF'))
R('mimetypes', 'text-csv text-tab-separated-values', D(GREEN, e_sheet, 'CSV'))
R('mimetypes', 'text-x-vcard text-directory text-vcard', D(BLUE, e_contact))
R('mimetypes', 'text-calendar text-x-vcalendar', D(RED, e_calendar))
R('mimetypes', 'text-x-tex application-x-latex', D(TEAL, e_sigma, 'TEX'))
R('mimetypes', 'application-x-yaml text-x-yaml application-toml text-x-toml text-x-ini application-x-desktop-config',
  D(GREY, e_gear))
R('mimetypes', 'application-pdf application-x-pdf', D(RED, e_book, 'PDF'))
R('mimetypes', 'application-epub+zip application-x-mobipocket-ebook', D(PURPLE, e_book, 'EPUB'))
R('mimetypes', 'application-postscript image-x-eps', D(BLUE, None, 'PS'))
R('mimetypes', 'application-x-executable application-x-elf application-x-pie-executable', D(GREEN, e_gear, 'EXEC'))
R('mimetypes', 'application-x-sharedlib application-x-object application-x-archive-lib', D(PURPLE, e_puzzle))
R('mimetypes', 'application-x-desktop application-x-kde-desktop', D(BLUE, e_rocket))
R('mimetypes', 'application-x-appimage application-vnd.appimage', D(TEAL, e_rocket, 'APP'))
R('mimetypes', 'application-vnd.flatpak application-vnd.flatpak.ref application-vnd.flatpak.repo', D(BLUE, e_box, 'FLAT'))
R('mimetypes', 'application-x-ms-dos-executable application-x-msdownload application-x-msi application-x-ms-shortcut '
               'application-x-wine-extension-msp', D(RED, e_wine, 'EXE'))
R('mimetypes', 'application-x-bittorrent', D(TEAL, e_download, 'TORR'))
R('mimetypes', 'application-x-trash', D(GREY, lambda ic: e_trash(ic)))
R('mimetypes', 'application-x-amiga-disk-format application-x-adf application-x-amiga-disk application-x-ipf '
               'application-x-hdf', D(NAVY, e_floppy, 'ADF'))
R('mimetypes', 'application-x-sqlite3 application-vnd.sqlite3 application-sql text-x-sql application-x-sqlite2',
  D(BLUE, lambda ic: e_layers(ic), 'SQL'))
R('mimetypes', 'application-x-iso9660-image application-x-cd-image application-x-raw-disk-image application-x-dmg',
  D(PURPLE, e_disc, 'ISO'))
R('mimetypes', 'application-x-virtualbox-vdi application-x-qemu-disk application-x-virt-image', D(GREEN, e_vm, 'DISK'))
R('mimetypes', 'application-x-java-archive application-java-archive', D(RED, e_box, 'JAR'))
# archives
R('mimetypes', 'package-x-generic application-x-archive', D(BROWN, e_box))
R('mimetypes', 'application-zip application-x-zip application-x-zip-compressed', D(BROWN, e_box, 'ZIP'))
R('mimetypes', 'application-x-tar application-x-compressed-tar application-x-bzip-compressed-tar '
               'application-x-xz-compressed-tar application-x-zstd-compressed-tar application-x-lzma-compressed-tar',
  D(BROWN, e_box, 'TAR'))
R('mimetypes', 'application-gzip application-x-gzip application-x-bzip application-x-bzip2 application-x-xz '
               'application-x-lzma application-zstd application-x-zstd', D(BROWN, e_box, 'GZ'))
R('mimetypes', 'application-x-7z-compressed', D(BROWN, e_box, '7Z'))
R('mimetypes', 'application-x-rar application-vnd.rar application-x-rar-compressed', D(PURPLE, e_box, 'RAR'))
R('mimetypes', 'application-x-lha application-x-lzh-compressed application-x-lha-compressed', D(NAVY, e_box, 'LHA'))
R('mimetypes', 'application-x-rpm application-x-source-rpm', D(RED, e_box, 'RPM'))
R('mimetypes', 'application-x-deb application-vnd.debian.binary-package', D(MAGENTA, e_box, 'DEB'))
# media
R('mimetypes', 'image-x-generic image-bmp image-x-bmp image-tiff image-x-tga image-x-pcx image-x-portable-pixmap '
               'image-x-xpixmap image-x-icon image-vnd.microsoft.icon image-heif image-avif image-jxl',
  D(GREEN, e_picture))
R('mimetypes', 'image-png', D(GREEN, e_picture, 'PNG'))
R('mimetypes', 'image-jpeg image-jpg', D(BLUE, e_picture, 'JPG'))
R('mimetypes', 'image-gif', D(PURPLE, e_picture, 'GIF'))
R('mimetypes', 'image-webp', D(TEAL, e_picture, 'WEBP'))
R('mimetypes', 'image-svg+xml image-svg+xml-compressed image-x-svg', D(ORANGE, e_draw, 'SVG'))
R('mimetypes', 'image-x-ilbm image-x-iff image-iff', D(NAVY, e_palette, 'IFF'))
R('mimetypes', 'image-x-xcf image-x-gimp', D(BROWN, e_brush, 'XCF'))
R('mimetypes', 'application-x-krita image-openraster', D(MAGENTA, e_brush, 'KRA'))
R('mimetypes', 'image-vnd.adobe.photoshop image-x-psd', D(NAVY, e_brush, 'PSD'))
R('mimetypes', 'application-x-blender', D(ORANGE, e_layers, 'BLEND'))
R('mimetypes', 'model-gltf+json model-gltf-binary model-obj model-stl application-x-fbx', D(TEAL, e_box, '3D'))
R('mimetypes', 'audio-x-generic audio-x-wav audio-wav audio-x-aiff audio-ac3 audio-x-mod audio-x-it audio-x-xm '
               'audio-x-s3m audio-midi audio-x-midi', D(MAGENTA, e_note))
R('mimetypes', 'audio-mpeg audio-mp3 audio-x-mp3', D(MAGENTA, e_note, 'MP3'))
R('mimetypes', 'audio-flac audio-x-flac', D(ORANGE, e_note, 'FLAC'))
R('mimetypes', 'audio-ogg audio-x-vorbis+ogg audio-x-opus+ogg audio-opus', D(TEAL, e_note, 'OGG'))
R('mimetypes', 'audio-mp4 audio-aac audio-x-m4a', D(BLUE, e_note, 'M4A'))
R('mimetypes', 'audio-x-mpegurl audio-x-scpls application-vnd.apple.mpegurl audio-x-ms-asx', D(MAGENTA, e_bars))
R('mimetypes', 'video-x-generic video-mpeg video-x-msvideo video-quicktime video-x-flv video-3gpp video-x-ogm+ogg',
  D(RED, e_film))
R('mimetypes', 'video-mp4 video-x-m4v', D(RED, e_film, 'MP4'))
R('mimetypes', 'video-x-matroska video-matroska', D(PURPLE, e_film, 'MKV'))
R('mimetypes', 'video-webm', D(TEAL, e_film, 'WEBM'))
R('mimetypes', 'application-x-subrip text-x-ssa text-vtt', D(DARK, e_chat, 'SUB'))
# office
R('mimetypes', 'x-office-document application-vnd.oasis.opendocument.text application-msword '
               'application-vnd.openxmlformats-officedocument.wordprocessingml.document application-rtf text-rtf '
               'application-vnd.oasis.opendocument.text-template', D(BLUE, e_lines, 'DOC'))
R('mimetypes', 'x-office-spreadsheet application-vnd.oasis.opendocument.spreadsheet application-vnd.ms-excel '
               'application-vnd.openxmlformats-officedocument.spreadsheetml.sheet', D(GREEN, e_sheet, 'XLS'))
R('mimetypes', 'x-office-presentation application-vnd.oasis.opendocument.presentation application-vnd.ms-powerpoint '
               'application-vnd.openxmlformats-officedocument.presentationml.presentation', D(ORANGE, e_slides, 'PPT'))
R('mimetypes', 'x-office-drawing application-vnd.oasis.opendocument.graphics', D(AMBER, e_draw, 'ODG'))
R('mimetypes', 'x-office-address-book', D(BLUE, e_contact))
R('mimetypes', 'x-office-calendar', D(RED, e_calendar))
R('mimetypes', 'application-vnd.oasis.opendocument.formula', D(GREY, e_sigma))
R('mimetypes', 'message-rfc822 message-x-gnu-rmail application-mbox', D(BLUE, e_mail))
R('mimetypes', 'font-x-generic application-x-font-ttf font-ttf font-otf font-woff font-woff2 application-x-font-otf '
               'application-x-font-type1 application-x-font-pcf font-collection', D(RED, e_font))
R('mimetypes', 'application-pgp-keys application-pgp-signature application-pkcs12 application-x-x509-ca-cert '
               'application-pkix-cert application-x-pem-key application-pgp-encrypted', D(AMBER, e_key))
R('mimetypes', 'application-vnd.iccprofile', D(MAGENTA, e_palette, 'ICC'))
R('mimetypes', 'application-x-torrent-file', D(TEAL, e_download))
R('mimetypes', 'inode-symlink', D(BLUE, lambda ic: e_arrow(ic, BLUE, -45)))
R('mimetypes', 'application-x-theme application-x-plasma', D(PURPLE, e_palette))

# ============================================================ APPS
R('apps', 'system-file-manager org.kde.dolphin dolphin file-manager nautilus org.gnome.Nautilus', F(e_magnifier, opened=False))
R('apps', 'utilities-terminal org.kde.konsole konsole terminal kitty Alacritty org.gnome.Terminal xterm '
          'com.mitchellh.ghostty', O(e_terminal))
R('apps', 'nvim vim gvim neovim', B(lambda ic: obj(ic, e_terminal(ic)), lambda ic: e_pencil(ic, GREEN)))
R('apps', 'systemsettings preferences-system configure org.kde.systemsettings preferences-other '
          'gnome-control-center', O(lambda ic: e_gear(ic, SILVER) + place(e_gear(ic, AMBER), 30, 30, .5)))
R('apps', 'preferences-desktop', O(lambda ic: e_monitor(ic) + place(e_gear(ic, AMBER), 30, 22, .5)))
R('apps', 'org.kde.kate kate accessories-text-editor kwrite org.kde.kwrite notepad wordpad gedit '
          'org.gnome.TextEditor io.github.cudatext.CudaText-Qt cudatext', O(lambda ic: e_lines(ic) + place(e_pencil(ic), 26, 22, .6)))
R('apps', 'web-browser internet-web-browser firefox org.mozilla.firefox applications-internet-browser '
          'com.google.Chrome google-chrome chromium org.chromium.Chromium brave-browser',
  O(lambda ic: e_globe(ic) + place(e_magnifier(ic), 32, 32, .5)))
R('apps', 'help-browser help-contents system-help org.kde.help khelpcenter help-about-alt', O(lambda ic: e_book(ic) + place(e_question(ic), 22, 18, .55)))
R('apps', 'plasmadiscover org.kde.discover system-software-install software-store system-software-update '
          'io.github.kolunmi.Bazaar update-manager', O(lambda ic: e_box(ic) + place(e_download(ic), 18, 0, .55)))
R('apps', 'spectacle org.kde.spectacle applets-screenshooter accessories-screenshot', O(e_camera))
R('apps', 'okular org.kde.okular document-viewer evince', O(lambda ic: e_book(ic, RED) + place(e_magnifier(ic), 26, 26, .55)))
R('apps', 'gwenview org.kde.gwenview image-viewer eog', O(e_picture))
R('apps', 'ark org.kde.ark file-roller utilities-file-archiver', O(e_box))
R('apps', 'accessories-calculator kcalc org.kde.kcalc org.gnome.Calculator', O(e_calculator))
R('apps', 'accessories-character-map kcharselect org.kde.kcharselect', O(lambda ic: rect(6, 6, 52, 52, 5, ic.v(WHITE, .3, .15)) +
                                                                          text(32, 46, '&#937;', 36, ic.v(PURPLE), stroke=OL, sw=1.6)))
R('apps', 'elisa org.kde.elisa multimedia-audio-player audio-player rhythmbox amarok juk',
  O(lambda ic: e_disc(ic) + place(e_note(ic), 30, 28, .55)))
R('apps', 'dragonplayer org.kde.dragonplayer vlc mpv multimedia-video-player totem haruna org.kde.haruna celluloid smplayer',
  O(lambda ic: e_tv(ic) + place(e_play(ic), 20, 14, .38)))
R('apps', 'com.obsproject.Studio obs obs-studio', O(lambda ic: e_badge(ic, DARK, circle(32, 32, 10, ic.ball(RED), None))))
R('apps', 'kamoso org.kde.kamoso cheese', O(lambda ic: e_camera(ic, '#3a3d4c')))
R('apps', 'filelight org.kde.filelight baobab', O(e_pie))
R('apps', 'partitionmanager org.kde.partitionmanager gparted gnome-disks org.gnome.DiskUtility',
  O(lambda ic: e_hdd(ic) + place(e_pie(ic), 34, 0, .45)))
R('apps', 'btrfs-assistant', O(lambda ic: e_hdd(ic) + place(e_refresh(ic), 34, 0, .45)))
R('apps', 'utilities-system-monitor org.kde.plasma-systemmonitor ksysguard plasma-systemmonitor gnome-system-monitor '
          'org.gnome.SystemMonitor htop btop', O(e_monitor_graph))
R('apps', 'hwinfo org.kde.kinfocenter kinfocenter hardinfo', O(lambda ic: e_chip(ic) + place(e_info(ic), 34, 34, .45)))
R('apps', 'kfind org.kde.kfind system-search search', O(e_magnifier))
R('apps', 'krunner plasma-search', O(lambda ic: e_magnifier(ic) + place(e_rocket(ic), 34, 30, .45)))
R('apps', 'system-run', O(e_rocket))
R('apps', 'kfontview kfontinst preferences-desktop-font font-viewer org.gnome.font-viewer preferences-desktop-font-installer', O(e_font))
R('apps', 'kmenuedit', O(lambda ic: e_lines(ic) + place(e_pencil(ic), 26, 22, .6)))
R('apps', 'klipper edit-paste-app', O(e_clipboard))
R('apps', 'kwalletmanager kwallet org.kde.kwalletmanager5 seahorse org.gnome.seahorse.Application', O(e_lock))
R('apps', 'kleopatra org.kde.kleopatra org.kde.kwatchgnupg kgpg gnupg pinentry', O(lambda ic: e_shield(ic, NAVY, False) +
                                                                                    place(e_key(ic), 16, 14, .5)))
R('apps', 'firewall-config firewall gufw', O(lambda ic: e_shield(ic, RED, False) + place(e_lightning(ic, YELLOW), 18, 12, .45)))
R('apps', 'kdeconnect org.kde.kdeconnect kdeconnect-app', O(lambda ic: e_phone(ic) + place(e_wifi(ic), 34, 0, .45)))
R('apps', 'kmail kmail2 org.kde.kmail2 thunderbird org.mozilla.Thunderbird internet-mail evolution mail-client '
          'geary sieveeditor', O(e_mail))
R('apps', 'kontact org.kde.kontact kontact-import-wizard', O(lambda ic: e_mail(ic) + place(e_calendar(ic), 30, 26, .5)))
R('apps', 'korganizer org.kde.korganizer office-calendar gnome-calendar evolution-calendar', O(e_calendar))
R('apps', 'kaddressbook org.kde.kaddressbook office-address-book contacts x-office-address-book-app', O(e_contact))
R('apps', 'akregator org.kde.akregator rss feedreader', O(lambda ic: e_badge(ic, ORANGE, circle(22, 42, 4.5, WHITE, None) +
                                                                           ostroke(arc_pts(20, 44, 14, -90, 0), WHITE, 4, 4) +
                                                                           ostroke(arc_pts(20, 44, 24, -90, 0), WHITE, 4, 4))))
R('apps', 'ktnef', O(lambda ic: e_mail(ic) + place(e_box(ic), 34, 34, .45)))
R('apps', 'org.kde.neochat neochat konversation org.kde.konversation internet-chat irc element discord '
          'com.discordapp.Discord', O(e_chat))
R('apps', 'krdc org.kde.krdc remmina preferences-system-network-remote vncviewer',
  O(lambda ic: e_monitor(ic) + place(e_arrow(ic, GREEN, 0), 34, 32, .45)))
R('apps', 'krfb org.kde.krfb desktop-sharing', O(lambda ic: e_monitor(ic) + place(e_people(ic), 32, 30, .5)))
R('apps', 'knetattach', O(lambda ic: e_globe(ic) + place(e_plus(ic), 36, 36, .4)))
R('apps', 'ktip help-hint', O(lambda ic: e_badge(ic, YELLOW, circle(32, 26, 10, WHITE, None) + rect(27, 36, 10, 10, 2, WHITE, None))))
R('apps', 'kmouth', O(lambda ic: e_chat(ic, AMBER)))
R('apps', 'orca preferences-desktop-accessibility accessibility', O(e_accessibility))
R('apps', 'kolourpaint org.kde.kolourpaint mspaint paint pinta', O(lambda ic: e_palette(ic) + place(e_brush(ic), 28, 24, .6)))
R('apps', 'krita org.kde.krita gimp org.gimp.GIMP', O(lambda ic: e_brush(ic, MAGENTA) + place(e_palette(ic), 30, 2, .5)))
R('apps', 'com.orama_interactive.Pixelorama pixelorama aseprite', O(lambda ic: e_grid(ic) + place(e_pencil(ic), 30, 26, .55)))
R('apps', 'inkscape org.inkscape.Inkscape', O(e_draw))
R('apps', 'blender org.blender.Blender', O(lambda ic: e_layers(ic) + place(e_ball(ic), 34, 0, .4)))
R('apps', 'kpat org.kde.kpat solitaire', O(e_cards))
R('apps', 'kmines org.kde.kmines winemine gnome-mines', O(e_mine))
R('apps', 'kmahjongg org.kde.kmahjongg', O(e_tile))
R('apps', 'com.valvesoftware.Steam steam', O(e_steam))
R('apps', 'net.lutris.Lutris lutris com.heroicgameslauncher.hgl heroic net.davidotek.pupgui2 com.vysp3r.ProtonPlus '
          'protonup-qt preferences-desktop-gaming', O(lambda ic: e_gamepad(ic) + place(e_star(ic, AMBER), 38, 0, .4)))
R('apps', 'io.github.TheMrGeeBee.MosaicModManager', O(lambda ic: e_gamepad(ic) + place(e_puzzle(ic), 38, 0, .4)))
R('apps', 'wine winecfg winefile winhelp regedit msiexec wine-program wine-browser', O(e_wine))
R('apps', 'org.dosbox-staging.dosbox-staging dosbox', O(lambda ic: e_computer(ic) + place(e_ball(ic), 40, 0, .35)))
R('apps', 'net.fsuae.FS-UAE net.fsuae.FS-UAE.Launcher fs-uae fs-uae-launcher amiberry', O(lambda ic: e_amiga(ic) +
                                                                                           place(e_ball(ic), 21, 0, .36)))
R('apps', 'qemu virt-manager virt-viewer virtualbox org.virt_manager.virt-manager gnome-boxes', O(e_vm))
R('apps', 'vscode code com.visualstudio.code co.anysphere.cursor cursor dev.zed.Zed zed com.jetbrains.WebStorm '
          'webstorm jetbrains-toolbox applications-development-ide kdevelop org.kde.kdevelop',
  O(lambda ic: e_window(ic, PURPLE, place(e_code(ic), 14, 20, .55))))
R('apps', 'rest.insomnia.Insomnia insomnia postman', O(lambda ic: e_window(ic, MAGENTA, place(e_arrow(ic, GREEN), 18, 22, .45))))
R('apps', 'unityhub unityhub-unity-editor godot org.godotengine.Godot', O(lambda ic: e_layers(ic) + place(e_gamepad(ic), 32, 34, .45)))
R('apps', 'libreoffice-startcenter libreoffice office applications-office-suite', O(lambda ic: e_pages(ic)))
R('apps', 'libreoffice-writer writer abiword', O(lambda ic: document(ic, BLUE, e_lines(ic)) ))
R('apps', 'libreoffice-calc calc gnumeric', O(lambda ic: document(ic, GREEN, e_sheet(ic))))
R('apps', 'libreoffice-impress impress', O(lambda ic: document(ic, ORANGE, e_slides(ic))))
R('apps', 'libreoffice-draw', O(lambda ic: document(ic, AMBER, e_draw(ic))))
R('apps', 'libreoffice-math', O(lambda ic: document(ic, GREY, e_sigma(ic))))
R('apps', 'libreoffice-base', O(lambda ic: document(ic, PURPLE, e_layers(ic))))
R('apps', 'skanpage org.kde.skanpage skanlite simple-scan', O(e_scanner))
R('apps', 'org.kde.qrca qrca', O(e_qr))
R('apps', 'org.fedoraproject.MediaWriter mediawriter', O(lambda ic: e_usb(ic) + place(e_ball(ic), 34, 0, .4)))
R('apps', 'org.fedoraproject.AnacondaInstaller anaconda system-installer', O(lambda ic: e_hdd(ic) + place(e_download(ic), 18, 0, .5)))
R('apps', 'abrt org.freedesktop.GnomeAbrt tools-report-bug drkonqi', O(e_bug))
R('apps', 'org.kde.kjournaldbrowser kjournald logview gnome-logs', O(lambda ic: e_book(ic, BROWN) + place(e_magnifier(ic), 26, 26, .5)))
R('apps', 'kvantum kvantummanager', O(lambda ic: e_palette(ic) + place(e_gear(ic), 34, 34, .45)))
R('apps', 'ibus ibus-setup ibus-engine ibus-anthy ibus-setup-hangul ibus-typing-booster ibus-bopomofo ibus-pinyin '
          'org.freedesktop.IBus.Chewing.Setup', O(lambda ic: e_keyboard(ic) + place(e_globe(ic), 36, 0, .42)))
R('apps', 'org.kde.xwaylandvideobridge xwaylandvideobridge', O(lambda ic: e_monitor(ic) + place(e_arrow(ic, GREEN), 18, 12, .4)))
R('apps', 'xorg x11', O(e_monitor))
R('apps', 'get-hot-new-stuff knewstuff', O(lambda ic: e_box(ic) + place(e_star(ic), 30, 0, .5)))
R('apps', 'kde-frameworks', O(e_puzzle))
R('apps', 'baloo preferences-desktop-baloo', O(lambda ic: e_magnifier(ic) + place(e_lines(ic), 4, 4, .4)))
R('apps', 'akonadi akonadi-ews account-google preferences-online-accounts goa-panel',
  O(lambda ic: e_cloud(ic) + place(e_user(ic), 20, 26, .45)))
R('apps', 'claude', O(lambda ic: e_badge(ic, '#d97757', path(star_pts(32, 32, 18, 5, 8), WHITE, None))))
R('apps', 'redshift redshift-status-on', O(e_redshift))
R('apps', 'kgamma preferences-desktop-color colord', O(e_palette))
R('apps', 'org.kde.plasma.emojier preferences-desktop-emoticons face-smile', O(lambda ic: circle(32, 32, 28, ic.ball(YELLOW)) +
                                                                                circle(23, 25, 4, DARK, None) + circle(41, 25, 4, DARK, None) +
                                                                                ostroke(arc_pts(32, 32, 16, 30, 150), DARK, 3.5, 3.5)))

# ============================================================ CATEGORIES
R('categories', 'applications-accessories applications-utilities', O(e_toolbox))
R('categories', 'applications-development applications-engineering', O(lambda ic: e_window(ic, PURPLE, place(e_code(ic), 14, 20, .55))))
R('categories', 'applications-education applications-science', O(lambda ic: e_book(ic, GREEN)))
R('categories', 'applications-games', O(e_gamepad))
R('categories', 'applications-graphics', O(lambda ic: e_palette(ic) + place(e_brush(ic), 28, 24, .6)))
R('categories', 'applications-internet', O(e_globe))
R('categories', 'applications-multimedia', O(lambda ic: e_film_clapper(ic) + place(e_note(ic), 34, 0, .45)))
R('categories', 'applications-office', O(e_pages))
R('categories', 'applications-system', O(lambda ic: e_computer(ic) + place(e_gear(ic), 36, 32, .45)))
R('categories', 'applications-other applications-all', O(e_grid))
R('categories', 'preferences-system-network preferences-system-network-connection network-connect',
  O(lambda ic: e_globe(ic) + place(e_network(ic), 34, 30, .5)))
R('categories', 'preferences-system-network-proxy', O(lambda ic: e_globe(ic) + place(e_shield(ic, GREEN, False), 34, 30, .5)))
R('categories', 'preferences-desktop-activities', O(e_grid))
R('categories', 'preferences-desktop-animations preferences-desktop-effects preferences-system-windows-effect',
  O(lambda ic: e_window(ic) + place(e_star(ic), 30, 28, .5)))
R('categories', 'preferences-desktop-cursors', O(e_cursor))
R('categories', 'preferences-desktop-default-applications', O(lambda ic: e_grid(ic) + place(e_check(ic), 30, 30, .5)))
R('categories', 'preferences-desktop-display-randr preferences-desktop-display-color', O(e_monitor))
R('categories', 'preferences-desktop-feedback', O(e_hourglass))
R('categories', 'preferences-desktop-filetype-association', O(lambda ic: document(ic, GREEN, e_gear(ic))))
R('categories', 'preferences-desktop-icons', O(e_grid))
R('categories', 'preferences-desktop-keyboard preferences-desktop-keyboard-shortcut', O(e_keyboard))
R('categories', 'preferences-desktop-locale preferences-desktop-locale-symbolic-alt', O(e_flag))
R('categories', 'preferences-desktop-mouse', O(e_mouse))
R('categories', 'preferences-desktop-notification-bell preferences-desktop-notification notifications', O(e_bell))
R('categories', 'preferences-desktop-plasma-theme preferences-desktop-theme preferences-desktop-theme-applications '
                'preferences-desktop-theme-global preferences-desktop-color-scheme', O(e_palette))
R('categories', 'preferences-desktop-theme-windowdecorations preferences-system-windows', O(e_window))
R('categories', 'preferences-desktop-sound preferences-desktop-multimedia', O(e_speaker))
R('categories', 'preferences-desktop-tablet', O(e_tablet))
R('categories', 'preferences-desktop-thunderbolt', O(e_lightning))
R('categories', 'preferences-desktop-touchpad', O(e_touchpad))
R('categories', 'preferences-desktop-touchscreen', O(e_phone))
R('categories', 'preferences-desktop-user-password preferences-desktop-user', O(lambda ic: e_user(ic) + place(e_key(ic), 34, 32, .45)))
R('categories', 'preferences-desktop-virtual', O(e_layers))
R('categories', 'preferences-desktop-wallpaper', O(e_picture))
R('categories', 'preferences-devices-printer', O(e_printer))
R('categories', 'preferences-security security-high preferences-system-privacy', O(e_shield))
R('categories', 'preferences-smart-status', O(lambda ic: e_hdd(ic) + place(e_ok(ic), 34, 0, .45)))
R('categories', 'preferences-system-login preferences-system-users system-users-alt', O(e_people))
R('categories', 'preferences-system-power-management preferences-system-power', O(lambda ic: e_battery(ic) + place(e_lightning(ic), 18, 14, .45)))
R('categories', 'preferences-system-session-services preferences-system-session', O(e_gear))
R('categories', 'preferences-system-splash', O(lambda ic: e_monitor(ic) + place(e_ball(ic), 20, 12, .4)))
R('categories', 'preferences-system-tabbox', O(e_layers))
R('categories', 'preferences-system-time preferences-system-date', O(e_clock))
R('categories', 'preferences-system-windows-actions preferences-system-windows-behavior', O(lambda ic: e_window(ic) + place(e_cursor(ic), 30, 26, .5)))
R('categories', 'preferences-web-browser-shortcuts preferences-web-browser', O(e_globe))
R('categories', 'preferences-kde-connect', O(e_phone))

# ============================================================ ACTIONS
R('actions', 'document-new tab-new-doc', P(lambda ic: document(ic, GREEN, None) + place(e_plus(ic), 30, 30, .5)))
R('actions', 'document-open fileopen', P(lambda ic: folder(ic, DRAWER, None, True)))
R('actions', 'document-open-recent', P(lambda ic: folder(ic, DRAWER, e_clock(ic), True)))
R('actions', 'document-save filesave', P(e_floppy))
R('actions', 'document-save-as filesaveas', P(lambda ic: e_floppy(ic) + place(e_pencil(ic), 30, 30, .5)))
R('actions', 'document-save-all', P(lambda ic: place(e_floppy(ic, BLUE), 0, 0, .7) + place(e_floppy(ic), 18, 18, .7)))
R('actions', 'document-print fileprint', P(e_printer))
R('actions', 'document-print-preview', P(lambda ic: e_printer(ic) + place(e_magnifier(ic), 30, 30, .5)))
R('actions', 'document-properties document-info', P(lambda ic: document(ic, BLUE, None) + place(e_info(ic), 30, 30, .5)))
R('actions', 'document-edit edit-entry', P(lambda ic: document(ic, BLUE, None) + place(e_pencil(ic), 28, 26, .55)))
R('actions', 'document-export', P(lambda ic: document(ic, BLUE, None) + place(e_arrow(ic, GREEN), 30, 30, .5)))
R('actions', 'document-import', P(lambda ic: document(ic, BLUE, None) + place(e_arrow(ic, GREEN, 180), 30, 30, .5)))
R('actions', 'document-close', P(lambda ic: document(ic, BLUE, None) + place(e_cross(ic), 30, 30, .5)))
R('actions', 'document-revert', P(lambda ic: document(ic, BLUE, None) + place(e_undo(ic), 30, 30, .5)))
R('actions', 'folder-new folder-add', P(lambda ic: folder(ic) + place(e_plus(ic), 34, 30, .45)))
R('actions', 'edit-copy editcopy', P(e_pages))
R('actions', 'edit-cut editcut', P(e_scissors))
R('actions', 'edit-paste editpaste', P(e_clipboard))
R('actions', 'edit-delete delete edit-delete-shred', P(lambda ic: e_trash(ic)))
R('actions', 'edit-undo', P(e_undo))
R('actions', 'edit-redo', P(lambda ic: e_undo(ic, AMBER, True)))
R('actions', 'edit-find edit-find-replace find', P(e_magnifier))
R('actions', 'edit-clear edit-clear-all edit-clear-history', P(lambda ic: e_brush(ic, YELLOW)))
R('actions', 'edit-select-all', P(lambda ic: e_lines(ic) + rect(4, 4, 56, 56, 3, 'none', BLUE, 3, ' stroke-dasharray="6 4"')))
R('actions', 'edit-rename', P(e_pencil))
R('actions', 'list-add add', P(e_plus))
R('actions', 'list-remove remove', P(e_minus))
R('actions', 'go-next go-next-view arrow-right', P(e_arrow))
R('actions', 'go-previous go-previous-view arrow-left go-back', P(lambda ic: e_arrow(ic, BLUE, 180)))
R('actions', 'go-up arrow-up', P(lambda ic: e_arrow(ic, BLUE, -90)))
R('actions', 'go-down arrow-down', P(lambda ic: e_arrow(ic, BLUE, 90)))
R('actions', 'go-last go-jump', P(e_arrow_end))
R('actions', 'go-first', P(lambda ic: e_arrow_end(ic, BLUE, 180)))
R('actions', 'go-top', P(lambda ic: e_arrow_end(ic, BLUE, -90)))
R('actions', 'go-bottom', P(lambda ic: e_arrow_end(ic, BLUE, 90)))
R('actions', 'go-home', P(e_house))
R('actions', 'view-refresh reload view-refresh-symbolic-alt', P(e_refresh))
R('actions', 'process-stop stop', P(lambda ic: path('M20,4 H44 L60,20 V44 L44,60 H20 L4,44 V20 Z', ic.v(RED)) +
                                     rect(14, 26, 36, 12, 2, WHITE, None)))
R('actions', 'zoom-in', P(lambda ic: e_magnifier(ic) + place(e_plus(ic), 14, 14, .3)))
R('actions', 'zoom-out', P(lambda ic: e_magnifier(ic) + place(e_minus(ic), 14, 14, .3)))
R('actions', 'zoom-original zoom-fit-best', P(e_magnifier))
R('actions', 'view-preview view-visible', P(e_eye))
R('actions', 'view-list-icons view-grid', P(e_grid))
R('actions', 'view-list-details view-list-text view-list-tree', P(e_lines))
R('actions', 'window-close tab-close dialog-close', P(e_cross))
R('actions', 'window-new', P(lambda ic: e_window(ic) + place(e_plus(ic), 30, 30, .45)))
R('actions', 'tab-new', P(lambda ic: e_window(ic, GREEN) + place(e_plus(ic), 30, 30, .45)))
R('actions', 'application-exit system-shutdown exit', P(e_power))
R('actions', 'system-log-out', P(lambda ic: e_window(ic, RED) + place(e_arrow(ic, GREEN), 18, 22, .5)))
R('actions', 'system-reboot', P(lambda ic: e_badge(ic, GREEN, '') + place(e_refresh(ic, WHITE), 12, 12, .62)))
R('actions', 'system-lock-screen', P(e_lock))
R('actions', 'system-suspend system-suspend-hibernate system-hibernate', P(e_moon))
R('actions', 'system-switch-user', P(e_people))
R('actions', 'system-search', P(e_magnifier))
R('actions', 'configure settings-configure preferences-configure', P(e_gear))
R('actions', 'configure-shortcuts', P(e_keyboard))
R('actions', 'help-contents-action help-about', P(e_info))
R('actions', 'help-whatsthis', P(e_question))
R('actions', 'dialog-ok dialog-ok-apply object-select', P(e_check))
R('actions', 'dialog-cancel', P(e_cross))
R('actions', 'media-playback-start media-playback-playing', P(e_play))
R('actions', 'media-playback-pause', P(lambda ic: rect(12, 8, 14, 48, 3, ic.v(BLUE)) + rect(38, 8, 14, 48, 3, ic.v(BLUE))))
R('actions', 'media-playback-stop', P(lambda ic: rect(10, 10, 44, 44, 4, ic.v(RED)) + gloss_rect(ic, 12, 12, 40, 14, 3, .5)))
R('actions', 'media-record', P(lambda ic: circle(32, 32, 24, ic.ball(RED))))
R('actions', 'media-skip-forward', P(lambda ic: place(e_play(ic, BLUE), -6, 6, .8) + rect(44, 10, 10, 44, 2, ic.v(BLUE))))
R('actions', 'media-skip-backward', P(lambda ic: g(place(e_play(ic, BLUE), -6, 6, .8) + rect(44, 10, 10, 44, 2, ic.v(BLUE)),
                                                   'translate(64 0) scale(-1 1)')))
R('actions', 'media-seek-forward', P(lambda ic: place(e_play(ic, BLUE), -6, 10, .7) + place(e_play(ic, BLUE), 18, 10, .7)))
R('actions', 'media-seek-backward', P(lambda ic: g(place(e_play(ic, BLUE), -6, 10, .7) + place(e_play(ic, BLUE), 18, 10, .7),
                                                   'translate(64 0) scale(-1 1)')))
R('actions', 'mail-message-new mail-compose', P(lambda ic: e_mail(ic) + place(e_pencil(ic), 30, 26, .55)))
R('actions', 'mail-receive mail-get', P(lambda ic: e_mail(ic) + place(e_download(ic), 30, 26, .5)))
R('actions', 'mail-send mail-send-receive', P(lambda ic: e_mail(ic) + place(e_arrow(ic, GREEN), 30, 30, .5)))
R('actions', 'mail-reply-sender mail-reply-all mail-forward', P(lambda ic: e_mail(ic) + place(e_undo(ic), 30, 30, .5)))
R('actions', 'contact-new list-add-user', P(lambda ic: e_user(ic) + place(e_plus(ic), 34, 34, .45)))
R('actions', 'bookmark-new bookmark-add', P(lambda ic: e_bookmark(ic) + place(e_plus(ic), 34, 34, .45)))
R('actions', 'bookmarks-organize bookmark-edit', P(lambda ic: e_bookmark(ic) + place(e_pencil(ic), 30, 26, .5)))
R('actions', 'download', P(e_download))
R('actions', 'upload cloud-upload', P(e_upload))
R('actions', 'debug-run', P(lambda ic: e_bug(ic) + place(e_play(ic), 30, 30, .5)))
R('actions', 'tools-check-spelling', P(lambda ic: text(28, 32, 'abc', 24, DARK) + place(e_check(ic), 18, 30, .5)))
R('actions', 'favorite emblem-favorite-action', P(e_star))
R('actions', 'mark-location', P(e_location))
R('actions', 'insert-image', P(e_picture))
R('actions', 'insert-link', P(lambda ic: ostroke('M26,38 L38,26', SILVER, 5) + rect(4, 26, 30, 18, 9, 'none', OL, 8, ' transform="rotate(-45 19 35)"') +
                              rect(4, 26, 30, 18, 9, 'none', BLUE, 4.5, ' transform="rotate(-45 19 35)"') +
                              rect(30, 20, 30, 18, 9, 'none', OL, 8, ' transform="rotate(-45 45 29)"') +
                              rect(30, 20, 30, 18, 9, 'none', BLUE, 4.5, ' transform="rotate(-45 45 29)"')))
R('actions', 'run-build system-run-action', P(e_rocket))
R('actions', 'games-config-options', P(e_gamepad))
R('actions', 'office-chart-line office-chart-bar', P(e_chart))
R('actions', 'office-chart-pie', P(e_pie))
R('actions', 'view-calendar', P(e_calendar))
R('actions', 'appointment-new', P(lambda ic: e_calendar(ic) + place(e_plus(ic), 34, 34, .45)))
R('actions', 'user-online', P(lambda ic: circle(32, 32, 20, ic.ball(GREEN))))
R('actions', 'user-away', P(lambda ic: circle(32, 32, 20, ic.ball(AMBER))))
R('actions', 'user-busy', P(lambda ic: circle(32, 32, 20, ic.ball(RED))))
R('actions', 'user-offline', P(lambda ic: circle(32, 32, 20, ic.ball(GREY))))
R('actions', 'format-text-bold', P(lambda ic: text(32, 52, 'B', 54, ic.v(DARK), stroke=OL, sw=1)))
R('actions', 'format-text-italic', P(lambda ic: text(32, 52, 'I', 54, ic.v(DARK), 'bold" font-style="italic', stroke=OL, sw=1,
                                                     family='DejaVu Serif,Serif')))
R('actions', 'format-text-underline', P(lambda ic: text(32, 46, 'U', 48, ic.v(DARK), stroke=OL, sw=1) + rect(12, 52, 40, 5, 2, BLUE, None)))

# ============================================================ STATUS
R('status', 'dialog-information messagebox_info', O(e_info))
R('status', 'dialog-warning messagebox_warning security-medium', O(e_warning))
R('status', 'dialog-error messagebox_critical security-low process-stop-status', O(e_error))
R('status', 'dialog-question', O(e_question))
R('status', 'dialog-positive task-complete', O(e_ok))
R('status', 'dialog-password system-user-prompt', O(lambda ic: e_key(ic) + place(e_lock(ic), 34, 34, .45)))
R('status', 'update-low', O(lambda ic: e_badge(ic, GREEN, '') + place(e_download(ic, WHITE), 14, 12, .55)))
R('status', 'update-medium', O(lambda ic: e_badge(ic, AMBER, '') + place(e_download(ic, WHITE), 14, 12, .55)))
R('status', 'update-high', O(lambda ic: e_badge(ic, RED, '') + place(e_download(ic, WHITE), 14, 12, .55)))
R('status', 'network-vpn', O(lambda ic: e_shield(ic, GREEN, False) + place(e_lock(ic), 18, 16, .45)))
R('status', 'network-wireless-hotspot', O(lambda ic: e_wifi(ic, AMBER)))
R('status', 'image-loading', O(e_hourglass))
R('status', 'image-missing', O(lambda ic: e_picture(ic) + place(e_error(ic), 30, 30, .5)))
R('status', 'mail-unread mail-unread-new', O(lambda ic: e_mail(ic) + place(circle(32, 32, 24, ic.ball(RED)), 36, 0, .4)))
R('status', 'appointment-soon alarm', O(e_clock))
R('status', 'weather-clear', O(e_sun))
R('status', 'weather-clear-night', O(e_moon))
R('status', 'weather-overcast weather-few-clouds', O(e_cloud))
R('status', 'printer-printing', O(lambda ic: e_printer(ic) + place(e_play(ic), 34, 34, .4)))
R('status', 'printer-error', O(lambda ic: e_printer(ic) + place(e_error(ic), 34, 34, .45)))

# ============================================================ EMBLEMS
R('emblems', 'emblem-favorite emblem-favorites', P(e_star))
R('emblems', 'emblem-important emblem-urgent', P(e_warning))
R('emblems', 'emblem-locked emblem-readonly emblem-encrypted-locked', P(e_lock))
R('emblems', 'emblem-unlocked emblem-encrypted-unlocked', P(lambda ic: ostroke('M20,30 V20 A12,12 0 0,1 44,14', SILVER, 6) +
                                                               rect(10, 28, 44, 30, 5, ic.v(GREEN, .5, .3))))
R('emblems', 'emblem-symbolic-link', P(lambda ic: e_badge(ic, BLUE, '') + place(e_arrow(ic, WHITE, -45), 12, 12, .62)))
R('emblems', 'emblem-shared emblem-share', P(lambda ic: e_badge(ic, TEAL, '') + place(e_people(ic), 12, 10, .62)))
R('emblems', 'emblem-mounted', P(lambda ic: e_badge(ic, GREEN, '') + place(e_play(ic, WHITE), 14, 14, .55)))
R('emblems', 'emblem-unmounted', P(lambda ic: e_badge(ic, GREY, '') + place(e_minus(ic, WHITE), 14, 14, .55)))
R('emblems', 'emblem-success emblem-checked emblem-default emblem-ok', P(e_ok))
R('emblems', 'emblem-error emblem-unavailable', P(e_error))
R('emblems', 'emblem-warning', P(e_warning))
R('emblems', 'emblem-information', P(e_info))
R('emblems', 'emblem-question', P(e_question))
R('emblems', 'emblem-new', P(lambda ic: e_star(ic, ORANGE)))
R('emblems', 'emblem-downloads', P(e_download))
R('emblems', 'emblem-music', P(e_note))
R('emblems', 'emblem-photos', P(e_picture))
R('emblems', 'emblem-system', P(e_gear))
R('emblems', 'emblem-synchronizing emblem-sync', P(e_refresh))
R('emblems', 'emblem-mail', P(e_mail))


# ============================================================ write
INDEX = """[Icon Theme]
Name=AmigaGloss
Comment=Glossy Workbench-4 style icons for KDE Plasma
Inherits=breeze,hicolor
Example=folder
DisplayDepth=32
LinkOverlay=emblem-symbolic-link
LockOverlay=emblem-locked
ZipOverlay=package-x-generic
FollowsColorScheme=true

Directories={dirs}

"""


def main(out):
    ctxs = sorted({c for c, _ in REG} | {c for c, _, _ in ALIAS})
    ctxname = {'actions': 'Actions', 'apps': 'Applications', 'categories': 'Categories', 'devices': 'Devices',
               'emblems': 'Emblems', 'mimetypes': 'MimeTypes', 'places': 'Places', 'status': 'Status'}
    if os.path.isdir(out):
        shutil.rmtree(out)
    dirs = ['scalable/%s' % c for c in ctxs]
    idx = INDEX.format(dirs=','.join(dirs))
    for c in ctxs:
        idx += '[scalable/%s]\nSize=64\nMinSize=8\nMaxSize=512\nType=Scalable\nContext=%s\n\n' % (c, ctxname[c])
        os.makedirs(os.path.join(out, 'scalable', c))
    with open(os.path.join(out, 'index.theme'), 'w') as f:
        f.write(idx)
    n = 0
    for (c, name), fn in REG.items():
        ic = Icon()
        with open(os.path.join(out, 'scalable', c, name + '.svg'), 'w') as f:
            f.write(ic.render(fn(ic)))
        n += 1
    a = 0
    for c, al, tgt in ALIAS:
        p = os.path.join(out, 'scalable', c, al + '.svg')
        if os.path.lexists(p) or (c, al) in REG:
            continue
        os.symlink(tgt + '.svg', p)
        a += 1
    print('%d icons, %d aliases -> %s' % (n, a, out))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'AmigaGloss')
