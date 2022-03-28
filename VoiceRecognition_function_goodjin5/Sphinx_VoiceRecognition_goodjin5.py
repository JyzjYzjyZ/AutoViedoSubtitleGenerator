# https://cmusphinx.github.io/wiki/download/
import time, librosa, numpy, os
import pocketsphinx

from datetime import datetime
from datetime import timezone







class Sphinx():
    def __init__(self):
        # 获取当前时间
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.local_now = str(utc_now.astimezone()).split('.', 1)[0].replace(':', '.')
        # 设置基础路径
        self.hmm = './models/sphinx/en-US/acoustic-model/'
        self.lm = './models/sphinx/en-US/language-model.lm.bin'
        self.dict = './models/sphinx/en-US/pronounciation-dictionary.dict'
        self.log = './log/sphinx@'+self.local_now+'.txt'
        # 设置编码器
        config = pocketsphinx.Decoder.default_config()
        config.set_string("-hmm",self.hmm)  # set the path of the hidden Markov model (HMM) parameter files
        config.set_string("-lm", self.lm)
        config.set_string("-dict", self.dict)
        config.set_string("-logfn", self.log)  # disable logging (logging causes unwanted output in terminal)
        self.decoder = pocketsphinx.Decoder(config)




    def STT(self,audio):
        wave = (audio * 32767).astype('int16').tobytes()
        # perform the speech recognition with the keywords file (this is inside the context manager so the file isn;t deleted until we're done)
        # decoder.set_kws("keywords", f.name)
        # decoder.set_search("keywords")
        # 对于需要使用keywords的，上面提供了基本的方法
        self.decoder.start_utt()  # begin utterance processing
        self.decoder.process_raw(wave, False,True)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
        self.decoder.end_utt()
        hypothesis = self.decoder.hyp().hypstr
        return hypothesis