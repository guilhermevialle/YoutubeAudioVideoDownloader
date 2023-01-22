import os
from pytube import YouTube
from tqdm import tqdm
import requests
import subprocess

title = None


def download_youtube_video(url):
    yt = YouTube(url)
    streams = yt.streams.filter(mime_type='video/mp4').all()
    for i, stream in enumerate(streams):
        print(f"{i}. {stream.resolution} ({stream.filesize/(1024*1024):.2f}MB)")
    choice = int(input("Escolha a qualidade do video: "))
    stream = streams[choice]
    global title
    title = yt.title
    file_size = stream.filesize
    pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc=title)
    response = requests.get(stream.url, stream=True)
    with open(f"{title}.mp4", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    pbar.close()
    os.rename(f"{title}.mp4",
              f"{os.path.expanduser('~/Downloads')}/{title}.mp4")
    print(f"Video {title} foi baixado com sucesso!")


url = input("Cole a URL do video: ")
print('Esse processo pode levar alguns minutos. Aguarde...')
download_youtube_video(url)


video_path = f"{os.path.expanduser('~/Downloads')}/{title}.mp4"


def convert_video_to_mp3(input_file):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = "/Users/guilhermevialle/Downloads/{}.mp3".format(file_name)
    command = ['ffmpeg', '-i', input_file, '-vn',
               '-c:a', 'libmp3lame', '-q:a', '0', output_file]
    subprocess.call(command)


convert_video_to_mp3(video_path)


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Arquivo {file_path} removido.")
    else:
        print(f"Arquivo {file_path} não existe.")


delete_file(video_path)
print('Musica baixada com sucesso. ' + os.path.expanduser('~/Downloads'))
