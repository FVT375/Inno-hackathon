from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wiki_ru_wordnet import WikiWordnet
from nltk.corpus import wordnet
from langid.langid import LanguageIdentifier, model
import json


def get_language(text):
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    language = identifier.classify(text)[0]

    return language


class ContextQuestionAnswering(APIView):
    language = 'ru'

    def squad(self, text, question):
        if self.language == 'ru':
            # TODO: реализация ContextQuestionAnswering для russian
            answer = 'Текст: ' + text + '. Вопрос: ' + question + '. Ответ: ЮЮЮЮЮЮЮ'
        elif self.language == 'en':
            # TODO: реализация ContextQuestionAnswering для english
            answer = 'Text: ' + text + '. Question: ' + question + '. Answer: LLLLLLLLLL'
        else:
            answer = 'error'

        return answer

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        question = context['question']
        self.language = get_language(text)
        result = self.squad(text, question)

        return '{answer: ' + result + '}'

    def post(self, request):
        result = self.get_answer(request.body)

        return Response(result)


class AutomaticSpellingCorrection(APIView):
    language = 'ru'

    def correct(self, text):
        if self.language == 'ru':
            # TODO: реализация AutomaticSpellingCorrection для russian
            corrected_text = 'Исправленный текст: ' + text
        elif self.language == 'en':
            # TODO: реализация AutomaticSpellingCorrection для english
            corrected_text = 'Corrected text: ' + text
        else:
            corrected_text = 'error'

        return corrected_text

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        self.language = get_language(text)
        result = self.correct(text)

        return '{answer: ' + result + '}'

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

            result = json.dumps(result, ensure_ascii=False)
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

            result = json.dumps(result, ensure_ascii=False)
        else:
            result = 'error'

        return result

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        self.language = get_language(text)
        result = self.search(text)

        return '{answer: ' + result + '}'

    def post(self, request):
        result = self.get_answer(request.body)

        return Response(result)