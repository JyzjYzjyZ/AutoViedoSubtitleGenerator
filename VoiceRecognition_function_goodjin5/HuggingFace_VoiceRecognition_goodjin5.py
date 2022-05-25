from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, HubertForCTC
import librosa
import torch
import VoiceRecognition_function_goodjin5



#                  ModelRelativePath='./models/facebookwav2vec2-large-960h/',
#                  ModelRelativePathBig='./models/facebookhubert-xlarge-ls960-ft/'



class AudioFlowLineHandling:
    def __init__(self):
        self.sr = 16000
        if VoiceRecognition_function_goodjin5.voice_model_engine in [2,5]:
            # xl
            self.path = VoiceRecognition_function_goodjin5.path_model_huggingface_big
            self.model = HubertForCTC.from_pretrained(self.path)
        if VoiceRecognition_function_goodjin5.voice_model_engine in [1,4]:
            # l
            self.path = VoiceRecognition_function_goodjin5.path_model_huggingface_small
            self.model = Wav2Vec2ForCTC.from_pretrained(self.path)

        self.tokenizer = Wav2Vec2Processor.from_pretrained(self.path)
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

        # retrieve logits
        logits = self.model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        res = self.tokenizer.batch_decode(predicted_ids)  # input
        return res[0].lower()






if __name__=='__main__':
    from transformers.dependency_versions_check import pkgs_to_check_at_runtime
    print(pkgs_to_check_at_runtime)
    # ['python', 'tqdm', 'regex', 'sacremoses', 'requests', 'packaging', 'filelock', 'numpy', 'tokenizers']



