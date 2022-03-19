import numpy as np
from pyannote.audio.pipelines import VoiceActivityDetection
from pyannote.audio import Model
import librosa,torch,time
import AudioTransformer as at
# pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
# https://pypi.tuna.tsinghua.edu.cn/simple 在这里安装pytorch
# pip install D:\setup\pyannote-audio-develop.zip -i https://pypi.tuna.tsinghua.edu.cn/simple
'''
没力气卷了 -3.18

足够用的，误差小的，比我自己累死写的好的
-v:1.0.3
author:goodjin5
date 22.3.19
'''



class SpeeSplit_pipe():
  def __init__(self,min_duration_on=1.25,model_RAM=None,device=None):
    self.min_duration_on = min_duration_on
    self._progress_hook = True
    self._ModelPath= r'D:\setup\models\pyannote-segmentation\pytorch_model.bin'
    self._device = device if device != None else ('cuda:0' if torch.cuda.is_available() else 'cpu')
    _model = (Model.from_pretrained(self._ModelPath) if model_RAM==None else model_RAM)
    _model.to(torch.device(self._device))
    if __name__=='__main__':print(_model.device.type)
    self.model = _model
    self.pipe = VoiceActivityDetection(self.model,device=self._device)
    self._option_pipe={
    # onset/offset activation thresholds
    "onset": 0.5, "offset": 0.5,
    # remove speech regions shorter than that many seconds.
    "min_duration_on": self.min_duration_on,
    # fill non-speech regions shorter than that many seconds.
    "min_duration_off": 0.0,
    }
    self.pipe.instantiate(self._option_pipe)


  def _getChunk(self,pip_result,y,s):
    def _TimeTransForm(time):
      secondArr = time.split(':')
      sceondRes = float(secondArr[0]) * 3600 + float(secondArr[1]) * 60 + float(secondArr[2])
      return sceondRes

    y_len = len(y)
    if y_len > 359998.9*s:raise Exception(print('Your video length exceeds the limit of 100 hours or less'))# 99:59:59

    chunk = []
    index = 0

    for c in pip_result:
      time_two = (str(c).replace(' ', ''))[1:-1].split('-->')
      start = _TimeTransForm(time_two[0])
      stop = _TimeTransForm(time_two[-1])
      start_chunk = int(start * s)
      stop_chunk = int(stop * s) + 1
      chunk_part = [start_chunk if start_chunk>=0 else 0,
                    stop_chunk if stop_chunk<=y_len else y_len]
      chunk.append(chunk_part)
      index += 1
    return chunk



  def Calculation(self,y:np.array,s:int):
    wav = at.toTorch(y)
    pipe_result = self.pipe({"waveform": wav, "sample_rate": s})
    pipe_result = str(pipe_result).split(' 0 SPEECH\n')
    pipe_result[len(pipe_result) - 1] = pipe_result[len(pipe_result) - 1].replace(' 0 SPEECH', '')
    chunk = self._getChunk(pipe_result,y,s)
    if len(pipe_result) != len(chunk):raise IndexError(r'The number of chunks and pipes do not match, you can report this bug on github')
    return pipe_result,chunk,y,s






if __name__=='__main__':
   start = time.time()
   pipe = SpeeSplit_pipe()
   model = pipe.model
   waveIndex = input(r'输入音频长度自动在D:\setup\wav\中搜索 或输入0以自定义路径')
   path = r'D:\setup\wav\{0}.wav'.format(int(waveIndex))
   if waveIndex=='0':path = input(r'输入自定义的路径')
   # waveIndex = 1
   y,s = at.read(path,sr=0)
   p,c,y,s = pipe.Calculation(y,s)
   print(p,c)
   print(time.time()-start)

