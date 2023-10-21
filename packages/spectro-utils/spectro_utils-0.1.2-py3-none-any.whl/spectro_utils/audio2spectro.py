from enum import Enum
import librosa
import numpy as np
from tqdm import tqdm
from PIL import Image
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time
class ImageFormat(Enum):
    png='png'
    bmp='bmp'

def read_audio_faster(paths:list[str],sampling_rate=44100,mono=True):
    with ThreadPoolExecutor() as exec:
        futures=list(exec.map(lambda x:librosa.core.load(x, sr=sampling_rate, mono=mono)[0],paths))
        return futures

def read_audio_lazy(paths:list[str],sampling_rate=44100,mono=True):
    for path in paths:
        y, sr = librosa.core.load(path, sr=sampling_rate, mono=mono)
        yield y
def wave2spectro_lazy(wavs):
    for y in wavs:
        yield librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

def spectro2img(spectros,image_names,save_path='./data/image/',image_format=ImageFormat.png):
    for spectro,name in tqdm(zip(spectros, image_names), total=len(image_names)):
        Image.fromarray(np.uint8(spectro), mode='L').save(save_path+name+'.'+image_format.value,format=image_format.value)

def audio2spectro_img(paths:list[str],save_path='./data/image/',image_names:list[str]|None=None,sampling_rate=44100,mono=True,image_format=ImageFormat.png):
    g=read_audio_lazy(paths,sampling_rate,mono)
    g=wave2spectro_lazy(g)
    if image_names is None:
        image_names=[x.split('/')[-1].split('.')[0] for x in paths]
    spectro2img(g,image_names,save_path,image_format)

def audio2spectro_img_faster(paths:list[str],save_path='./data/image/',image_names:list[str]|None=None,sampling_rate=44100,mono=True,image_format=ImageFormat.png):
    g=read_audio_faster(paths,sampling_rate,mono)
    g=wave2spectro_lazy(g)
    if image_names is None:
        image_names=[x.split('/')[-1].split('.')[0] for x in paths]
    spectro2img(g,image_names,save_path,image_format)




# def wav2spectro_faster(wavs):
#     with ProcessPoolExecutor() as exec:
#         stft=lambda x:librosa.stft(x)
#         a2s=lambda x:librosa.amplitude_to_db(x, ref=np.max)
#         futures=list(map(stft,wavs))
#         futures=[np.abs(x) for x in futures]
#         futures=list(exec.map(a2s,wavs))
#         return futures
# def spectro2img_faster(spectros,image_names,save_path='./data/image/',image_format=ImageFormat.png):
    
#     with ProcessPoolExecutor() as exec:
#         save_img = lambda spectro,image_name:Image.fromarray(np.uint8(spectro), mode='L').save(save_path+image_name+'.'+image_format,format=image_format)
#         futures=[exec.submit(save_img,spectro,image_name) for spectro,image_name in zip(spectros,image_names)]
#         # for f in futures:
#         #     f.result()
#         #list(tqdm(exec.map(save_img,zip(spectros,image_names)),total=len(image_names)))