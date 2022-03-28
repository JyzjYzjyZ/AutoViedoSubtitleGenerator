'''
author:goodjin5
v -1.0.4
'''
try:
    # 在文件中调用
    from .AudioFormatConversion_goodjin5 import *
    from .Vosk_VoiceRecognition_goodjin5 import *
    from .HuggingFace_VoiceRecognition_goodjin5 import *
    # from .Sphinx_VoiceRecognition_goodjin5 import *
    from .SpeechSplit_VoiceRecognition_goodjin5 import *
    _config_path = './config.ini'
except:
    # 直接运行
    from AudioFormatConversion_goodjin5 import *
    from Vosk_VoiceRecognition_goodjin5 import *
    from HuggingFace_VoiceRecognition_goodjin5 import *
    # from Sphinx_VoiceRecognition_goodjin5 import *
    from SpeechSplit_VoiceRecognition_goodjin5 import *
    _config_path = '../config.ini'
import torch,warnings,configparser
_voice_model_dict = ['v','h_s','h_b','s','v_hs','v_hb']





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
    def withe(self):
        print(str(self.data))

#-----------------------------------------------------------------------------------------------------------------------

# var
#[path]
path_model_Vosk = r'D:\setup\models\vosk-model-en-us-0.22'
path_model_Sphinx = r'D:\setup\models\sphinx'
path_model_huggingface_big = r'D:\setup\models\facebookhubert-xlarge-ls960-ft'
path_model_huggingface_small = r'D:\setup\models\facebookwav2vec2-large-960h'
path_model_SpeechSplit = r'D:\setup\models\pyannote-segmentation\pytorch_model.bin'


#[option]
device:str = 'cuda:0' if torch.cuda.is_available() else 'cpu'
mono:bool = True
min_during_on:float = 1.2
voice_model_engine:int = 0 # index
progressBar_speechSplit:bool = True
progressBar_recognition:bool  = True
speech_split_sr:int = 16000
debug:bool = False



'''
以下文件是简单的config读取写入功能
附带了一个str==>bool的简单方法
保存在_config路径
与上文变量息息相关
'''


def _toBool(string):
    if string in ['True','ture','T','t',1,'1',1.0,'1.0',True]:
        return True
    elif string in ['False' , 'false' , 'F' , 'f' , 0 , '0' , 0.0 , '0.0' , False]:
        return False
    else:
        raise UserWarning('A bool value in config is incorrectly set')



def load_config():
    config = configparser.ConfigParser()
    config.read(_config_path, encoding="utf-8")
    if config.sections() == []:
        warnings.warn('Failed to load config file Use default value')
        with open(_config_path,'x') as f:
            f.write('[path]\n\n\n[option]')
        save_config()
        return
    global path_model_Vosk,path_model_Sphinx,path_model_huggingface_big,path_model_huggingface_small,path_model_SpeechSplit,\
        device,mono,min_during_on,voice_model_engine,progressBar_speechSplit,progressBar_recognition,speech_split_sr,debug
    try:
        #load_path
        path_model_Vosk = config.get('path','path_model_Vosk')
        path_model_Sphinx = config.get('path','path_model_Sphinx')
        path_model_huggingface_big = config.get('path','path_model_huggingface_big')
        path_model_huggingface_small = config.get('path','path_model_huggingface_small')
        path_model_SpeechSplit = config.get('path','path_model_SpeechSplit')
        #load_option
        device = config.get('option', 'device')
        mono = config.get('option', 'mono')
        min_during_on = float(config.get('option', 'min_during_on'))
        voice_model_engine = int(config.get('option', 'voice_model_engine'))
        progressBar_speechSplit = config.get('option', 'progressBar_speechSplit')
        progressBar_recognition = config.get('option', 'progressBar_recognition')
        speech_split_sr = int(config.get('option', 'speech_split_sr'))
        debug = config.get('option', 'debug')
        # change bool
        mono = _toBool(mono)
        progressBar_recognition = _toBool(progressBar_recognition)
        progressBar_speechSplit = _toBool(progressBar_speechSplit)
        debug = _toBool(debug)
    except:
        warnings.warn(message='Some keys are missing from the config file')
        with open(_config_path, 'w+') as f:
            f.write('[path]\n\n\n[option]')
        save_config()






def save_config():
    config = configparser.ConfigParser()
    config.read(_config_path, encoding="utf-8")
    if config.sections() == []:return
    global path_model_Vosk,path_model_Sphinx,path_model_huggingface_big,path_model_huggingface_small,path_model_SpeechSplit,\
        device,mono,min_during_on,voice_model_engine,progressBar_speechSplit,progressBar_recognition,speech_split_sr
    #save_path
    config.set('path','path_model_Vosk',path_model_Vosk)
    config.set('path','path_model_Sphinx',path_model_Sphinx)
    config.set('path','path_model_huggingface_big',path_model_huggingface_big)
    config.set('path','path_model_huggingface_small',path_model_huggingface_small)
    config.set('path','path_model_SpeechSplit',path_model_SpeechSplit)
    #save_option
    config.set('option', 'device',device)
    config.set('option', 'mono',str(mono))
    config.set('option', 'min_during_on',str(min_during_on))
    config.set('option', 'voice_model_engine',str(voice_model_engine))
    config.set('option', 'progressBar_speechSplit',str(progressBar_speechSplit))
    config.set('option', 'progressBar_recognition',str(progressBar_recognition))
    config.set('option', 'speech_split_sr',str(speech_split_sr))
    config.set('option', 'debug',str(debug))
    with open(_config_path, "w+") as f:
        config.write(f)


# if __name__=='__main__':
#     load_config()
#     device = 'cpu'
#     save_config()


#-----------------------------------------------------------------------------------------------------------------------


