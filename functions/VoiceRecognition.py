import profile
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import librosa
import torch
import time







class AudioFlowLineHandling:
    def __init__(self,ModelRelativePath='./models/facebookwav2vec2-large-960h/'):
        self.sr = 16000
        self.ModelRelativePath=ModelRelativePath
        self.tokenizer = Wav2Vec2Processor.from_pretrained(ModelRelativePath)
        self.model = Wav2Vec2ForCTC.from_pretrained(ModelRelativePath)
        # self.input_type = 'data'# or path
        self.useMono = True


    def VoiceRecognition(self,audio_or_path:str or dict):
        '''
        :param audio_or_path:传入一个音频的地址或numpy.ndarray对象
        :return:返回一个单元素列表 list[str]
        '''
        # init
        if str(type(audio_or_path)) == '<class \'numpy.ndarray\'>':
            audioInput = audio_or_path
        elif type(audio_or_path) == str:
            audio, sr = librosa.load(audio_or_path, sr=self.sr, mono=self.useMono)
            audioInput = audio
        else:
            raise Exception('inputError:你应该在audio_or_path输入一个librosa载入的音频或一个.wav格式音频的路径')

        # input = self.tokenizer(audioInput, return_tensors="pt", padding=False, sr=self.sr)
        input_values = self.tokenizer(audioInput, return_tensors="pt", padding=False, sampling_rate=self.sr).input_values
        # Batch size 1
        # padding(bool, str or PaddingStrategy, optional, defaults
        # to
        # False) - 激活和控制padding。接受以下值。
        #
        # True或
        # 'longest'。填充到批次中最长的序列（如果只提供一个序列，则不填充）。
        # 'max_length': 填充到用参数max_length指定的最大长度，如果没有提供该参数，则填充到模型可接受的最大输入长度。
        # False或
        # 'do_not_pad'（默认）。没有填充（即可以输出一批具有不同长度的序列）。

        # retrieve logits
        logits = self.model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        res = self.tokenizer.batch_decode(predicted_ids)  # input
        return res[0].lower()










