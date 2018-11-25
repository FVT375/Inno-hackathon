from deeppavlov import build_model, configs

class Squad():
    model_ru = build_model(configs.squad.squad_ru)
    model_en = build_model(configs.squad.squad)

    def do(self, language, text, question):
        if language == 'ru':
            return self.model_ru([text], [question])[0][0]
        if language == 'en':
            return self.model_en([text], [question])[0][0]
        
        #error
        return ('error')

class SpellingCorrector():
    model_ru = build_model(configs.spelling_correction.brillmoore_kartaslov_ru)
    #model_en = build_model(configs.spelling_correction.brillmoore_wikitypos_en)

    def do(self, language, text):
        if language == 'ru':
            return self.model_ru([text])[0]
        
        #error
        return ('error')

def init_models():
    a = Squad()
    a.do('ru', 'test', 'test')
    a.do('en', 'test', 'test')

    b = SpellingCorrector()
    b.do('ru', 'test')
    #SpellingCorrector.do('en', 'test')
