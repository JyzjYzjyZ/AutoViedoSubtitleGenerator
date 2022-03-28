import numpy as np
from pyannote.audio.pipelines import VoiceActivityDetection
from pyannote.audio import Model
import torch

import VoiceRecognition_function_goodjin5
import VoiceRecognition_function_goodjin5.AudioFormatConversion_goodjin5 as afc
# pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
# https://pypi.tuna.tsinghua.edu.cn/simple 在这里安装pytorch
# pip install D:\setup\pyannote-audio-develop.zip -i https://pypi.tuna.tsinghua.edu.cn/simple




class SpeeSplit_pipe():
  def __init__(self):
    self.min_duration_on = VoiceRecognition_function_goodjin5.min_during_on
    self._progress_hook = VoiceRecognition_function_goodjin5.progressBar_speechSplit
    self._ModelPath= VoiceRecognition_function_goodjin5.path_model_SpeechSplit
    self._device = VoiceRecognition_function_goodjin5.device
    _model = Model.from_pretrained(self._ModelPath)
    _model.to(torch.device(self._device))
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
    afc.resample(sound=y,orig_sr=s,target_sr=VoiceRecognition_function_goodjin5.speech_split_sr)
    wav = afc.toTorch(y)
    pipe_result = self.pipe({"waveform": wav, "sample_rate": s})
    pipe_result = str(pipe_result).split(' 0 SPEECH\n')
    pipe_result[len(pipe_result) - 1] = pipe_result[len(pipe_result) - 1].replace(' 0 SPEECH', '')
    chunk = self._getChunk(pipe_result,y,s)
    if len(pipe_result) != len(chunk):raise IndexError(r'The number of chunks and pipes do not match, you can report this bug on github')
    return pipe_result,chunk,y,s






if __name__=='__main__':
   pipe = SpeeSplit_pipe()
   path = '../source/1.wav'
   # waveIndex = 1
   y,s = afc.read(path,sr=16000)
   p,c,y,s = pipe.Calculation(y,s)
   print(p)

