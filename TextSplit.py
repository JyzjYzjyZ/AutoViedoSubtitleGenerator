from deepmultilingualpunctuation import PunctuationModel


#  "." "," "?" "-" ":"
class TextPunctuation:
    def __init__(self,ModelRelativePath='./MODELS/oliverguhrfullstop-punctuation-multilang-large'):
        self.ModelRelativePath = ModelRelativePath
        self.model = PunctuationModel(ModelRelativePath)
        print('文本添加标点模型生成完成')
    def Punctuation(self,text:str):
        result = self.model.restore_punctuation(text)
        return result



















