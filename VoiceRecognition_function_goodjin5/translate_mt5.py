# url:https://huggingface.co/K024/mt5-zh-ja-en-trimmed
# pip install SentencePiece  -i https://pypi.tuna.tsinghua.edu.cn/simple
from transformers import T5Tokenizer,MT5ForConditionalGeneration,Text2TextGenerationPipeline

class Translate_mt5:
  path = "./models/mt5-zh-and-en-trimmed"
  modelVocabulary = 3
  orig = 'en'
  targ = 'zh'
  def __init__(self):
    self.pipe =  Text2TextGenerationPipeline(
    model=MT5ForConditionalGeneration.from_pretrained(self.path),
    tokenizer=T5Tokenizer.from_pretrained(self.path),
    )
    if not (self.orig in ['en','ja','zh']):
      raise Exception(UserWarning,'orig_lang Error')
    if not (self.targ in ['en','ja','zh']):
      raise Exception(UserWarning,'targ_lang Error')
    self.sign = self.orig  +  (str(int(self.modelVocabulary)) if int(self.modelVocabulary) in [1,2,3] else '2')  +  self.targ  +':'

  def translate(self,sentence):
    res = self.pipe(self.sign+sentence, max_length=100, num_beams=4)
    return  res[0]['generated_text']

  def tanslateGroups(self, list):
    res = []
    for c in list:
      td = self.translate(c)
      res.append(td)
    return res

if __name__ == '__main__':
  sentences = '''
  en3zh: custom interfaces that people use so if there's a favorite artist of your of years and he shared he or she shares their interviews you can download i always recommend to do a little bit of research because sometimes people add a lot of stuff i tried to keep it really simple so for me i pretty much just added all of this tools right here which we will be talking about through the course and changed the color to blue because i i really liked that blue color so yeah that's it guys hang on tight because now we have everything that we need to start eight for our first project and our first sculpture so get yourself ready get yourself like really acquainted with the with the way of movements here instead of the sabers with the basic shortcuts of the spacebar and what each of this'''
  t = Translate_mt5()
  r = t.translate(sentences)
  print(r)