from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import librosa
import numpy as np
def read_img_lazy(paths:list[str]):
    for path in paths:
        yield Image.open(path)

def read_img_faster(paths:list[str]):
    with ThreadPoolExecutor() as exec:
        futures=list(exec.map(Image.open,paths))
        return futures

def img2amp_lazy(images):
    for img in images:
        db_ud = np.uint8(np.array(img))
        amp = librosa.db_to_amplitude(db_ud)
        yield amp

def amp2wave_lazy(amplitudes):
    for amp in amplitudes:
        yield librosa.griffinlim(amp)

def wave2wav_file(waves:list[np.ndarray],file_names:list[str],save_path='./data/audio/',sampling_rate=44100):
    for wave,name in zip(waves,file_names):
        librosa.output.write_wav(save_path+name+".wav", wave.astype(np.int16), sampling_rate)

def img2wav_file(paths:list[str],save_path='./data/audio/',file_names:list[str]|None=None,sampling_rate=44100):
    g=read_img_lazy(paths)
    g=img2amp_lazy(g)
    g=amp2wave_lazy(g)
    if file_names is None:
        file_names=[x.split('/')[-1].split('.')[0] for x in paths]
    wave2wav_file(g,file_names,save_path,sampling_rate)

def img2wav_file_faster(paths:list[str],save_path='./data/audio/',file_names:list[str]|None=None,sampling_rate=44100):
    g=read_img_faster(paths)
    g=img2amp_lazy(g)
    g=amp2wave_lazy(g)
    if file_names is None:
        file_names=[x.split('/')[-1].split('.')[0] for x in paths]
    wave2wav_file(g,file_names,save_path,sampling_rate)