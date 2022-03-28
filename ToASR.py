import VoiceRecognition_function_goodjin5
from VoiceRecognition_function_goodjin5 import *
from tqdm import tqdm as tqdm
import soundfile,os
load_config()
'''
__./main.py__
# 导入必要库
import ToASR
from tqdm import tqdm

# 实例化asr,音频路径，识别引擎，最短片段长度，对于huggingface引擎的sota模型使用
asr = ToASR.ASR('./source/1.wav',engine='h',min_duration_on=1.5,usingBigHuggingFace=False)
sentences = []
# 迭代的，获取每句的识别结果
for sentence in tqdm(asr,total=len(asr.timeLine)):
    sentences.append(sentence)
# 映射
ToASR.subtitleGenerator('subtitle-test2.srt').addTimeLine(asr,sentences)
'''



class ASR():
    def __init__(self,errorString='@error'):
        '''
        :param path: 输入音频文件的路径
        :param min_duration_on: 音频片段的最小长度
        '''
        # 输入路径
        self.path = None
        # 于audio对应的时间轴列表
        self.timeLine = []
        # 于audio对应的音频帧列表
        self.actualChunk_timeline = []
        # 完整音频的wav浮点值列表
        self.fullAudio = []
        # 音频原始的sr
        self.audio_origin_sr = 0
        # 当遇到错误的
        self._errorString = errorString
        # 一些模型
        self._speechSplit_model = SpeeSplit_pipe()
        self._huggingface = None # AudioFlowLineHandling()
        self._vosk = None # VoskASR
        # 用于记录运行到哪里了
        self._progress_index = 0
        # 定义识别的函数
        self._recognition = None
        def set_recegnition_func():
            engine_index = VoiceRecognition_function_goodjin5.voice_model_engine
            # ['v', 'h_s', 'h_b', 's', 'v_hs', 'v_hb']
            if engine_index in [0,4,5]:
                self._vosk = VoskASR()
                self._recognition = self._vosk.read_audioDate # func-v
            if engine_index in [1,2,4,5]:
                self._huggingface = AudioFlowLineHandling()
                if self._vosk != None:
                    def func(audio):
                        v = self._vosk.read_audioDate(audio)
                        h = self._huggingface.VoiceRecognition(audio)
                        return {'Vosk':v,'HuggingFace':h}
                    self._recognition = func # func-v-h
                else:
                    self._recognition = self._huggingface.VoiceRecognition # func-h
            elif engine_index == 3:
                raise UserWarning('This engine is not supported at the moment')
            if engine_index in range(0,6) == False:
                # not in 0-5
                raise UserWarning('No additional engines supported__'+str(engine_index))
        set_recegnition_func()



    def sent_path(self,path):
        '''
        :param path: audio_path
        :return: null
        '''
        self.path = path
        if VoiceRecognition_function_goodjin5.debug: self.file_name = os.path.split(self.path)[1].split(".")[0]
        self.fullAudio,sr = read(path,sr=16000,mono=VoiceRecognition_function_goodjin5.mono)
        y,s = afc.resample(self.fullAudio,sr,VoiceRecognition_function_goodjin5.speech_split_sr)
        self.timeLine,self.actualChunk_timeline,y,self.audio_origin_sr = self._speechSplit_model.Calculation(y,s)
        pass



    def __iter__(self):
        return self
    def __next__(self):
        # 用于替代Get_all_asr
        if self._progress_index >= len(self.timeLine):
            # 下标越界
            self.path = None
            raise StopIteration
        return self._ToASR(self._progress_index)






    def _delFromIndex(self, index: int):
        '''
        :param self:
        :param index:
        :return:
        '''
        del self.timeLine[index], self.actualChunk_timeline[index]

    def _ToASR(self,index):
        '''
        :param index: 传入ASR的句子是chunk[index]对应的audio
        :return: string 从huggingface或vosk出来的
        :param actualChunk_timeline: 音频片段在fullAudio中的确切位置
        能够调用同一个方法得益于AutoSpeechRecognition的动态变化
        实现：通过chunk得到audio nparray
        '''
        chunk = self.actualChunk_timeline[index]
        audio_ = self.fullAudio[chunk[0]:chunk[-1]]
        if VoiceRecognition_function_goodjin5.debug:
            soundfile.write(file=self.file_name+'_'+str(index)+'.wav',data=audio_,samplerate=16000,format='wav')

        # 把audio【index】传到ASR
        self._progress_index += 1
        return self._recognition(audio_)










if __name__=='__main__':
    res = []
    asr = ASR()
    path = input('Please enter the path to the audio/video file')
    if path in ['','d','t','1']:
        path = r'D:\setup\wav\1.wav'
    asr.sent_path(path)
    for c in tqdm(asr,total=len(asr.timeLine)):
        res.append(c)
    for c in res:
        print(c)
    save_config()
    input('Identification is complete, config is saved, press enter to exit')

