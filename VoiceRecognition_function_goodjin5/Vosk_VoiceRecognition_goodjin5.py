from vosk import Model, KaldiRecognizer, SetLogLevel
import json
SetLogLevel(0)
import VoiceRecognition_function_goodjin5



class VoskASR():
    def __init__(self):
        self.sr = 16000
        self.path = VoiceRecognition_function_goodjin5.path_model_Vosk
        self.model = Model(self.path)
        self.tokenizer = KaldiRecognizer(self.model, self.sr)
        self.tokenizer.SetWords(True)


    def read_audioDate(self,audio):
        '''
        :param audio: 确保是sr=16000 mono=True 的librosa:ndarry类型文件
        :return: string:result  另外，字典res中的key=‘result’中有好东西
        '''

        wav = VoiceRecognition_function_goodjin5.toWave(audio)
        self.tokenizer.AcceptWaveform(wav)
        res = self.tokenizer.Result()
        res = json.loads(res)
        return res['text']



