from django.db import models
from utils.helpers import is_valid_url
import yt_dlp
from mutagen.id3 import ID3, TPE1, TALB, TYER, TIT2, TRCK
from django.http import FileResponse, JsonResponse
import tempfile
import os

# Create your models here.
class Video(models.Model):
    titulo = models.CharField(max_length=100)
    url = models.URLField()
    artista = models.CharField(max_length=100)
    canal = models.CharField(max_length=100)
    duracao_segundos = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.titulo
    
    @staticmethod
    def duracao(duracao_segundos):
        minutos = duracao_segundos // 60
        segundos = duracao_segundos % 60
        if segundos < 10:
            segundos = f"0{segundos}"
        return f"{minutos}:{segundos}"
    
    @staticmethod
    def download_preview(url_video):
        # Configuração para extrair apenas metadados
        ydl_opts = {
            'extract_flat': False,  # Extrai metadados completos
            'quiet': True,          # Evita logs desnecessários
            'extract_info': {
                'allowed_fields': [
                    'title',
                    'uploader',
                    'duration',
                    'webpage_url',
                ],
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrai metadados SEM download
            info = ydl.extract_info(url_video, download=False)
            
            # Exemplo: Extrai artista e título do título do vídeo (formato "ARTISTA - TÍTULO")
            if '-' in info['title']:
                artista, titulo = [parte.strip() for parte in info['title'].split('-', 1)]
            else:
                artista = info.get('uploader')
                titulo = info['title']
            
            video_info = {
                'titulo': titulo,
                'artista': artista,
                'duracao': Video.duracao(info.get('duration')),
                'url': info.get('webpage_url'),
            }
            return video_info
        
    
    @staticmethod    
    def download_url(url_video):
        accept = False
        if is_valid_url(url_video):
            result = Video.download_preview(url_video)
            accept = True
        return result, accept
    
    @staticmethod
    def download_media(url, title, bitrate):
        
        # Configurações do yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
            'postprocessor_args': [
                '-vn', '-ac', '2', '-ar', '44100', '-b:a', f'{bitrate}k'
            ],
            'addmetadata': True,
            'ignoreerrors': True,
            # Salva em um arquivo temporário
            'outtmpl': os.path.join(tempfile.gettempdir(), f'{title}.%(ext)s'),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                temp_file = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                
                Video.preencher_metadados(temp_file, info)
                
                # Envia o arquivo para o navegador
                file = open(temp_file, 'rb')
                response = FileResponse(file, as_attachment=True, filename=f'{title}.mp3')
                
                # Configura para deletar o arquivo após o envio
                response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
                
                # ...e cria uma thread para remover o arquivo depois de um tempo
                import threading, time

                def delayed_delete(path, delay=10):
                    time.sleep(delay)
                    try:
                        os.remove(path)
                    except Exception as e:
                        print(f'Erro ao remover arquivo temporário: {e}')

                threading.Thread(target=delayed_delete, args=(temp_file,)).start()
                
                return response
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        #return JsonResponse({'error': 'Erro ao baixar o vídeo'}, status=500)
    
    @staticmethod
    def preencher_metadados(caminho, info):
        #Preenche metadados do arquivo de áudio    
        audio = ID3(caminho)
        
        # Exemplo: Extrai artista e título do título do vídeo (formato "ARTISTA - TÍTULO")
        if '-' in info['title']:
            artista, titulo = [parte.strip() for parte in info['title'].split('-', 1)]
        else:
            artista = info.get('uploader')
            titulo = info['title']
        
        audio.update({
            'TPE1': TPE1(encoding=3, text=artista.strip()),  # ARTISTA
            'TIT2': TIT2(encoding=3, text=titulo.strip()),   # TÍTULO
            'TALB': TALB(encoding=3, text="Single"),         # ÁLBUM
            'TYER': TYER(encoding=3, text=info['upload_date'][:4]),  # ANO (extrai da data de upload)
            'TRCK': TRCK(encoding=3, text='1/1'),           # FAIXA Nº
        })
        
        audio.save()