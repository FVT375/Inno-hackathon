from deeppavlov import build_model, configs

class Squad():
    model = build_model(configs.squad.squad_ru)

    def do(self, text, question):
        #return self.model([text], [question])[0][0]
        return (text, question)

def init_models():
    Squad.do('test', 'test')
