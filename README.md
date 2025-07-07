# YT_dowloader
# YouTube Downloader

A simple, user-friendly YouTube downloader with a graphical interface built using Python and Kivy.

## Features

- **Easy-to-use GUI** - Clean, intuitive interface
- **Multiple Format Options** - Download videos in various qualities and formats
- **Audio Extraction** - Download audio-only files in MP3, M4A, or WEBM
- **Custom Download Location** - Choose where to save your downloads
- **Video Information** - Preview video details before downloading
- **Progress Tracking** - Real-time download progress with percentage
- **Error Handling** - Clear error messages and status updates

## Available Download Formats

- Best Quality (MP4)
- HD 1080p (MP4)
- HD 720p (MP4)
- Standard 480p (MP4)
- Best Audio (MP3)
- Audio Only (M4A)
- Audio Only (WEBM)
- Worst Quality (Small File Size)

## Requirements

- Python 3.7 or higher
- Internet connection

## Installation & Usage

### Method 1: Run Python Script Directly

1. **Install Dependencies**
   ```bash
   pip install kivy yt-dlp
   ```
   
   Or simply run:
   ```bash
   install_requirements.bat
   ```

2. **Run the Application**
   ```bash
   python youtube_downloader.py
   ```

### Method 2: Build Executable (Recommended)

1. **Build EXE File**
   - Double-click `build_exe.bat`
   - Wait for the build process to complete
   - Find `YouTube_Downloader.exe` in the `dist` folder

2. **Run the Executable**
   - Double-click `YouTube_Downloader.exe`
   - No Python installation required!

## How to Use

1. **Enter YouTube URL** - Paste the video URL in the input field
2. **Select Format** - Choose your preferred download format from the dropdown
3. **Choose Location** - Click "Browse" to select download folder (defaults to Downloads)
4. **Get Info** (Optional) - Click "Get Info" to view video details
5. **Download** - Click "Download" to start the download process

## File Structure

```
YouTube-Downloader/
├── youtube_downloader.py      # Main application script
├── build_exe.bat             # Build executable file
├── install_requirements.bat   # Install dependencies
├── README.md                 # This file
└── dist/                     # Generated after building
    └── YouTube_Downloader.exe # Executable file
```

## Screenshots

The application features:
- URL input field for YouTube links
- Format selection dropdown
- Download path browser
- Progress bar with percentage
- Status messages
- Video information display

## Dependencies

- **Kivy** - GUI framework for cross-platform applications
- **yt-dlp** - Robust YouTube downloader library
- **PyInstaller** - For building executable files

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'yt_dlp'"**
- Run `install_requirements.bat` or manually install: `pip install yt-dlp`

**"No module named 'kivy'"**
- Run `install_requirements.bat` or manually install: `pip install kivy`

**Download fails**
- Check internet connection
- Verify the YouTube URL is valid
- Try a different format option

**Build fails**
- Ensure Python is installed and in PATH
- Run `install_requirements.bat` first
- Check if all dependencies are installed

### Tips

- Use "Get Info" to verify video details before downloading
- For audio-only downloads, choose MP3 format for best compatibility
- Large video files may take longer to download
- The app saves files with the video title as the filename

## Legal Notice

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download content you have permission to download.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your Python installation is working correctly

## License

This project is for educational and personal use. Please use responsibly and in accordance with applicable laws and terms of service.

---

**Enjoy downloading your favorite YouTube content!** 🎥📥
