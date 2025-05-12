from django.shortcuts import render, redirect
from django.http import JsonResponse
import json


from core.models import Video

# Create your views here.

def index(request):
    return render(request, 'index.html')

def submit_preview(request):
    if request.method == 'POST':
        video_info, accept = Video.download_url(request.POST.get('url_video'))
        #print(f"Aqui: {video_info}")
        dados = {}
        if accept:
            dados = {'videos': [video_info]}  # Transforma em uma lista com um único item
            for chave, valor in dados.items():
                print(f"{chave}: {valor[0]['url']}")
        return render(request, 'download.html', dados)
    return redirect('')

def submit_download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("[DEBUG] Dados recebidos:", data)
        url = data.get('video_url')
        title = data.get('title');  # Nome padrão se não fornecido
        bitrate = data.get('bitrate')
        result = Video.download_media(url, title, bitrate)
        
        return result
        
    return JsonResponse({'error': 'Método não permitido'}, status=405)
    