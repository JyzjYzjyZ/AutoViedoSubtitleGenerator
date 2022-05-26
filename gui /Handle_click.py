import os,copy
import warnings
from VoiceRecognition_function_goodjin5.translate_mt5 import  Translate_mt5
from PyQt5.QtWidgets import *
from ToASR import ASR
from PyQt5.QtCore import pyqtSignal,QThread


class Thread(QThread):
    def __init__(self, func):
        super(Thread, self).__init__()
        self.func = func
        print(self.func)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class HandleClickStart():

    refrenceLen =30
    standard = '，'
    addRule = ['。',',','.']
    def __init__(self):
        self.asr = ASR()

    def make_sentence_short(self, sentences, chunk, sr):  # , refrenceLen,standard,addRule
        def encode(sentences: list, max_len=self.refrenceLen, Non_IdentifySentences
        =True):
            '''
            根据句子长度重新分配
            :param sentences: [sentence1,sentence2,...]
            :param max_len: The maximum length after encoding is generally much less than this value
            :return:[sentence1+sentence2,sentence3+sentence4+sentence5,...]
            '''

            # while '' in sentences:
            #     sentences.remove('')

            # if len(sentences) == 1:
            #     if Non_IdentifySentences:
            #         return sentences, [1]
            #     return sentences

            def _getListLen(l):
                le = 0
                for c in l:
                    le += len(c)
                return le

            def _chagesentences(sentences, max_len):
                temp = []
                clear = []
                for sentence in sentences:
                    # 放进去以后的长度
                    if len(sentence) + _getListLen(temp) + len(temp) * 2 > max_len:
                        if len(temp) != 0:
                            clear.append(temp)
                        # 内部无内容，必至少放一句
                        temp = [sentence]
                    else:
                        # 能够放进去
                        temp.append(sentence)

                if temp != []:
                    clear.append(temp)
                return clear

            def _change_to_list(clearList):

                arr = copy.copy(clearList)
                for y in range(len(arr)):
                    for x in range(len(arr[y])):
                        arr[y][x] = [arr[y][x]]
                for i in range(len(arr)):
                    c = arr[i]
                    c = str(c).replace('["', '[').replace('"]', ']').replace("['", '[').replace("']", ']').replace(
                        '], ', ']')
                    c = c[1:-1]
                    # c = del_by_index_from_string(c,1)
                    # c = del_by_index_from_string(c,-2)
                    arr[i] = c
                return arr

            res = _chagesentences(sentences, max_len)
            result = _change_to_list(res)
            return_result = []
            if Non_IdentifySentences:
                weighting_l = []
                for c in result:
                    weighting_l.append(c.count('['))
                    return_result.append(
                        c.replace('[', '').replace(']', '')
                    )
                return return_result, weighting_l
            return result

        def Distribution_len(chunk, sentences, addRule, standard, max=self.refrenceLen):
            '''重新计算时间长度'''
            index = -1
            ch = []
            se = []
            for sentence in sentences:
                index += 1
                repl_sen = copy.copy(sentence)
                for rep in addRule:
                    # 支持数组分割
                    repl_sen = repl_sen.replace(rep, standard)
                # 去掉开头和结尾的符号
                repl_sen = repl_sen[1:] if repl_sen[0] == standard else repl_sen
                repl_sen = repl_sen[0:-1] if repl_sen[-1] == standard else repl_sen
                # repl_sen = sentence.replace(addRule, standard)# 为分割做准备
                l, weight = encode(repl_sen.split(standard),  # 在这里，由于一个句子的分割必定损失一个标点，所以weight的计算是看分句的数量。与哪个标点被替换无关
                                   max, True)
                t = chunk[index]
                sentence_len = len(sentence)
                t_delta = t[-1] - t[0]

                last_endTime = t[0]
                con_chunk = []
                x = -1
                for c in l:
                    x += 1
                    # 计算时间头尾 [  [f,f]  [s,e]]
                    inceas_time = ((len(c) + weight[x]) * t_delta) / sentence_len
                    this_chunk = [last_endTime, last_endTime + inceas_time]
                    last_endTime += inceas_time
                    con_chunk.append(this_chunk)

                ch += con_chunk
                se += l
            return ch, se

        def chunkToTimeline(chunk, sr):
            '''
            区块到时间线
            还需处理为srt标准'''

            def chunkToTimelineSingle(second: float):
                def addZero(x):
                    if len(str(x)) == 0: raise Exception('calc timeline error')
                    return '0' + str(x) if len(str(x)) == 1 else str(x)

                hour = int(second / 3600)
                minute = int((second - hour * 3600) / 60)
                second = (second - hour * 3600 - minute * 60)
                # r = f'{addZero(hour)}:{addZero(minute)}:{addZero(second)}'
                return f'{addZero(hour)}:{addZero(minute)}:{addZero(second)}'

            # to second
            x = [
                [c[0] / sr, c[-1] / sr] for c in chunk
            ]
            timeLine = []
            intChunk = []
            for c in x:
                timeLine.append(
                    [
                        chunkToTimelineSingle(c[0]), chunkToTimelineSingle(c[-1])
                    ]
                )
            for c in chunk:
                intChunk.append(
                    [float(c[0]), float(c[-1])]
                )
            return timeLine, intChunk

        def changeTimeline(timeLine):
            '''处理为srt标准'''
            r = []
            for c in timeLine:
                r.append(c[0] + ' -->  ' + c[-1])
            return r

        chunk_short, sentences_short = Distribution_len(chunk, sentences, self.addRule, self.standard, self.refrenceLen)
        timeLine, int_chunk = chunkToTimeline(chunk_short, sr)
        return sentences_short, chunk_short, int_chunk, changeTimeline(timeLine)



    def responseFilename(self,Filename,signal_res:pyqtSignal=None,write=True):
        # 做一些处理和计算
        f = Filename.replace('/','''\\''')
        asr,t,s = self.asr.run(f)
        # use translate
        mt5 = Translate_mt5()
        s_zh =  mt5.tanslateGroups(s)
        sentences_short, chunk_short, int_chunk, timeLine = self.make_sentence_short(
            sentences=s_zh, chunk=asr.actualChunk_timeline,
            sr=asr.audio_origin_sr,
            # refrenceLen=self.refrenceLen,standard=self.standard,addRule=self.addRule
        )
        # mix
        mix_list_zh = asr.Mix_timeLineToSentences(timeLine,sentences_short)
        # mix_list_en = asr.Mix_timeLineToSentences(timeLine,s)
        [print(x) for x in mix_list_zh]
        if signal_res:
            signal_res[:] = mix_list_zh
        if write:
            self.writeSubtitle(Filename,mix_list_zh)
        return mix_list_zh# ,mix_list_en
    def writeSubtitle(self,filename,list):
        with open(os.path.splitext(filename)[0] + '.srt', 'w') as f:
            for c in list:
                f.write(c + '\n')
            # for c in en:
            #     f.write(c + '\n')
    def muiltThread_start(self,filename,signal:pyqtSignal=None,write=True):

        # 计算子线程 写入主线程 涉及到通信 signal使用了inputClass.button.pysignalResult
        thread = Thread(lambda: self.responseFilename(filename,signal,write))
        thread.start()
        # signal.connect(writeSubtitle)


    # def _testThread(self):
    #     for i in range(int(1e10)):
    #         print(1)


