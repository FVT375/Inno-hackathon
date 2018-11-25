from deeppavlov import build_model, configs

class Squad():
    model_ru = build_model(configs.squad.squad_ru)
    model_en = build_model(configs.squad.squad)

    def do(self, language, text, question):
        if language == 'ru':
            #return self.model_ru([text], [question])[0][0]
            return (language, text, question)
        if language == 'en':
            #return self.model_en([text], [question])[0][0]
            return (language, text, question)
        
        #error
        return (language, text, question)

class SpellingCorrector():
    model_ru = build_model(configs.spelling_correction.brillmoore_kartaslov_ru)
    #model_en = build_model(configs.spelling_correction.brillmoore_wikitypos_en)

    def do(self, language, text):
        if language == 'ru':
            #return self.model_ru([text])[0]
            return (language, text)
        #if language == 'en':
        #    return self.model_en([text])[0]
        #    return (language, text)
        
        #error
        return (language, text)

def init_models():
    Squad.do('ru', 'test', 'test')
    Squad.do('en', 'test', 'test')
    SpellingCorrector.do('ru', 'test')
    #SpellingCorrector.do('en', 'test')
