import soundfile,librosa, copy,warnings
import numpy as np
import scipy.interpolate as interpolate
try:
    import torch
except:
    warnings.warn(message=r'You don\'t have torch installed which prevents you from using some of the features')
# import torchaudio,wave,torchvision #build时祈福求平安

'''
author:goodjin5
date:2022.3.16 --> 2022.3.19
-v 1.0.2 --> 1.0.3
=====================================
简单的工具类，弥补了librosa载入速度极慢，soundfile不能转换raw,wave难以使用的问题
使用场景 使用多个预训练模型时音频库不统一，实现了一次载入一直可用
支持：以大约46s/130min 的速度加载音频重采样并转换成单声道
input:audioPath  or  nparray:float64
output:tensor:shape(1,x)or shape(x,1)
    numpy：interesting6
    wave二进制：int16
更新：你现在可以从视频中阅读音频了
P.S 从视频中阅读音频 这是一个很多人不知道的librosa的实用功能
=====================================
A simple tool class to compensate for the extremely slow loading of librosa, the inability to convert soundfiles to raw, and the difficulty of using wave
Usage scenarios Audio libraries are inconsistent when using multiple pre-trained models, making them always available on a single load
Support: loading audio resamples and converting to mono at a speed of approximately 46s/130min
input:audioPath or nparray:float64
output:tensor:shape(1,x) or shape(x,1)
    numpy:interest6
    wave binary:int16
UpDate:You can now read the audio from the video
P.S Read audio from video Here's a great feature of librosa that many people don't know about
'''

def resample(sound,orig_sr,target_sr=16000,resample_type:str=None):
    '''
    :param sound: numpy-float64 maybe can run in float 32
    :param orig_sr: 原始的采样率
    :param target_sr: 目标采样率，与原相同或为0时直接返回
    :param resample_type: 采用类型，默认自动分配fast或者best,可以强制指定 使用 'best',  'kaiser_best','fast','kaiser_fast'
    :return: 采样后的nparray
    '''
    if orig_sr == target_sr or target_sr==0:
        return sound,orig_sr


    if resample_type in ['best',  'kaiser_best','fast','kaiser_fast']:
        restype = ['kaiser_best','kaiser_best','kaiser_fast','kaiser_fast'][['best', 'kaiser_best','fast', 'kaiser_fast'].index(resample_type)]
    else:
        restype = ('kaiser_fast' if target_sr <= orig_sr else 'kaiser_best')
    if __name__=='__main__':
        print(resample_type,restype)

    sound = librosa.resample(y=sound,orig_sr=orig_sr,target_sr=target_sr,res_type=restype)
    return sound,target_sr


def read(path:str,sr:int=16000,mono:bool=True):
    '''
    支持音视频格式，所以ffmpeg支持的格式都可以
    :param path: 音频路径
    :param sr: 采样率 为0时采用原始的采样率
    :param mono: 启用单声道
    :return: numpy-float64
    '''
    try:
        sound,orig_sr = soundfile.read(path,dtype='float64')
        sound=sound.T
    except:
        sound, orig_sr = librosa.load(path=path,dtype=np.float64,res_type='kaiser_fast')
    # to mono,and resample sr
    if mono:
        sound = librosa.to_mono(sound)
    # if sr == 0 or target_sr == orig_sr:
    #     # 无需采样
    #     return sound,orig_sr
    # sound = librosa.resample(y=sound,orig_sr=orig_sr,target_sr=target_sr,
    #                          res_type=('kaiser_fast' if target_sr <= orig_sr else 'kaiser_best'))
    sound,s = resample(sound,orig_sr,sr)
    return sound,s




def toWave(sound):
    '''
    :param sound: numpy-float64
    :return: waveFile -bytes
    '''
    # 32767
    return (sound * 32767).astype('int16').tobytes()


def toTorch(sound):
    '''
    :param sound: numpy-float64
    :return: tensor-float32
    '''
    sound = sound.astype('float32')
    t = torch.from_numpy(copy.deepcopy(sound))
    # 扩展维度，维度转换
    return t.unsqueeze(1).permute(1, 0)


def toNumpy_int16(sound):
    return (sound * 32767).astype('int16')


def torchToNumpy_float(sound):
    '''
    :param sound: tensor
    :return: numpy_float float是16还是32由输入的tensor决定
    '''
    # 将所有shape为1的维度降维
    return sound.squeeze().numpy()


def resampleBylen(orig_list:list,target_len:int):
    '''
    同于标准重采样，此函数将len(list1)=x 从采样为len(list2)=y；y为指定的值，list2为输出
    :param orig_list: 是list,重采样的源列表：list1
    :param target_len: 重采样的帧数：y
    :return: 重采样后的数组:list2
    '''
    orig_list_len =len(orig_list)
    k = target_len/orig_list_len
    x = [x*k for x in range(orig_list_len)]
    x[-1] = 3572740
    if x[-1]!=target_len:
        # 线性更改越界结尾
        x1=x[-2];y1=orig_list[-2];x2=x[-1];y2=orig_list[-1]
        y_resa = (y2 - y1) * (target_len - x1) / (x2 - x1) + y1
        x[-1] = target_len;orig_list[-1]=y_resa
    # 使用了线性的插值方法，也可以根据需要改成其他的。推荐是线性
    f = interpolate.interp1d(x,orig_list,'linear')
    del x
    resample_list = f([x for x in range(target_len)])
    return resample_list


'''

if __name__=='__main__':
    # exaxmple
    # You can test performance and usability here
    # change 'AUDIO_PATH.wav' or 'Video_path.*' all format[ffmpeg]
    path = 'AUDIO_PATH.wav'
    path = r'D:\setup\wav\130.wav'
    import matplotlib.pyplot as plt
    numpy_float64,sr = read(path,0,True)
    # 把target设置的过低会出现不能除以0的错误
    res_low,sr = resample(numpy_float64,sr,target_sr=100,resample_type='kaiser_best')
    # resample(numpy_float64,sr,50000,'kaiser_best')
    wave = toWave(numpy_float64)
    tensor = toTorch(numpy_float64)
    numpy_int16 = toNumpy_int16(numpy_float64)
    resamplr_bylen = resampleBylen(numpy_float64.tolist(),5000)
    plt.figure(figsize=(1000, 50), dpi=80)
    plt.subplot(111)
    plt.plot(resamplr_bylen, color='red',linestyle="-",alpha=1)
    # plt.plot(numpy_float64.tolist(), color='green',linestyle="-",alpha=1)
    plt.plot(res_low.tolist(), color='blue',linestyle="-",alpha=1)
    plt.text(5, 0.4, 'InAudio,max{0},min{1}\nred:By len\nblue:By sr'
             .format(max(numpy_float64.tolist()),min(numpy_float64.tolist())))
    plt.show()
    print('Passing the test')
    
'''