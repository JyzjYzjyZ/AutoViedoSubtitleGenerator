# from functions import SpeechSplit, VoiceRecognition, TextSplit
# import librosa
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
    def __init__(self,path):
        '''
        :param path: 输入音频文件的路径
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
        # 切割的wav音频列表
        self.audio = []
        # 于audio对应的时间轴列表
        self.timeLine = []
        # 于audio对应的音频帧列表
        self.actualChunk_timeline = []
        # 完整音频的wav浮点值列表
        self.fullAudio = []
        # 输出的三个用于映射的字符串列表
        self.resFromAsr = []
        # 实例化语音识别类
        from functions import  VoiceRecognition,TextSplit
        self.AFLH = VoiceRecognition.AudioFlowLineHandling()
        self.AFLH.sr = self.sr
        self.AFLH.useMono = self.mono
        #实例化添加标点类
        self.TP = TextSplit.TextPunctuation()
        #音频分割的单音频片段最短时间(float/second),规避了ASR时间不足的报错问题
        '''
            按照2/3s一个单词的时间计算，最短句，3个单词需要2s。所以1.25s是一个比较合适的值
        '''
        self.min_duration_on = 1.25
        # ---------------------------------------------
        def _AutoSpechRecognition(data):
            '''
            :param data: wav 01-array
            :return: string
            '''
            return self.AFLH.VoiceRecognition(data)

        def _AddPunctuation(seq):
            '''
            :param seq: string
            :return: string with punctuation
            '''
            return self.TP.Punctuation(text=seq)

        def _SpeechSplit(path):
            '''
            :param path: ./2.wav
            :return: timeline audio[list] chunk
            '''
            return SpeechSplit.main(path,min_duration_on=self.min_duration_on)
        # -------------------------------------------------
        self.AutoSpechRecognition = _AutoSpechRecognition
        self.AddPunctuation = _AddPunctuation
        self.SpeechSplit = _SpeechSplit
        # ----------------------------------------------




        from functions import SpeechSplit, TextSplit
        import librosa
        # 这里是定义初始变量
        speechSplit = self.SpeechSplit(self.path)
        self.audio = speechSplit['AudioArr']
        self.timeLine = speechSplit['ClipArr']
        self.actualChunk_timeline = speechSplit['ActualChunk']

        self.fullAudio, sr = librosa.load(self.path, sr=self.sr, mono=self.mono)
        #可以把时间最短的拿出来溜溜


        
        sentemceDur = [abs(x[-1] - x[0]) for x in self.actualChunk_timeline]
        printColor('单句时间最短minTime:' + str(min(sentemceDur) / self.sr)
                   +'s').yellow()
        printColor('单句时间最长maxTime:' + str(max(sentemceDur) / self.sr)
                   +'s').yellow()
        span = [self.actualChunk_timeline[i+1][0]-self.actualChunk_timeline[i][-1]
                for i in range(len(self.actualChunk_timeline)-1)]
        printColor('maxSpan:'+str(   max(span)/self.sr   )+'s'+'\n'
                   +'avgSpan:'+str(sum(span)/len(span)/self.sr)+'s').yellow()

        pass








    def _delFromIndex(self, index: int):
        '''
        :param self:
        :param index:
        :return:
        '''
        del self.audio[index], self.timeLine[index], self.actualChunk_timeline[index]

    def ToASR(self,index, toAsrPervious): #  audio=audio, actualChunk_timeline=actualChunk_timeline, fullAudio=fullAudio):
        '''
        :param index: 传入ASR的句子是audio[index]于audio[index+1]
        :param audio: 在SpeechSplit中切分好的音频区块的列表
        :param actualChunk_timeline: 音频片段在fullAudio中的确切位置
        :param fullAudio: 原始音频的读取
        :return:

        实现：将audio中的两个，fullAudio中的一段输出到ASR
        '''

        audio_ = self.audio[index:index + 2]
        actualChunk_timeline_ = self.actualChunk_timeline[index:index + 2]
        fullAudio_ = self.fullAudio[actualChunk_timeline_[0][0]:actualChunk_timeline_[-1][-1]]
        if self.debug:
            printColor(str(audio_)+str(fullAudio_)+str(actualChunk_timeline_)).d()
        # 把三个送到ASR中去,直接调用上一个，节约性能
        if toAsrPervious != []:
            firstResElem = toAsrPervious[1]  # 就是第二个元素
        else:
            firstResElem = self.AutoSpechRecognition(audio_[0])[0]
        #这里可能因为时间太短而报错，预期是在上层代码中处理完毕
        if self.quick:
            doubleSentences = 'null'
        else:
            doubleSentences = self.AddPunctuation(self.AutoSpechRecognition(fullAudio_)[0])
        return [
            firstResElem,
            self.AutoSpechRecognition(audio_[-1])[0],
            doubleSentences
        ]

    def GetAll_ToASR(self):
        '''
        :param audio: 分割过的音频集合
        :return: audio*2+fullaudio的集合
        '''
        res = []
        toAsr = []
        for i in range(len(self.audio) - 1):
            toAsr = self.ToASR(i, toAsr)
            res.append(toAsr)
        return res

    def ReGeneration(self,delempty_toasr):
        '''
        :param delempty_toasr: Output:function: DelEmpty_ToAsr() 有需要删除元素的索引【audio time chunk】
        :return: 为修改变量的方法，无返回值
        '''
        del_index_list = []
        for c in delempty_toasr:
            del_index = c[0] + c[-1]
            del_index_list.append(del_index)
        del_index_set = set(del_index_list)
        # 在speechSplit,audio,timeline,actuChunk_timeline中删除
        for del_index in list(del_index_set):
            # audio = DelElement(audio,del_index)
            # timeLine = DelElement(timeLine,del_index)
            # actuChunk_timeline = DelElement(actuChunk_timeline,del_index)
            self._delFromIndex(del_index)

        # 运行，从头开始
        getall_toasr=self.GetAll_ToASR()
        self.DelEmpty_ToAsr(getall_toasr)
        printColor('self.timeLine:' + str(len(self.timeLine))+'\n'+'self.resForAsr:' + str(len(self.resFromAsr))).green()
        return

    def DelEmpty_ToAsr(self,getall_toasr, remove=''):
        '''
        :param getall_toasr: Result from function: GetAll_ToASR()
        :param remove: 将要被移除的元素
        :return: 将要被移除的元素在二维列表Output:function: GetAll_ToASR()中的位置
        对于所有符合remove的查找，无关s或p
        # 初始化不作为函数，仅执行一次
        '''
        res = []
        for i in range(len(getall_toasr)):
            c = getall_toasr[i]
            for ii in range(3):
                if c[ii] == remove:
                    # 若双句为空，则必两单句为空。测试是否两单句为空，并不记录双句
                    if ii == 2:
                        # 为双句
                        if [i,0] in res == False:
                            #双句为空但是单句不存在
                            res.append([i,0])
                            warnings.warn('双句为空但是单句不存在,已添加错误单句到列表'+str([i,0]))
                        if [i,1] in res == False:
                            #双句为空但是单句不存在
                            res.append([i,1])
                            warnings.warn('双句为空但是单句不存在,已添加错误单句到列表'+str([i,0]))
                        #若两句都在，没问题
                    else:
                        # 为单句
                        index = [i, ii]
                        res.append(index)
        if res == []:
            #在不等于之前。return多次会进行对self.resFromAsr的错误赋值
            # 调用递归的，多次赋值的
            # 只在res【】时赋值，对于二次或以上调用的。也应该有正确的’getall_toasr‘
            self.resFromAsr = getall_toasr
            printColor('self.timeLine:' + str(len(self.timeLine))+'\n'+'self.resForAsr:' + str(len(self.resFromAsr))).green()
        if res != []:
            # self.debugVar.append(copy.deepcopy(self))
            printColor('语言片段中存在空的元素，这将会重新生成文本'+'\n'+'空元素列表:'+str(res)+'\n'+'正常情况不会出现此提示').blue()
            printColor('self.timeLine:' + str(len(self.timeLine)) + '\n' + 'self.resForAsr:' + str(len(self.resFromAsr))).green()
            self.ReGeneration(res)
        # self.resFromAsr = getall_toasr
        return
        # 更改self值的函数，无需返回值

    def run(self):
        print(self)
        self.DelEmpty_ToAsr(self.GetAll_ToASR())
        if '' in self.resFromAsr:
            raise Exception("''in self.resFromAsr  这本来应该递归清除")
        return self





def demo():
    import time
    start = time.time()
    r = ASR('./source/130.wav')
    r.quick = False
    r = r.run()
    printColor((time.time()-start)/60).d()
    printColor('======================================').violetRed()
    for c in r.resFromAsr:
        printColor(c[0]).d()
    printColor(r.resFromAsr[-1][1]).d()
    return

demo()