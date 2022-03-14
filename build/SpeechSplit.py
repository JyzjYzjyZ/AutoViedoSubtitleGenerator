from pyannote.audio.pipelines import VoiceActivityDetection
from pyannote.audio import Model
import librosa
# pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
# https://pypi.tuna.tsinghua.edu.cn/simple 在这里安装pytorch

# pip install D:\setup\pyannote-audio-develop.zip -i https://pypi.tuna.tsinghua.edu.cn/simple

def main(SourceRelativePath, ModelRelativePath='./models/pyannote-segmentation/pytorch_model.bin', onset=0.5, offset=0.5, min_duration_on=0.0, min_duration_off=0.0, sr = 16000,mono=True):
  # ModelRelativePath = './pyannote-segmentation/pytorch_model.bin'
  # SourceRelativePath "./1.wav"
  model = Model.from_pretrained(ModelRelativePath)
  pipeline = VoiceActivityDetection(model)
  HYPER_PARAMETERS = {
    # onset/offset activation thresholds
    "onset": onset, "offset": offset,
    # remove speech regions shorter than that many seconds.
    "min_duration_on": min_duration_on,
    # fill non-speech regions shorter than that many seconds.
    "min_duration_off": min_duration_off
  }

  pipeline.instantiate(HYPER_PARAMETERS)
  res = pipeline(SourceRelativePath)
  # `vad` is a pyannote.core.Annotation instance containing speech regions
  # string==>array
  clipArr = str(res).split(' 0 SPEECH\n')
  clipArr[len(clipArr)-1] = clipArr[len(clipArr)-1].replace(' 0 SPEECH','')
  actualChunk = ClipAudio(SourceRelativePath, clipArr, sr, mono)
  # print('ResAudioArr\n\n',ResAudioArr, '\n' ,' clipArr\n\n',  clipArr)
  FinResDict = {'ClipArr':clipArr,'ActualChunk':actualChunk}
  return FinResDict




def ClipAudio(SourceRelativePath, clipArr, sr=16000,mono:bool=True):
  # clipArr[0]  [ 00:01:07.845 -->  00:01:12.030]
  def TimeTransForm(time):
    secondArr = time.split(':')
    sceondRes = float(secondArr[0])*3600+ float(secondArr[1])*60+float(secondArr[2])
    return sceondRes
  #====================检测时长========================
  audio, sr = librosa.load(SourceRelativePath, sr=sr, mono=mono)
  dur = librosa.get_duration(y=audio,sr=sr)
  print('duration:'+str(dur))
  if dur> 359998.9:
      raise Exception(print('Your video length exceeds the limit of 100 hours or less'))# 99:59:59
  #============================================
  audioClipArrRes = []
  actualChunk = []
  index = 0
  for clip in clipArr:
    timeClipArr = (str(clip).replace(' ', ''))[1:-1].split('-->')
    start = TimeTransForm(timeClipArr[0])
    stop = TimeTransForm(timeClipArr[1])
    audio_part = audio[int(start*sr):int(stop*sr)+1]
    actualChunk_part =  [int(start * sr),int(stop * sr) + 1]
    audioClipArrRes.append(audio_part)
    actualChunk.append(actualChunk_part)
    #=================保存=======================
    # SaveAudio(audio_part,index)
    #=======================================
    index += 1
  pass
  print('sr:'+str(sr))
  return actualChunk



def SaveAudio(audio,i):
  try:
    import soundfile
    soundfile.write('./source/test1/2_' + str(i) + '.wav', samplerate=16000, data=audio, format='wav')
  except:
    pass


if __name__ == '__main__':
    # from transformers.dependency_versions_check import pkgs_to_check_at_runtime
    # print(pkgs_to_check_at_runtime)
    # ['python', 'tqdm', 'regex', 'sacremoses', 'requests', 'packaging', 'filelock', 'numpy', 'tokenizers']
    print("这是一个speechsplit的测试")
    # print('tornado',' The WebAgg backend requires Tornado','D:\project\test\speechsplite\dist\SpeechSplit\SpeechSplit.exe','pip install --upgrade torch==1.9.0  pip install --upgrade torchvision==0.10.0')
    print('==========================================')
    path = input('请输入音频文件的绝对路径，例如D:\\setup\\models\\pyannote-segmentation\\pytorch.wav')
    res = main(path,'D:\\setup\\models\\pyannote-segmentation/pytorch_model.bin')
    print(res)
