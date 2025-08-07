# Raspberry Pi Photo Frame

A digital photo frame application designed for the **Raspberry Pi 3B**. It displays a slideshow of photos stored in a local folder, with a touchscreen-friendly fullscreen interface, GPS location lookup, and configurable settings.

## Features

- Fullscreen slideshow with automatic image cycling
- Forward/back navigation through photos
- GPS location display — reads coordinates from a GPS module via serial port and opens them in Google Maps
- Settings menu to configure the auto-advance delay (2s, 3s, 4s, 8s, or 16s), persisted to `Config.txt`

## Architecture

The application is built with **Python** and uses **Tkinter** as the graphical interface framework, running fullscreen on startup.

### Visual Interface (Tkinter)

All UI is rendered inside a single Tkinter root window (`root = Tk()`) set to fullscreen. Screens are composed of Tkinter `Button` and `Label` widgets arranged with the `grid` and `pack` geometry managers. Images are displayed as `Button` widgets (allowing tap/click to toggle fullscreen). Tkinter's `root.after()` is used to schedule automatic image advancement in slideshow mode without blocking the main loop.

### Screen State Machine

Navigation is controlled by a global `current_screen` integer. The `main()` function dispatches to the appropriate screen based on its value:

| Value | Screen |
|-------|--------|
| `0` | Main menu — 4-button grid (Pictures, Location, Settings, Exit) |
| `1` | Image viewer — photo with Back / Menu / Forward buttons |
| `2` | Fullscreen slideshow — photo auto-advances on a timer |
| `3` | GPS / My Location |
| `4` | Settings menu |

Transitioning between screens works by destroying the current screen's widgets, updating `current_screen`, and calling `main()` again.

### Key Files

| File | Purpose |
|------|---------|
| `ImageDatabase_015.py` | Main application entry point |
| `GPS_03.py` | GPS module — reads NMEA sentences from serial port `/dev/ttyS0`, parses coordinates, opens Google Maps in the browser |
| `Config.txt` | Persists the slideshow delay setting in milliseconds |
| `Images/` | UI icon assets for menu buttons |

### Image Handling

Photos are loaded from the path defined in `cloud_folder_path` (default: `/home/pi/Documents/Python/Projects/Photos`). Each image is resized to fit the screen using a custom `resizeimage_to_fit()` function that preserves the aspect ratio by applying the minimum of the width/height scale ratios. The `loadedImg` class stores a reference to each loaded `ImageTk.PhotoImage` object to prevent it from being garbage-collected by Python.

## Dependencies

```bash
pip install pillow pyserial
```

`tkinter` is included with the standard Python installation.

## Running

```bash
python3 ImageDatabase_015.py
```

Update `cloud_folder_path` in `ImageDatabase_015.py` to point to your local photos directory before running.

## Author

**Jonas dos Santos Silva**
eng.jonas.s@gmail.com
