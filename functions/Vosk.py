from vosk import Model, KaldiRecognizer, SetLogLevel
import librosa,numpy,wave,re,json
SetLogLevel(0)


class VoskASR():
    def __init__(self,modelPath:str = './models/vosk-model-en-us-0.22'):
        self.sr = 16000
        self.path = modelPath
        self.model = model = Model(self.path)
        self.tokenizer = KaldiRecognizer(model, self.sr)
        self.tokenizer.SetWords(True)


    def read_audioDate_librosa(self,audio):
        '''
        :param audio: 确保是sr=16000 mono=True 的librosa:ndarry类型文件
        :return: string:result  另外，字典res中的key=‘result’中有好东西
        '''

        wav = (audio * 32767).astype('int16').tobytes()
        self.tokenizer.AcceptWaveform(wav)
        res = self.tokenizer.Result()
        res = json.loads(res)
        return res['text']



