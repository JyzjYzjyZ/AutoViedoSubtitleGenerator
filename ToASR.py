import time
import warnings


class printColor():
    def __init__(self,data):
        self.data = data
        pass
    def green(self):
        print('\033[0;32m'+str(self.data)+'\033[0m')
    def blue(self):
        print('\033[0;34m'+str(self.data)+'\033[0m')
    def violetRed(self):
        print('\033[0;35m'+str(self.data)+'\033[0m')
    def yellow(self):
        print('\033[0;33m'+str(self.data)+'\033[0m')
    def red(self):
        print('\033[0;31m'+str(self.data)+'\033[0m')
    def d(self):
        print(str(self.data))



class ASR():
    def __init__(self,path,min_duration_on:float = 1.25,engine:str = 'h'):
        '''
        :param path: 输入音频文件的路径
        :param min_duration_on: 音频片段的最小长度
        '''
        # 输入路径
        self.path = path
        # 使用debug调试
        self.debug = True
        # 不计算双句
        self.quick = False
        #采样率16kHz
        self.sr = 16000
        #启用但声轨
        self.mono = True
        # 于audio对应的时间轴列表
        self.timeLine = []
        # 于audio对应的音频帧列表
        self.actualChunk_timeline = []
        # 完整音频的wav浮点值列表
        self.fullAudio = []
        # 使用Vosk或HuggingFace
        self.ASR_engine = engine
        # 一个通用的语音识别方法
        self.ToASR = self.ToASR
        # 用作句子分割的
        # 按照2/3s一个单词的时间计算，最短句，3个单词需要2s。所以1.25s是一个比较合适的值
        self.min_duration_on = min_duration_on
        # ---------------------------------------------
        def _AutoSpechRecognition(data):
            '''
            :param data: wav 01-array
            :return: string
            '''
            usedToCalculateTheFunctionStartTime = time.time()
            if self.ASR_engine=='h':
                res = self.AFLH.VoiceRecognition(data)
            elif self.ASR_engine=='v':
                # vosk 中的方法完成了 librosa 转 wave
                res = self.Vo.read_audioDate_librosa(data)
            elif self.ASR_engine=='s':
                res = self.Sph.STT(audio=data)
                pass
            printColor('time_voiceRecognition:' + str(time.time() - usedToCalculateTheFunctionStartTime)).violetRed()
            return res




        def _SpeechSplit(path):
            '''
            :param path: ./2.wav
            :return: timeline audio[list] chunk
            '''
            return SpeechSplit.main(path,min_duration_on=self.min_duration_on)
        # -------------------------------------------------
        self.AutoSpechRecognition = _AutoSpechRecognition
        self.SpeechSplit = _SpeechSplit
        #使用huggingFace
        if self.ASR_engine == 'h':
            # 实例化语音识别类
            from functions import VoiceRecognition
            self.AFLH = VoiceRecognition.AudioFlowLineHandling()
            self.AFLH.sr = self.sr
            self.AFLH.useMono = self.mono
        #使用Vosk
        elif self.ASR_engine == 'v':
            from functions import Vosk
            self.Vo = Vosk.VoskASR()
            self.Vo.sr = self.sr
            # 这里没有什么需要详细设置的东西
        elif self.ASR_engine == 's':
            from functions import Sphinx
            self.Sph = Sphinx.Sphinx()
            pass
        print('语音识别模型创建完成')
        # ----------------------------------------------
        init_start = time.time()
        from functions import SpeechSplit
        import librosa
        # 这里是定义初始变量
        speechSplit = self.SpeechSplit(self.path)
        self.timeLine = speechSplit['ClipArr']
        self.actualChunk_timeline = speechSplit['ActualChunk']
        self.fullAudio, sr = librosa.load(self.path, sr=self.sr, mono=self.mono)

        #可以把时间最短的拿出来溜溜


        ASR_engine_name_dic = {'h':'Hugging Face','v':'Vosk','s':'Sphinx'}
        printColor('正在使用'+ASR_engine_name_dic[self.ASR_engine]+'引擎进行语音识别').violetRed()
        sentemceDur = [abs(x[-1] - x[0]) for x in self.actualChunk_timeline]
        printColor('单句时间最短minTime:' + str(min(sentemceDur) / self.sr)
                   +'s').yellow()
        printColor('单句时间最长maxTime:' + str(max(sentemceDur) / self.sr)
                   +'s').yellow()
        span = [self.actualChunk_timeline[i+1][0]-self.actualChunk_timeline[i][-1]
                for i in range(len(self.actualChunk_timeline)-1)]
        printColor('maxSpan:'+str(   max(span)/self.sr   )+'s'+'\n'
                   +'avgSpan:'+str(sum(span)/len(span)/self.sr)+'s').yellow()
        printColor('timeline初始化'+str(time.time()-init_start)).violetRed()
        pass








    def _delFromIndex(self, index: int):
        '''
        :param self:
        :param index:
        :return:
        '''
        del self.timeLine[index], self.actualChunk_timeline[index]

    def ToASR(self,index): #  audio=audio, actualChunk_timeline=actualChunk_timeline, fullAudio=fullAudio):
        '''
        :param index: 传入ASR的句子是chunk[index]对应的audio
        :return: string 从huggingface或vosk出来的
        :param actualChunk_timeline: 音频片段在fullAudio中的确切位置
        能够调用同一个方法得益于AutoSpechRecognition的动态变化
        实现：通过chunk得到audio nparray
        '''

        chunk = self.actualChunk_timeline[index]
        audio_ = self.fullAudio[chunk[0]:chunk[-1]]

        printColor('audio.len:' + str(len(audio_) / self.sr) + 's' + '\n' + 'chunk:' + str(chunk)).d()
        printColor('progress:'+str(((chunk[0]+chunk[-1])/2)*100/len(self.fullAudio))).blue()
        # 把audio【index】传到ASR
        return self.AutoSpechRecognition(audio_)



    def GetAll_ToASR(self):
        '''
        :param audio: 分割过的音频集合
        :return: audio*2+fullaudio的集合
        '''
        res = []
        for i in range(len(self.actualChunk_timeline)):
            try:
                sentence = self.ToASR(i)
                res.append(sentence)
            except:
                # 标记错误的
                res.append('error,audio.len:'+str(len(self.actualChunk_timeline[i])/self.sr)+'s')
        return res












start = time.time()
r = ASR('./source/1.wav',engine='s',min_duration_on=1.5).GetAll_ToASR()



printColor('======================================').violetRed()
for c in r:
    if c[0:6] == 'error,' and c[-1] == 's':
        printColor(c).red()
    else:
        printColor(c).green()
end = time.time()-start
if end <= 120:
    end=str(end)+'s'
else:
    end = str(end/60)+'m'
print('time:'+str(end))
