import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
import os
from yt_dlp import YoutubeDL
import threading
import time
import subprocess
import winreg

class DownloaderUI:
    def __init__(self, root):
        self.root = root
        root.title("Reynaldo Yt-Mp4 - Pengunduh YouTube ke MP4")
        root.geometry("1200x800")
        root.configure(bg='#F0F2F5')  # Light blue-gray background
        
        # Set window icon
        try:
            # Convert PNG to PhotoImage for icon
            icon = tk.PhotoImage(file="Rty.png")
            root.iconphoto(True, icon)
            self.icon = icon  # Keep reference to prevent garbage collection
        except:
            # Fallback if icon file not found
            pass
        
        # Make window non-resizable
        root.resizable(False, False)
        
        # Center the window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main frame with gradient-like background
        main_frame = tk.Frame(root, bg='#FFFFFF', padx=20, pady=20)  # White background
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(main_frame, text="🎬 Reynaldo Yt-Mp4 🎬", 
                              font=('Arial', 24, 'bold'), 
                              fg='#1A73E8', bg='#FFFFFF')  # Google blue
        title_label.pack(pady=(0, 20))

        # Content frame
        content_frame = tk.Frame(main_frame, bg='#FFFFFF')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for controls (60% of width)
        left_frame = tk.Frame(content_frame, bg='#FFFFFF')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        content_frame.grid_columnconfigure(0, weight=6)  # 60% width

        # Right frame for downloaded files (40% of width)
        right_frame = tk.Frame(content_frame, bg='#F8F9FA', relief='raised', bd=2)  # Light gray
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0), expand=True)
        content_frame.grid_columnconfigure(1, weight=4)  # 40% width

        # URL input section
        url_frame = tk.Frame(left_frame, bg='#E8F0FE', relief='raised', bd=2, padx=15, pady=15)  # Light blue
        url_frame.pack(fill=tk.X, pady=(0, 15))

        url_label = tk.Label(url_frame, text="🔗 URL YouTube:", 
                            font=('Arial', 12, 'bold'), 
                            fg='#1A73E8', bg='#E8F0FE')  # Google blue
        url_label.pack(anchor="w")

        # URL entry with paste button
        url_input_frame = tk.Frame(url_frame, bg='#E8F0FE')
        url_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.url_entry = tk.Entry(url_input_frame, width=50, font=('Arial', 11), 
                                 relief='flat', bd=5)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.paste_button = tk.Button(url_input_frame, text="📋 Tempel", 
                                     command=self.paste_url,
                                     font=('Arial', 9, 'bold'),
                                     bg='#1A73E8', fg='white',  # Google blue
                                     relief='flat', padx=10, pady=2,
                                     cursor='hand2')
        self.paste_button.pack(side=tk.RIGHT)

        # Directory selection section
        dir_frame = tk.Frame(left_frame, bg='#F3E8FD', relief='raised', bd=2, padx=15, pady=15)  # Light purple
        dir_frame.pack(fill=tk.X, pady=(0, 15))

        self.output_dir = os.getcwd()
        # Frame horizontal untuk label, path, dan tombol
        dir_path_button_frame = tk.Frame(dir_frame, bg='#F3E8FD')
        dir_path_button_frame.pack(fill=tk.X, pady=(5, 10))

        output_dir_label = tk.Label(dir_path_button_frame, text="📁 Folder Tujuan:", 
                                   font=('Arial', 12, 'bold'), 
                                   fg='#8430CE', bg='#F3E8FD')  # Purple
        output_dir_label.pack(side=tk.LEFT)

        self.output_dir_display = tk.Label(dir_path_button_frame, text=self.output_dir, 
                                          wraplength=400, font=('Arial', 10),
                                          fg='#8430CE', bg='#F3E8FD')  # Purple
        self.output_dir_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        self.choose_dir_button = tk.Button(dir_path_button_frame, text="📂 Pilih Folder", 
                                          command=self.choose_directory,
                                          font=('Arial', 10, 'bold'),
                                          bg='#8430CE', fg='white',  # Purple
                                          relief='flat', padx=20, pady=5,
                                          cursor='hand2')
        self.choose_dir_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Download method selection section
        method_frame = tk.Frame(left_frame, bg='#E8F5E8', relief='raised', bd=2, padx=15, pady=15)  # Light green
        method_frame.pack(fill=tk.X, pady=(0, 15))

        method_label = tk.Label(method_frame, text="⚙️ Metode Download:", 
                               font=('Arial', 12, 'bold'), 
                               fg='#2E7D32', bg='#E8F5E8')  # Dark green
        method_label.pack(anchor="w")

        # Radio buttons for download method
        self.download_method = tk.StringVar()
        self.download_method.set("auto")  # Default to auto

        method_options_frame = tk.Frame(method_frame, bg='#E8F5E8')
        method_options_frame.pack(fill=tk.X, pady=(10, 0))

        # Peletakan radio button secara horizontal
        self.auto_radio = tk.Radiobutton(method_options_frame, text="🔄 Otomatis (IDM jika tersedia)", 
                                        variable=self.download_method, value="auto",
                                        font=('Arial', 10), bg='#E8F5E8', fg='#2E7D32',
                                        activebackground='#E8F5E8', selectcolor='#C8E6C9')
        self.auto_radio.pack(side=tk.LEFT, padx=5)

        self.idm_radio = tk.Radiobutton(method_options_frame, text="⚡ Paksa IDM (Lebih Cepat)", 
                                       variable=self.download_method, value="idm",
                                       font=('Arial', 10), bg='#E8F5E8', fg='#2E7D32',
                                       activebackground='#E8F5E8', selectcolor='#C8E6C9')
        self.idm_radio.pack(side=tk.LEFT, padx=5)

        self.direct_radio = tk.Radiobutton(method_options_frame, text="📥 Download Langsung (yt-dlp)", 
                                          variable=self.download_method, value="direct",
                                          font=('Arial', 10), bg='#E8F5E8', fg='#2E7D32',
                                          activebackground='#E8F5E8', selectcolor='#C8E6C9')
        self.direct_radio.pack(side=tk.LEFT, padx=5)

        # Control buttons section
        control_frame = tk.Frame(left_frame, bg='#FFFFFF')
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Queue button with caption
        queue_frame = tk.Frame(control_frame, bg='#FFFFFF')
        queue_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.queue_button = tk.Button(queue_frame, text="📋 Masuk Antrian", 
                                    command=self.add_to_queue_from_entry,
                                    font=('Arial', 14, 'bold'),
                                    bg='#1A73E8', fg='white',  # Google blue
                                    relief='flat', padx=30, pady=10,
                                    cursor='hand2')
        self.queue_button.pack()
        
        step1_label = tk.Label(queue_frame, text="1️⃣ Tekan untuk memasukkan URL ke antrian", 
                              font=('Arial', 8),
                              fg='#5F6368', bg='#FFFFFF')  # Google gray
        step1_label.pack(pady=(5, 0))

        # Download button with caption
        download_frame = tk.Frame(control_frame, bg='#FFFFFF')
        download_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.download_button = tk.Button(download_frame, text="⬇️ Mulai Download", 
                                       command=self.start_queue_processing,
                                       font=('Arial', 14, 'bold'),
                                       bg='#34A853', fg='white',  # Google green
                                       relief='flat', padx=30, pady=10,
                                       cursor='hand2')
        self.download_button.pack()
        
        step2_label = tk.Label(download_frame, text="2️⃣ Tekan untuk memulai download", 
                              font=('Arial', 8),
                              fg='#5F6368', bg='#FFFFFF')  # Google gray
        step2_label.pack(pady=(5, 0))

        # Cancel button with caption
        cancel_frame = tk.Frame(control_frame, bg='#FFFFFF')
        cancel_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.cancel_button = tk.Button(cancel_frame, text="❌ Batalkan", 
                                     command=self.cancel_download, 
                                     state='disabled',
                                     font=('Arial', 14, 'bold'),
                                     bg='#EA4335', fg='white',  # Google red
                                     relief='flat', padx=30, pady=10,
                                     cursor='hand2')
        self.cancel_button.pack()

        step3_label = tk.Label(cancel_frame, text="3️⃣ Tekan untuk membatalkan", 
                              font=('Arial', 8),
                              fg='#5F6368', bg='#FFFFFF')  # Google gray
        step3_label.pack(pady=(5, 0))

        # Status and progress section
        status_frame = tk.Frame(left_frame, bg='#FFFFFF')
        status_frame.pack(fill=tk.X, pady=(0, 15))

        self.status_label = tk.Label(status_frame, text="", 
                                    font=('Arial', 11, 'bold'),
                                    fg='#F9AB00', bg='#FFFFFF')  # Google yellow
        self.status_label.pack()

        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar", 
                       background='#34A853',  # Google green
                       troughcolor='#E8EAED',  # Light gray
                       borderwidth=0,
                       lightcolor='#34A853',
                       darkcolor='#34A853')

        self.progress = ttk.Progressbar(status_frame, orient="horizontal", 
                                       length=500, mode="determinate",
                                       style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=(10, 0))

        # Log section
        log_frame = tk.Frame(left_frame, bg='#FFFFFF')
        log_frame.pack(fill=tk.BOTH, expand=True)

        log_label = tk.Label(log_frame, text="📋 Log Aktivitas:", 
                            font=('Arial', 12, 'bold'),
                            fg='#5F6368', bg='#FFFFFF')  # Google gray
        log_label.pack(anchor="w")

        self.log_text = scrolledtext.ScrolledText(log_frame, width=70, height=12, 
                                                 state='disabled',
                                                 font=('Consolas', 9),
                                                 bg='#F8F9FA', fg='#202124',  # Light gray bg, dark text
                                                 relief='flat', bd=5)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Downloaded files section
        downloaded_label = tk.Label(right_frame, text="🎬 File yang Diunduh:", 
                                   font=('Arial', 14, 'bold'),
                                   fg='#202124', bg='#F8F9FA')  # Dark text on light bg
        downloaded_label.pack(anchor="w", padx=15, pady=(15, 10))

        # Downloaded files listbox frame
        downloaded_frame = tk.Frame(right_frame, bg='#F8F9FA')
        downloaded_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 5))

        self.downloaded_listbox = tk.Listbox(downloaded_frame, width=40, height=15,
                                           font=('Arial', 9),
                                           bg='#FFFFFF', fg='#202124',
                                           selectbackground='#E8F0FE',
                                           relief='flat', bd=5)
        self.downloaded_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        downloaded_scrollbar = tk.Scrollbar(downloaded_frame, orient="vertical",
                                          bg='#F8F9FA', troughcolor='#E8EAED')
        downloaded_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.downloaded_listbox.config(yscrollcommand=downloaded_scrollbar.set)
        downloaded_scrollbar.config(command=self.downloaded_listbox.yview)

        # Clear downloaded history button
        clear_downloaded_frame = tk.Frame(right_frame, bg='#F8F9FA')
        clear_downloaded_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.clear_downloaded_button = tk.Button(clear_downloaded_frame, text="🗑️ Hapus History", 
                                               command=self.clear_downloaded_history,
                                               font=('Arial', 9, 'bold'),
                                               bg='#EA4335', fg='white',  # Google red
                                               relief='flat', padx=15, pady=5,
                                               cursor='hand2')
        self.clear_downloaded_button.pack(side=tk.RIGHT)

        # Tombol baru: Open File Location
        self.open_location_button = tk.Button(clear_downloaded_frame, text="📂 Lokasi Tujuan", 
                                              command=self.open_output_dir,
                                              font=('Arial', 9, 'bold'),
                                              bg='#1A73E8', fg='white',  # Google blue
                                              relief='flat', padx=15, pady=5,
                                              cursor='hand2')
        self.open_location_button.pack(side=tk.RIGHT, padx=(0, 10))

        # Queue section
        queue_label = tk.Label(right_frame, text="⏳ Antrian Download:", 
                              font=('Arial', 14, 'bold'),
                              fg='#202124', bg='#F8F9FA')
        queue_label.pack(anchor="w", padx=15, pady=(20, 10))

        # Queue listbox frame
        queue_frame = tk.Frame(right_frame, bg='#F8F9FA')
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.queue_listbox = tk.Listbox(queue_frame, width=40, height=15,
                                       font=('Arial', 9),
                                       bg='#FFFFFF', fg='#F9AB00',  # White bg, Google yellow text
                                       selectbackground='#FEF7E0',  # Light yellow
                                       relief='flat', bd=5)
        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        queue_scrollbar = tk.Scrollbar(queue_frame, orient="vertical",
                                     bg='#F8F9FA', troughcolor='#E8EAED')
        queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.queue_listbox.config(yscrollcommand=queue_scrollbar.set)
        queue_scrollbar.config(command=self.queue_listbox.yview)

        # Initialize queue system
        self.download_queue = []
        self.is_downloading = False
        self.cancelled = False
        
        # Add hover effects and bindings
        self.add_hover_effects()
        
        # Add double-click binding for downloaded files
        self.downloaded_listbox.bind('<Double-Button-1>', self.open_file)
        
        # Check for IDM availability
        self.idm_path = self.get_idm_path()
        if self.idm_path:
            self.log("✅ IDM terdeteksi dan siap digunakan")
            self.log(f"📂 Path IDM: {self.idm_path}")
        else:
            self.log("⚠️ IDM tidak terdeteksi. Menggunakan download langsung")
            
    def get_idm_path(self):
        """Get IDM installation path"""
        possible_paths = [
            r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\IDMan.exe',
            r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\App Paths\IDMan.exe',
            r'SOFTWARE\Download Manager\Internet Download Manager',
            r'SOFTWARE\Wow6432Node\Download Manager\Internet Download Manager'
        ]
        
        # Try registry paths first
        for reg_path in possible_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    try:
                        idm_path = winreg.QueryValue(key, None)
                        if idm_path and os.path.exists(idm_path):
                            return idm_path
                    except:
                        # Try getting the "Path" value if direct query fails
                        try:
                            idm_path = winreg.QueryValueEx(key, "Path")[0]
                            if idm_path and os.path.exists(idm_path):
                                return idm_path
                        except:
                            continue
            except WindowsError:
                continue
        
        # Try common installation paths if registry search fails
        common_paths = [
            r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe",
            r"C:\Program Files\Internet Download Manager\IDMan.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
                
        return None

    def paste_url(self):
        """Paste clipboard content into URL entry"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_text)
        except:
            self.log("Tidak ada teks yang dapat ditempel")

    def open_file(self, event):
        """Open the selected file when double-clicked"""
        selection = self.downloaded_listbox.curselection()
        if selection:
            filename = self.downloaded_listbox.get(selection[0])
            filepath = os.path.join(self.output_dir, filename)
            if os.path.exists(filepath):
                os.startfile(filepath)
            else:
                messagebox.showwarning("File Tidak Ditemukan", 
                                     f"File tidak ditemukan:\n{filepath}")

    def add_hover_effects(self):
        def on_enter(event, button, color):
            button.configure(bg=color)
        
        def on_leave(event, button, original_color):
            button.configure(bg=original_color)

        # Queue button hover
        self.queue_button.bind("<Enter>", lambda e: on_enter(e, self.queue_button, '#1557B0'))
        self.queue_button.bind("<Leave>", lambda e: on_leave(e, self.queue_button, '#1A73E8'))

        # Download button hover
        self.download_button.bind("<Enter>", lambda e: on_enter(e, self.download_button, '#2D7D32'))
        self.download_button.bind("<Leave>", lambda e: on_leave(e, self.download_button, '#34A853'))

        # Cancel button hover
        self.cancel_button.bind("<Enter>", lambda e: on_enter(e, self.cancel_button, '#D33B2C'))
        self.cancel_button.bind("<Leave>", lambda e: on_leave(e, self.cancel_button, '#EA4335'))

        # Choose directory button hover
        self.choose_dir_button.bind("<Enter>", lambda e: on_enter(e, self.choose_dir_button, '#7627BB'))
        self.choose_dir_button.bind("<Leave>", lambda e: on_leave(e, self.choose_dir_button, '#8430CE'))

        # Clear downloaded button hover
        self.clear_downloaded_button.bind("<Enter>", lambda e: on_enter(e, self.clear_downloaded_button, '#D33B2C'))
        self.clear_downloaded_button.bind("<Leave>", lambda e: on_leave(e, self.clear_downloaded_button, '#EA4335'))

    def log(self, message):
        def append():
            self.log_text['state'] = 'normal'
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.log_text['state'] = 'disabled'
        self.root.after(0, append)

    def update_status(self, message):
        self.root.after(0, lambda: self.status_label.config(text=message))

    def update_progress(self, percent):
        self.root.after(0, lambda: self.progress.config(value=percent))

    def progress_hook(self, d):
        if self.cancelled:
            raise Exception("Unduhan dibatalkan oleh pengguna.")
        
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                percent = downloaded_bytes / total_bytes * 100
                self.update_progress(percent)
                self.log(f"Mengunduh: {percent:.2f}%")
            else:
                self.log(f"Mengunduh: {d.get('_percent_str', '')}")
        
        elif d['status'] == 'finished':
            self.update_progress(100)
            self.log("Unduhan selesai, sedang mengkonversi...")
            self.update_status("Memproses video...")

    def choose_directory(self):
        dir_path = filedialog.askdirectory(title="Pilih Folder Tujuan")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_display.config(text=self.output_dir)

    def get_video_info(self, url):
        """Get video information and direct download URL"""
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    # Playlist
                    entries = []
                    for entry in info['entries']:
                        if entry:
                            entries.append({
                                'title': entry.get('title', 'Unknown Title'),
                                'url': entry.get('url'),
                                'ext': entry.get('ext', 'mp4')
                            })
                    return entries
                else:
                    # Single video
                    return [{
                        'title': info.get('title', 'Unknown Title'),
                        'url': info.get('url'),
                        'ext': info.get('ext', 'mp4')
                    }]
        except Exception as e:
            self.log(f"Error getting video info: {str(e)}")
            return None

    def clean_filename(self, filename):
        """Clean filename from invalid characters"""
        # Replace invalid characters with underscore
        invalid_chars = r'[<>:"/\\|?*]'
        import re
        return re.sub(invalid_chars, '_', filename)

    def download_with_idm(self, video_info):
        """Download video using IDM"""
        try:
            title = self.clean_filename(video_info['title'])
            url = video_info['url']
            ext = video_info['ext']
            filename = f"{title}.{ext}"
            filepath = os.path.join(self.output_dir, filename)
            
            # Prepare IDM command
            idm_command = [
                self.idm_path,
                '/d', url,
                '/p', self.output_dir,
                '/f', filename,
                '/n',  # No confirmation dialog
                '/q'   # Add to queue
            ]
            
            # Execute IDM command
            subprocess.run(idm_command)
            self.log(f"Video ditambahkan ke antrian IDM: {title}")
            self.add_downloaded_file(filename)
            return True
            
        except Exception as e:
            self.log(f"Error starting IDM download: {str(e)}")
            return False

    def download_youtube_video_as_mp4(self, url):
        # Get selected download method
        method = self.download_method.get()
        
        # Determine which method to use
        use_idm = False
        if method == "auto":
            use_idm = self.idm_path is not None
            self.log(f"🔄 Mode Otomatis: {'Menggunakan IDM' if use_idm else 'Menggunakan yt-dlp'}")
        elif method == "idm":
            if self.idm_path:
                use_idm = True
                self.log("⚡ Mode IDM dipilih")
            else:
                self.log("❌ IDM tidak tersedia, beralih ke yt-dlp")
                messagebox.showwarning("IDM Tidak Tersedia", 
                                     "IDM tidak terdeteksi di sistem. Menggunakan download langsung.")
                use_idm = False
        elif method == "direct":
            use_idm = False
            self.log("📥 Mode Download Langsung dipilih")
        
        if use_idm:
            # Use IDM for download
            try:
                self.cancelled = False
                self.update_status("Mendapatkan informasi video...")
                video_info_list = self.get_video_info(url)
                
                if video_info_list:
                    for video_info in video_info_list:
                        if self.cancelled:
                            raise Exception("Unduhan dibatalkan oleh pengguna.")
                            
                        self.update_status(f"Menambahkan ke IDM: {video_info['title']}")
                        if self.download_with_idm(video_info):
                            self.log(f"✅ Berhasil menambahkan ke IDM: {video_info['title']}")
                        else:
                            self.log(f"❌ Gagal menambahkan ke IDM: {video_info['title']}")
                    
                    self.update_status("Video berhasil ditambahkan ke IDM!")
                    self.update_progress(100)
                else:
                    raise Exception("Gagal mendapatkan informasi video")
                    
            except Exception as e:
                if str(e) == "Unduhan dibatalkan oleh pengguna.":
                    self.update_status("Unduhan dibatalkan.")
                    self.log("Unduhan dibatalkan oleh pengguna.")
                else:
                    self.update_status("Terjadi kesalahan.")
                    self.log(f"Kesalahan: {str(e)}")
            finally:
                self.cancel_button.config(state='disabled')
                self.download_button.config(state='normal')
                self.clear_url_entry()
        else:
            # Use direct yt-dlp download
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'writethumbnail': False,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
                'restrictfilenames': True,  # Restrict filenames to ASCII characters
            }
            try:
                self.cancelled = False
                self.update_status("Memulai unduhan langsung...")
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                self.update_status("Unduhan selesai!")
                self.log("✅ Unduhan dan konversi berhasil diselesaikan.")
                
                # Add the downloaded file to the list
                if 'entries' in info_dict:
                    # Playlist
                    for entry in info_dict['entries']:
                        if entry:
                            title = entry.get('title', 'Judul Tidak Diketahui')
                            self.add_downloaded_file(f"{title}.mp4")
                else:
                    # Single video
                    title = info_dict.get('title', 'Judul Tidak Diketahui')
                    self.add_downloaded_file(f"{title}.mp4")
                
            except Exception as e:
                if str(e) == "Unduhan dibatalkan oleh pengguna.":
                    self.update_status("Unduhan dibatalkan.")
                    self.log("Unduhan dibatalkan oleh pengguna.")
                else:
                    self.update_status("Terjadi kesalahan.")
                    self.log(f"Kesalahan: {str(e)}")
            finally:
                self.cancel_button.config(state='disabled')
                self.download_button.config(state='normal')
                self.clear_url_entry()

    def add_to_queue(self, url):
        """Add URL to download queue"""
        self.download_queue.append(url)
        
        # Update queue display immediately
        def update_queue():
            self.queue_listbox.delete(0, tk.END)  # Clear current display
            for i, queued_url in enumerate(self.download_queue, 1):
                display_text = f"{i}. {queued_url}"
                self.queue_listbox.insert(tk.END, display_text)
            self.queue_listbox.see(tk.END)
            
        # Update display in main thread
        self.root.after(0, update_queue)
        self.log(f"URL ditambahkan ke antrian: {url}")
        
        # Start processing queue in a separate thread if not already downloading
        if not self.is_downloading:
            threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        """Process the download queue"""
        while True:
            if self.cancelled or not self.download_queue:
                self.is_downloading = False
                return
                
            if not self.is_downloading and self.download_queue:
                self.is_downloading = True
                url = self.download_queue[0]  # Get first URL but don't remove yet
                
                # Update UI in main thread
                self.root.after(0, lambda: self.prepare_download_ui())
                
                # Process download
                try:
                    self.download_youtube_video_as_mp4(url)
                except Exception as e:
                    self.log(f"Error downloading {url}: {str(e)}")
                finally:
                    # Remove processed URL and update queue in main thread
                    self.download_queue.pop(0)
                    self.root.after(0, lambda: self.update_queue_display())
                    self.is_downloading = False
            
            time.sleep(0.1)  # Small delay to prevent CPU overuse
            
    def prepare_download_ui(self):
        """Prepare UI for download"""
        self.progress['value'] = 0
        self.cancel_button.config(state='normal')
        self.download_button.config(state='disabled')

    def update_queue_display(self):
        """Update queue display with correct numbering"""
        def update_display():
            self.queue_listbox.delete(0, tk.END)
            for i, url in enumerate(self.download_queue, 1):
                display_text = f"{i}. {url}"
                self.queue_listbox.insert(tk.END, display_text)
        self.root.after(0, update_display)

    def download_with_queue(self, url):
        """Download with queue management"""
        try:
            self.download_youtube_video_as_mp4(url)
        finally:
            # Mark as not downloading and process next in queue
            self.is_downloading = False
            self.root.after(100, self.process_queue)  # Small delay before next download

    def clean_youtube_url(self, url):
        """Clean YouTube URL to remove playlist and other parameters"""
        import re
        
        # Extract video ID from various YouTube URL formats
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                clean_url = f"https://www.youtube.com/watch?v={video_id}"
                return clean_url
        
        # If no pattern matches, return original URL
        return url

    def add_to_queue_from_entry(self):
        """Add URL from entry to queue without starting download"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Kesalahan Input", "Silakan masukkan URL YouTube.")
            return
        
        # Clean the URL to remove playlist and other parameters
        original_url = url
        clean_url = self.clean_youtube_url(url)
        
        if original_url != clean_url:
            self.log(f"🧹 URL dibersihkan dari: {original_url}")
            self.log(f"🧹 Menjadi: {clean_url}")
            
        self.download_queue.append(clean_url)
        self.update_queue_display()
        self.log(f"URL ditambahkan ke antrian: {clean_url}")
        self.clear_url_entry()
        
    def start_queue_processing(self):
        """Start processing the download queue"""
        if not self.download_queue:
            messagebox.showwarning("Antrian Kosong", "Tidak ada URL dalam antrian download.")
            return
            
        if not self.is_downloading:
            threading.Thread(target=self.process_queue, daemon=True).start()

    def cancel_download(self):
        self.cancelled = True

    def clear_url_entry(self):
        self.url_entry.delete(0, tk.END)

    def add_downloaded_file(self, filename):
        def add_to_list():
            self.downloaded_listbox.insert(tk.END, filename)
            self.downloaded_listbox.see(tk.END)
        self.root.after(0, add_to_list)

    def clear_downloaded_history(self):
        """Clear the downloaded files history"""
        if self.downloaded_listbox.size() == 0:
            messagebox.showinfo("History Kosong", "Tidak ada history download untuk dihapus.")
            return
            
        result = messagebox.askyesno("Konfirmasi Hapus", 
                                   "Apakah Anda yakin ingin menghapus semua history download?\n\n"
                                   "Catatan: File yang sudah diunduh tidak akan terhapus, "
                                   "hanya history di aplikasi yang akan dibersihkan.")
        
        if result:
            self.downloaded_listbox.delete(0, tk.END)
            self.log("🗑️ History download berhasil dihapus")
            messagebox.showinfo("Berhasil", "History download telah dibersihkan.")

    def open_output_dir(self):
        """Membuka folder tujuan output di File Explorer"""
        if os.path.exists(self.output_dir):
            os.startfile(self.output_dir)
        else:
            messagebox.showwarning("Folder Tidak Ditemukan", f"Folder tidak ditemukan:\n{self.output_dir}")

def main():
    root = tk.Tk()
    app = DownloaderUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
