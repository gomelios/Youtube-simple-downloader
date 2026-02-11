import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os

class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Downloader Pro")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Variáveis
        self.download_path = tk.StringVar()
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp3")
        self.status_var = tk.StringVar(value="Pronto para baixar")
        self.progress_var = tk.DoubleVar() # Variável para a barra de progresso
        
        # Configuração de Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')

        self.create_widgets()

    def create_widgets(self):
        # Frame Principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Título ---
        lbl_title = ttk.Label(main_frame, text="Youtube Downloader", font=("Segoe UI", 16, "bold"))
        lbl_title.pack(pady=(0, 20))

        # --- Entrada de URL ---
        lbl_url = ttk.Label(main_frame, text="Link (Vídeo, Playlist ou Youtube Music):")
        lbl_url.pack(anchor=tk.W)
        
        entry_url = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        entry_url.pack(fill=tk.X, pady=(5, 15))

        # --- Seleção de Pasta ---
        lbl_path = ttk.Label(main_frame, text="Salvar em:")
        lbl_path.pack(anchor=tk.W)

        frame_path = ttk.Frame(main_frame)
        frame_path.pack(fill=tk.X, pady=(5, 15))

        # CORREÇÃO AQUI: Removido o 'readonlybackground="white"'
        entry_path = ttk.Entry(frame_path, textvariable=self.download_path)
        entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_browse = ttk.Button(frame_path, text="📂 Escolher Pasta", command=self.browse_folder)
        btn_browse.pack(side=tk.RIGHT, padx=(10, 0))

        # --- Opções de Formato ---
        frame_format = ttk.LabelFrame(main_frame, text="Formato", padding="10")
        frame_format.pack(fill=tk.X, pady=(0, 20))

        rb_mp3 = ttk.Radiobutton(frame_format, text="🎵 Áudio (MP3)", variable=self.format_var, value="mp3")
        rb_mp3.pack(side=tk.LEFT, padx=20)

        rb_mp4 = ttk.Radiobutton(frame_format, text="🎬 Vídeo (MP4)", variable=self.format_var, value="mp4")
        rb_mp4.pack(side=tk.LEFT, padx=20)

        # --- Botão de Download ---
        self.btn_download = ttk.Button(main_frame, text="BAIXAR AGORA", command=self.start_download_thread)
        self.btn_download.pack(fill=tk.X, pady=(0, 15))

        # --- Barra de Progresso ---
        self.progress_bar = ttk.Progressbar(main_frame, style="green.Horizontal.TProgressbar", orient="horizontal", length=100, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        # --- Texto de Status ---
        self.lbl_status = ttk.Label(main_frame, textvariable=self.status_var, foreground="#555")
        self.lbl_status.pack(pady=0)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.set(folder_selected)

    def start_download_thread(self):
        url = self.url_var.get()
        path = self.download_path.get()

        if not url:
            messagebox.showwarning("Atenção", "Cole um link primeiro!")
            return
        if not path:
            messagebox.showwarning("Atenção", "Escolha onde salvar o arquivo!")
            return

        self.btn_download.config(state=tk.DISABLED)
        self.progress_var.set(0) # Reseta a barra
        self.status_var.set("Iniciando...")
        
        thread = threading.Thread(target=self.run_download, args=(url, path))
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                self.progress_var.set(float(p))
                self.status_var.set(f"Baixando: {d.get('_percent_str')}")
            except:
                self.status_var.set("Baixando...")
            
            self.root.update_idletasks()

        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_var.set("Download finalizado. Convertendo arquivo...")

    def run_download(self, url, path):
        fmt = self.format_var.get()
        
        # Opções básicas
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True,
        }

        # Configurações específicas MP3 vs MP4
        if fmt == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else: # mp4
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best', # Baixa vídeo e áudio separados
                'merge_output_format': 'mp4',         # Junta no final
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.status_var.set("Sucesso! Tudo pronto.")
            messagebox.showinfo("Concluído", "Download finalizado com sucesso!")
            self.progress_var.set(0)
            self.status_var.set("Pronto para o próximo")
        
        except Exception as e:
            self.status_var.set("Erro.")
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro:\n{str(e)}\n\nVerifique se o FFmpeg está instalado.")
        
        finally:
            self.btn_download.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()