def clickEvent_getFilename(self,element):
        errorList = []
        filenames, selectType = QFileDialog.getOpenFileNames(element, '选择音视频', os.getcwd(),
                                                             "All Files(*);;Text Files(*.txt);;"
                                                             "Mp4 Files Viedo(*.mp4);;Mp3 Sound(*.mp3);;Wav Sound(*.wav)")
        for filename in filenames:
            if os.path.exists(filename):
                try:
                    self.muiltThread_do(filename)  # zh =  responseFilename(filename)#,en
                    # 开线程
                except Exception:
                    warnings.warn(f'failed to response{filename}', UserWarning, )
                    errorList.append(f'{filename}_fileError:  {str(Exception)}')  # 记录错误
            else:
                warnings.warn(f'failed to find{filename}', UserWarning, )
                if filename != '':
                    errorList.append(filename + '_notFindError')
        return errorList

class Handle_Input_Start():

    def __init__(self):
        self.handleStart = HandleClickStart()
        self.errorList = []
        self.filenames = []
        # Signal >默认行为是自动写入

    def HandleInput(self,element):
        filenames, selectType = QFileDialog.getOpenFileNames(element, '选择音视频', os.getcwd(),
                                                             "All Files(*);;Text Files(*.txt);;"
                                                             "Mp4 Files Viedo(*.mp4);;Mp3 Sound(*.mp3);;Wav Sound(*.wav)")
        self.filenames += filenames
        self.element = element
        print(self.filenames)

    def HandleStart(self):
        self.handleStart.muiltThread_start(self.filenames[0],None,True)
