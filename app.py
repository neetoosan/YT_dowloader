#!/usr/bin/env python3
"""
YouTube Downloader with Kivy GUI
Requires: pip install kivy yt-dlp
"""
import os
import threading
from pathlib import Path
import yt_dlp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView


class YouTubeDownloader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Download path
        self.download_path = str(Path.home() / "Downloads")
        
        # Available formats
        self.formats = {
            'Best Quality (MP4)': 'best[ext=mp4]',
            'Best Audio (MP3)': 'bestaudio[ext=m4a]/bestaudio',
            'HD 1080p (MP4)': 'best[height<=1080][ext=mp4]',
            'HD 720p (MP4)': 'best[height<=720][ext=mp4]',
            'Standard 480p (MP4)': 'best[height<=480][ext=mp4]',
            'Audio Only (M4A)': 'bestaudio[ext=m4a]',
            'Audio Only (WEBM)': 'bestaudio[ext=webm]',
            'Worst Quality (Small File)': 'worst'
        }
        
        self.build_ui()
    
    def build_ui(self):
        # Title
        title = Label(text='YouTube Downloader', size_hint_y=None, height=40,
                     font_size=20, bold=True)
        self.add_widget(title)
        
        # URL input
        url_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        url_layout.add_widget(Label(text='YouTube URL:', size_hint_x=None, width=100))
        self.url_input = TextInput(multiline=False, hint_text='Paste YouTube URL here...')
        url_layout.add_widget(self.url_input)
        self.add_widget(url_layout)
        
        # Format selection
        format_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        format_layout.add_widget(Label(text='Format:', size_hint_x=None, width=100))
        self.format_spinner = Spinner(
            text='Best Quality (MP4)',
            values=list(self.formats.keys()),
            size_hint_x=None,
            width=200
        )
        format_layout.add_widget(self.format_spinner)
        self.add_widget(format_layout)
        
        # Download path
        path_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        path_layout.add_widget(Label(text='Save to:', size_hint_x=None, width=100))
        self.path_label = Label(text=self.download_path, text_size=(None, None))
        path_layout.add_widget(self.path_label)
        browse_btn = Button(text='Browse', size_hint_x=None, width=100)
        browse_btn.bind(on_press=self.browse_folder)
        path_layout.add_widget(browse_btn)
        self.add_widget(path_layout)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.info_btn = Button(text='Get Info')
        self.info_btn.bind(on_press=self.get_video_info)
        btn_layout.add_widget(self.info_btn)
        
        self.download_btn = Button(text='Download')
        self.download_btn.bind(on_press=self.start_download)
        btn_layout.add_widget(self.download_btn)
        
        self.add_widget(btn_layout)
        
        # Progress bar
        self.progress = ProgressBar(max=100, size_hint_y=None, height=30)
        self.add_widget(self.progress)
        
        # Status label
        self.status_label = Label(text='Ready', size_hint_y=None, height=30)
        self.add_widget(self.status_label)
        
        # Info display
        info_scroll = ScrollView()
        self.info_label = Label(text='', text_size=(None, None), valign='top')
        info_scroll.add_widget(self.info_label)
        self.add_widget(info_scroll)
    
    def browse_folder(self, instance):
        """Open folder browser"""
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserListView(
            path=self.download_path,
            dirselect=True,
            filters=['']
        )
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select Download Folder',
            content=content,
            size_hint=(0.8, 0.8)
        )
        
        def select_folder(instance):
            if filechooser.selection:
                self.download_path = filechooser.selection[0]
                self.path_label.text = self.download_path
            popup.dismiss()
        
        select_btn.bind(on_press=select_folder)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def get_video_info(self, instance):
        """Get video information"""
        url = self.url_input.text.strip()
        if not url:
            self.show_popup('Error', 'Please enter a YouTube URL')
            return
        
        self.status_label.text = 'Getting video info...'
        self.info_btn.disabled = True
        
        def fetch_info():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    # Format info text
                    info_text = f"Title: {info.get('title', 'N/A')}\n"
                    info_text += f"Duration: {self.format_duration(info.get('duration', 0))}\n"
                    info_text += f"Views: {info.get('view_count', 'N/A')}\n"
                    info_text += f"Uploader: {info.get('uploader', 'N/A')}\n"
                    info_text += f"Upload Date: {info.get('upload_date', 'N/A')}\n"
                    
                    # Available formats
                    formats = info.get('formats', [])
                    info_text += f"\nAvailable formats: {len(formats)}\n"
                    
                    Clock.schedule_once(lambda dt: self.update_info(info_text, True))
                    
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_info(f"Error: {str(e)}", False))
        
        thread = threading.Thread(target=fetch_info)
        thread.daemon = True
        thread.start()
    
    def update_info(self, text, success):
        """Update info display"""
        self.info_label.text = text
        self.info_label.text_size = (self.info_label.parent.width - 20, None)
        self.status_label.text = 'Info retrieved' if success else 'Error getting info'
        self.info_btn.disabled = False
    
    def format_duration(self, seconds):
        """Format duration in seconds to readable format"""
        if not seconds:
            return "N/A"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def start_download(self, instance):
        """Start download process"""
        url = self.url_input.text.strip()
        if not url:
            self.show_popup('Error', 'Please enter a YouTube URL')
            return
        
        self.download_btn.disabled = True
        self.progress.value = 0
        self.status_label.text = 'Starting download...'
        
        def download():
            try:
                format_code = self.formats[self.format_spinner.text]
                
                # Configure yt-dlp options
                ydl_opts = {
                    'format': format_code,
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                }
                
                # Convert audio formats to MP3 if needed
                if 'MP3' in self.format_spinner.text:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                Clock.schedule_once(lambda dt: self.download_complete(True))
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.download_complete(False, str(e)))
        
        thread = threading.Thread(target=download)
        thread.daemon = True
        thread.start()
    
    def progress_hook(self, d):
        """Progress callback for yt-dlp"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                Clock.schedule_once(lambda dt: self.update_progress(percent, 'Downloading...'))
            elif 'total_bytes_estimate' in d:
                percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                Clock.schedule_once(lambda dt: self.update_progress(percent, 'Downloading...'))
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_progress(100, 'Processing...'))
    
    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress.value = value
        self.status_label.text = f"{status} {value:.1f}%"
    
    def download_complete(self, success, error_msg=None):
        """Handle download completion"""
        self.download_btn.disabled = False
        
        if success:
            self.status_label.text = 'Download completed!'
            self.progress.value = 100
            self.show_popup('Success', f'Video downloaded successfully to:\n{self.download_path}')
        else:
            self.status_label.text = f'Download failed: {error_msg}'
            self.progress.value = 0
            self.show_popup('Error', f'Download failed:\n{error_msg}')
    
    def show_popup(self, title, message):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()


class YouTubeDownloaderApp(App):
    def build(self):
        self.title = 'YouTube Downloader'
        return YouTubeDownloader()


if __name__ == '__main__':
    YouTubeDownloaderApp().run()