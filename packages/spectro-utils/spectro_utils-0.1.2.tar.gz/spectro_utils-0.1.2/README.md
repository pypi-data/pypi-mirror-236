# spectro-utils
Conversion from wav file to spectro image and from spectro image to wav file

## install
```
pip install spectro-utils
```

## how to use

### get started
#### wav file to spectro image
```python
import spectro_utils.audio2spectro as a2s
a2s.audio2spectro_img(audio_paths)
```

#### spectro image to wav file
```python
import spectro_utils.spectro2audio as s2a
s2a.img2wav_file(image_paths)
```

### more details of audio2spectro

#### read_audio_lazy
Reads a wav file using delayed evaluation.
It saves memory compared to normal loading.
```python
audios=a2s.read_audio_lazy(paths)
```

#### wave2spectro_lazy
Converts the waves to an spectrum using delayed evaluation.
```python
spectros=a2s.wave2spectro_lazy(audios)
```

#### spectro2img
Save the spectro images as a image files(png or bmp).
```
a2s.spectro2img(spectros,image_names)
```

#### example of custom pipeline
```python
def split_four_audio_lazy(audios):
    for audio in audios:
        n=len(audio)/4
        for i in range(4):
            start=n*i
            yield audio[start:start+n]

def custom_pipeline(paths:list[str],image_names:list[str])->None:
    g=a2s.read_audio_lazy(paths)
    g=split_four_audio_lazy(g)
    g=a2s.wave2spectro_lazy(g)
    a2s.spectro2img(g,image_names)
```

### more details of spectro2audio

#### read_img_lazy
Reads a image file using delayed evaluation.
It saves memory compared to normal loading.
```python
images=s2a.read_img_lazy(paths)
```

#### img2amp_lazy
Converts the image to an power spectrum using delayed evaluation.
```python
amplitudes=s2a.img2amp_lazy(images)
```

#### amp2wave_lazy
Converts power spectrum to sound waves using delay evaluation.
```python
waves=s2a.amp2wave_lazy(amplitudes)
```

#### wave2wav_file
Save the sound wave as a wav file.
```python
s2a.wave2wav_file(waves,file_names)
```

#### example of custom pipeline
```python
def volume_up_lazy(amplitudes):
    for amp in amplitudes:
        yield amp*2000

def custom_pipeline(paths)->None:
    g=s2a.read_img_lazy(paths)
    g=s2a.img2amp_lazy(g)
    g=volume_up_lazy(g)
    g=s2a.amp2wave_lazy(g)
    return g

g=custom_pipeline(['./data/image/1.png'])
display(IPython.display.Audio(g.__next__(), rate=44100))
```