# AutoViedoSubtitleGenerator
用于自动为视频添加字幕
## introduction
我不想赘述太多，目前正处于测试阶段

调用ASR/STT  huggingface-facebookwave;vosk;sphinx-project-5

支持config 全离线的字幕生成

必要库见源码，使用方法简单 自行阅读ToASR最后一段
详细运行结果请看
```
[output]
# 3种引擎huggingFace_l _xl Vosk 5+组合可选 ；弃用了效果最差的Sphinx
<Vosk>time:65.21595287322998s
D:\python\envs\e-28-1\python.exe D:/project/@demo/ToASR.py
LOG (VoskAPI:ReadDataFiles():model.cc:213) Decoding params beam=13 max-active=7000 lattice-beam=6
LOG (VoskAPI:ReadDataFiles():model.cc:216) Silence phones 1:2:3:4:5:11:12:13:14:15
LOG (VoskAPI:RemoveOrphanNodes():nnet-nnet.cc:948) Removed 0 orphan nodes.
LOG (VoskAPI:RemoveOrphanComponents():nnet-nnet.cc:847) Removing 0 orphan components.
LOG (VoskAPI:CompileLooped():nnet-compile-looped.cc:345) Spent 0.083782 seconds in looped compilation.
LOG (VoskAPI:ReadDataFiles():model.cc:248) Loading i-vector extractor from D:\setup\models\vosk-model-en-us-0.22/ivector/final.ie
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:183) Computing derived variables for iVector extractor
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:204) Done.
LOG (VoskAPI:ReadDataFiles():model.cc:278) Loading HCLG from D:\setup\models\vosk-model-en-us-0.22/graph/HCLG.fst
LOG (VoskAPI:ReadDataFiles():model.cc:293) Loading words from D:\setup\models\vosk-model-en-us-0.22/graph/words.txt
LOG (VoskAPI:ReadDataFiles():model.cc:302) Loading winfo D:\setup\models\vosk-model-en-us-0.22/graph/phones/word_boundary.int
LOG (VoskAPI:ReadDataFiles():model.cc:309) Loading subtract G.fst model from D:\setup\models\vosk-model-en-us-0.22/rescore/G.fst
LOG (VoskAPI:ReadDataFiles():model.cc:311) Loading CARPA model from D:\setup\models\vosk-model-en-us-0.22/rescore/G.carpa
LOG (VoskAPI:ReadDataFiles():model.cc:317) Loading RNNLM model from D:\setup\models\vosk-model-en-us-0.22/rnnlm/final.raw
LOG (VoskAPI:CompileLooped():nnet-compile-looped.cc:345) Spent 0.00897598 seconds in looped compilation.
Please enter the path to the audio/video filed
# 进度条
100%|██████████| 9/9 [00:29<00:00,  3.27s/it]
# 语音识别结果
if you want to sculpt amazing creatures characters props environments but dunno why
where to start if that is the case then i welcome you to next is complete guide to sievers
twenty twenty two my name is abraham leo i have eleven years of experience in the industry and i've been teaching for the past seven years i also manage my own studio here
mexican and i will be your instructor throughout this course in this course we will be covering of the most important aspects inside of sievers i will be showing you different ways in which you can start your projects and bring to life all of the amazing things that lived inside your aim
originates through this course we will be learning about the principle
sculpting in mesh sees for years archer visto poly paint rendering and
much more this course is divided into ten chapters each chapter will develop one project that will use specific tools about the piper at the end of all this courses you will be able to read anything that you can imagine
this means i have the signs of sports for beginner level students will want to start their career besides the sieber software and that the only thing you need is to have a pen tablets work is going to be very important make sure to have supers twenty two as well in the latest update your bread
join me and start grading amazing sculptures with version twenty
Using China server backend.
_try_translate 429 Client Error: Too many requests for url: https://www2.deepl.com/jsonrpc?method=LMT_split_into_sentences
# 多线程复合翻译
# https://github.com/JyzjYzjyZ/MultiThreaded_Composite_Translate_100perCentSuccessRate
=============================================
如果你想塑造神奇的生物角色道具环境，但不知道为什么
 从哪里开始如果是这样的话，那么我欢迎你到下一个是完整的西弗斯指南
 二十二我的名字亚伯拉罕·利奥，我在这个行业有11年的经验在过去的七年里，我一直在教书，我也在这里管理我自己的工作室
 墨西哥人，我将在本课程中成为你的导师。在本课程中，我们将涵盖最重要的方面在西弗斯，我将向你展示不同的方式你可以开始你的项目，把你目标中所有令人惊奇的东西变成现实
 起源于本课程，我们将学习原理
 多年来在网格中雕刻archer visto poly油漆渲染和
 更多本课程分为十章每一章将开发一个项目，该项目将使用关于吹笛者的特定工具。在所有课程的最后，你将能够阅读任何你能想象的东西
 这意味着我有标志对于初学者来说，运动的学生会想开始他们的除了sieber软件之外的职业生涯，你唯一需要的就是拥有一个笔式平板电脑，工作将是非常重要的，确保在最新的更新中拥有超级二十二，你的面包
 加入我，开始用版本给令人惊叹的雕塑评分二十
Identification is complete, config is saved, press enter to exit
```
------------------------------------------------------
author:goodjin5

现在编译以完成需要管线版本请>goodjin5add0@gmail.com<  <free!>

![Image text](https://github.com/JyzjYzjyZ/AutoViedoSubtitleGenerator/blob/main/img/H2iQBHGA2B.png?raw=true)

19G/30G (zip/unzip) && build , source,project file
