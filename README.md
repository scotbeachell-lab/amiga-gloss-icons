# AmigaGloss icon theme for KDE Plasma

A glossy icon theme for KDE Plasma in the spirit of the AmigaOS 4.1 Workbench look: chunky shapes, thick outlines, bright gradients and soft drop shadows.

![Amiga ball](previews/amiga-ball.png)

All artwork is original. Every icon is drawn from code in Python and written out as SVG. Nothing was copied or traced from AmigaOS.

**Version:** v00.01

## What's included

- **~460 drawn icons** plus **~700 alias names**, so many apps and file types pick them up automatically
- **Places:** amber drawers with pictures for Documents, Downloads, Music, Pictures, Videos, Code and Games; 15 coloured drawers for Dolphin's "assign folder colour"; home, trash (empty and full), network, and a red/white checkered ball as the start button
- **Devices:** hard drive, SSD, floppy, CD/DVD, USB stick, SD card, keyboard, mouse, printer, scanner, monitor, laptop, a wedge home computer, and more
- **File types:** labelled documents (PDF, PY, ZIP, MP3, MKV, DOC…), including Amiga formats: ADF disk images, LHA archives and IFF pictures
- **Apps:** Dolphin, Konsole (a Shell window with a `1>` prompt), Kate, System Settings, Discover, Okular, Gwenview, Steam, Lutris, Wine, FS-UAE, VS Code and others, Blender, LibreOffice, and more
- **Settings categories, toolbar actions, dialog/status icons and file emblems**

Anything not covered falls back to **Breeze**.

## Previews

| | |
|---|---|
| Places ![](previews/places.png) | Devices ![](previews/devices.png) |
| Apps ![](previews/apps.png) | File types ![](previews/mimetypes.png) |
| Actions ![](previews/actions.png) | Categories ![](previews/categories.png) |
| Status ![](previews/status.png) | Emblems ![](previews/emblems.png) |

## Install

**From a release:** download `AmigaGloss-v00.01.tar.gz`, extract it into `~/.local/share/icons/`, then pick **AmigaGloss** in *System Settings → Colours & Themes → Icons*.

**From source** (needs only Python 3):

```sh
git clone https://github.com/scotbeachell-lab/amiga-gloss-icons.git
cd amiga-gloss-icons
./install.sh
/usr/libexec/plasma-changeicons AmigaGloss
```

### Start button

To get the checkered ball on your launcher, right-click it → *Configure* → click the icon → search for `start-here-amiga`. The common start-menu icon names (`start-here-kde`, `start-here-kde-symbolic`, `about_kde`) also map to the ball.

## How it works

| File | Purpose |
|---|---|
| `gen/lib.py` | Colours, gradients, shape and gloss primitives (64×64 canvas) |
| `gen/art.py` | Pictograms and objects (drawers, disks, globe, ball…) |
| `gen/objects.py` | Composite bases: drawer, document, tile |
| `gen/build.py` | Maps KDE/freedesktop icon names to drawings, then writes the theme |

To add or change an icon, add one line to `build.py`:

```python
R('apps', 'my-app org.example.MyApp', O(lambda ic: e_globe(ic) + place(e_star(ic), 34, 34, .45)))
```

The SVGs avoid filters, masks and clip paths, so Qt's SVG renderer draws them exactly like librsvg does.
