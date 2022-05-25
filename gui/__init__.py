import os,copy
import warnings
from VoiceRecognition_function_goodjin5.translate_mt5 import  Translate_mt5
from PyQt5.QtWidgets import *
# from ToASR import ASR
from Handle_click import Handle_Input_Start
from PyQt5.QtCore import pyqtSignal,QThread


# asr = ASR()
if os.path.isfile('.'):
    path_head = '.'
else:
    path_head = './gui'




handle_Input_Start = Handle_Input_Start()
def ui_button_handle(key,element):
    print('click')


