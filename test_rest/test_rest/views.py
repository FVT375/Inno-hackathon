from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wiki_ru_wordnet import WikiWordnet
from nltk.corpus import wordnet
from langid.langid import LanguageIdentifier, model
import langid
import json
from .utils import Squad

def get_language(text):
    langid.set_languages(['en', 'ru'])
    language = langid.classify(text)[0]
    return language

class ContextQuestionAnswering(APIView):
    language = 'ru'

    def squad(self, text, question):
        if self.language == 'ru':
            result = Squad.do(text, question)
        elif self.language == 'en':
            result = model_ans_en([text], [question])[0][0]
        else:
            result = 'error'
        return json.dumps(result, ensure_ascii=False)

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        self.language = get_language(text)
        question = context['question']

        result = self.squad(text, question)
        return result

    def post(self, request):
        result = self.get_answer(request.body)
        return Response(result)


class AutomaticSpellingCorrection(APIView):
    language = 'ru'

    def correct(self, text):
        result = {}
        if self.language == 'ru':
            words = text.split(' ')
            for word in words:
                corr_word = model_corr_ru([word])[0]
                if corr_word != word:
                    result[word] = corr_word
        elif self.language == 'en':
            # TODO: реализация AutomaticSpellingCorrection для english
            result = 'Corrected text: ' + text
        else:
            result = 'error'

        return json.dumps(result, ensure_ascii=False)

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        self.language = get_language(text)

        result = self.correct(text)
        return result

    def post(self, request):
        result = self.get_answer(request.body)
        return Response(result)


class SynonymSearch(APIView):
    language = 'ru'
    wikiwordnet = WikiWordnet()

    def search(self, text):
        if self.language == 'ru':
            words = text.split(' ')
            result = {}
            for word in words:
                synset = self.wikiwordnet.get_synsets(word)[0]
                synonyms = []
                for w in synset.get_words():
                    synonyms.append(w.lemma())
                result[word] = synonyms
                
        elif self.language == 'en':
            words = text.split(' ')
            result = {}
            for word in words:
                synonyms = []
                for synset in wordnet.synsets(word):
                    for w in synset.lemmas():
                        if(w.name() not in synonyms):
                            synonyms.append(w.name())
                result[word] = synonyms
        else:
            result = 'error'

        return json.dumps(result, ensure_ascii=False)

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']

        self.language = get_language(text)

        result = self.search(text)
        return result

    def post(self, request):
        result = self.get_answer(request.body)
        return Response(result)