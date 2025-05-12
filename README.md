# 🎵 DYT (Download Your Tune) — Django App para Baixar Áudios de Vídeos

Este é um projeto Django que permite aos usuários baixarem o áudio de vídeos (ex: YouTube), escolhendo a qualidade (bitrate) desejada. O áudio é convertido para `.mp3` e pode ser salvo localmente no navegador (com suporte moderno).

---

## 🧩 Funcionalidades

- 🔍 Pré-visualização de título, artista e duração do vídeo.
- 🎼 Download do áudio em `.mp3`, com bitrate selecionável (128, 192, 256 ou 320 kbps).
- 🧠 Extração de metadados automáticos via backend.
- 📂 Salvamento local do arquivo usando a API `File System Access`.

---

## 📦 Tecnologias Utilizadas

- Django 5.2
- yt-dlp (para download e conversão dos vídeos)
- HTML + JavaScript (com uso de File System Access API)
- SQLite (em desenvolvimento)

---

## 🚀 Como Executar Localmente

1. **Clone o repositório:**

```bash
git clone https://github.com/josuelfeitosa/DYT.git
cd DYT
```
2. **Crie e ative o ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```
3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```
4. **Realize as migrações e inicie o servidor:**

```bash
python manage.py migrate
python manage.py runserver
```
5. **Acesse no navegador:**

```bash
http://127.0.0.1:8000
```