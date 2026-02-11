import yt_dlp

def baixar_musica_ou_playlist(url):
    # Configurações do download
    ydl_opts = {
        # 1. Formato: Baixa o melhor áudio disponível
        'format': 'bestaudio/best',
        
        # 2. Nome do arquivo final (Título da música.extensão)
        'outtmpl': '%(title)s.%(ext)s',
        
        # 3. Pós-processadores (executados após o download do arquivo bruto)
        'postprocessors': [
            {
                # Converte o áudio baixado para MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                # Adiciona a thumbnail como capa do arquivo MP3
                'key': 'EmbedThumbnail',
            },
            {
                # Adiciona metadados (artista, álbum, etc.)
                'key': 'FFmpegMetadata',
            }
        ],
        
        # 4. Comandos auxiliares para a capa e playlists
        'writethumbnail': True,  # Baixa a imagem da capa para disco (necessário para o Embed)
        'noplaylist': False,     # Se a URL for uma playlist, baixa TUDO. (Use True para baixar só 1)
    }

    # Inicia o processo de download
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Iniciando download de: {url}")
            ydl.download([url])
            print("Download concluído com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso:
# Pode ser um link de vídeo único OU um link de playlist
url_para_baixar = input("INSIRA_SEU_LINK_AQUI") 
baixar_musica_ou_playlist(url_para_baixar)