import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os

# Logger para capturar o "Pular" do histórico
class MyLogger:
    def __init__(self, status_callback):
        self.status_callback = status_callback

    def debug(self, msg):
        # Detecta mensagens de arquivo já existente ou registrado no histórico
        if "download_archive" in msg or "already been recorded" in msg:
            self.status_callback("Arquivo já consta no Histórico. Pulando...")
        elif "has already been downloaded" in msg:
            self.status_callback("Arquivo já existe. Pulando...")

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(f"Erro YT-DLP: {msg}")

class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Downloader Pro - V4 (Inteligente)")
        self.root.geometry("600x480")
        self.root.resizable(False, False)

        # Variáveis
        self.download_path = tk.StringVar()
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp3")
        self.status_var = tk.StringVar(value="Pronto para baixar")
        self.progress_var = tk.DoubleVar()
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        lbl_title = ttk.Label(main_frame, text="Youtube Downloader", font=("Segoe UI", 16, "bold"))
        lbl_title.pack(pady=(0, 20))

        # URL
        lbl_url = ttk.Label(main_frame, text="Link (Vídeo, Playlist ou Youtube Music):")
        lbl_url.pack(anchor=tk.W)
        entry_url = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        entry_url.pack(fill=tk.X, pady=(5, 15))

        # Pasta
        lbl_path = ttk.Label(main_frame, text="Salvar em:")
        lbl_path.pack(anchor=tk.W)
        frame_path = ttk.Frame(main_frame)
        frame_path.pack(fill=tk.X, pady=(5, 15))
        entry_path = ttk.Entry(frame_path, textvariable=self.download_path)
        entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True)
        btn_browse = ttk.Button(frame_path, text="📂 Escolher Pasta", command=self.browse_folder)
        btn_browse.pack(side=tk.RIGHT, padx=(10, 0))

        # Formato
        frame_format = ttk.LabelFrame(main_frame, text="Formato", padding="10")
        frame_format.pack(fill=tk.X, pady=(0, 20))
        ttk.Radiobutton(frame_format, text="🎵 Áudio (MP3)", variable=self.format_var, value="mp3").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(frame_format, text="🎬 Vídeo (MP4)", variable=self.format_var, value="mp4").pack(side=tk.LEFT, padx=20)

        # Botão
        self.btn_download = ttk.Button(main_frame, text="BAIXAR AGORA", command=self.start_download_thread)
        self.btn_download.pack(fill=tk.X, pady=(0, 15))

        # Barra e Status
        self.progress_bar = ttk.Progressbar(main_frame, style="green.Horizontal.TProgressbar", orient="horizontal", length=100, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        self.lbl_status = ttk.Label(main_frame, textvariable=self.status_var, foreground="#555")
        self.lbl_status.pack(pady=0)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder: self.download_path.set(folder)

    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()

    def start_download_thread(self):
        url = self.url_var.get()
        path = self.download_path.get()

        if not url: return messagebox.showwarning("Atenção", "Cole um link primeiro!")
        if not path: return messagebox.showwarning("Atenção", "Escolha onde salvar!")

        self.btn_download.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Verificando...")
        
        threading.Thread(target=self.run_download, args=(url, path)).start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                self.progress_var.set(float(p))
                filename = os.path.basename(d.get('filename', 'arquivo'))
                if len(filename) > 30: filename = filename[:27] + "..."
                self.status_var.set(f"Baixando: {d.get('_percent_str')} - {filename}")
            except: pass
            self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_var.set("Finalizando conversão...")

    def run_download(self, url, path):
        fmt = self.format_var.get()
        logger = MyLogger(self.update_status)

        # Configurações Avançadas
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True,
            'logger': logger,
            # CRUCIAL: Cria um arquivo .txt na pasta que memoriza o que já baixou
            'download_archive': os.path.join(path, 'historico_downloads.txt'),
            'continuedl': True,
        }

        if fmt == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.status_var.set("Tudo pronto! Lista finalizada.")
            messagebox.showinfo("Sucesso", "Todos os downloads foram concluídos!")
        except Exception as e:
            self.status_var.set("Erro no processo.")
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")
        finally:
            self.progress_var.set(0)
            self.btn_download.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()