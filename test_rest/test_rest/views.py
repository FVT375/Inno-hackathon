from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wiki_ru_wordnet import WikiWordnet
from nltk.corpus import wordnet
from langid.langid import LanguageIdentifier, model
import langid
import json
from .utils import Squad, SpellingCorrector
from django.http import JsonResponse
from pymystem3 import Mystem
from nltk.stem import WordNetLemmatizer

mystem = Mystem()
wordnet_lemmatizer = WordNetLemmatizer()
wikiwordnet = WikiWordnet()
squad_ = Squad()
spelling_corrector = SpellingCorrector()

langid.set_languages(['en', 'ru'])

def get_language(text):
    language = langid.classify(text)[0]
    return language

class ContextQuestionAnswering(APIView):
    language = 'ru'

    def squad(self, text, question):
        result = {}
        t = squad_.do(self.language, text, question)
        if t != 'error':
            result['answer'] = t
        print("####")
        print(result)
        print("####")
        return json.dumps(result, ensure_ascii=False)

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        question = context['question']

        self.language = get_language(text)

        result = self.squad(text, question)
        return result

    def post(self, request):
        result = self.get_answer(request.body)
        return JsonResponse(result, safe=False)


class AutomaticSpellingCorrection(APIView):
    language = 'ru'

    def correct(self, text):
        result = []
        words = text.split(' ')
        for word in words:
            corr_word = spelling_corrector.do(self.language, word)
            if corr_word != 'error' and corr_word != word:
                result.append(corr_word)

        return json.dumps(result, ensure_ascii=False)

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        self.language = get_language(text)

        result = self.correct(text)
        return result

    def post(self, request):
        result = self.get_answer(request.body)
        return JsonResponse(result, safe=False)


class SynonymSearch(APIView):
    language = 'ru'

    def search(self, text, query):
        query_words = query.split(' ')
        query_synonyms = {}
        print(query_words)
        for word in query_words:
            if self.language == 'ru':
                if len (wikiwordnet.get_synsets(word)) > 0:
                    synset = wikiwordnet.get_synsets(word)[0]
                else: continue
                synonyms = []
                for w in synset.get_words():
                    synonyms.append(w.lemma())
                t = mystem.lemmatize(word)
                print(t[0])
                query_synonyms[t[0]] = synonyms
                print(synonyms)

            elif self.language == 'en':
                synonyms = []
                for synset in wordnet.synsets(word):
                    for w in synset.lemmas():
                        if(w.name() not in synonyms):
                            synonyms.append(w.name())
                t = wordnet_lemmatizer.lemmatize(word)
                print(t[0])
                query_synonyms[t] = synonyms
            
        result = []
        #text_words = ''
        if self.language == 'ru':
            text_words = mystem.lemmatize(text)
        else:
            text_words = wordnet_lemmatizer.lemmatize(text)
        for word in text_words:
            for query_word in query_synonyms:
                if word in query_synonyms[query_word]:
                    result.append(word)
            
        #     synonyms = []
        #     if self.language == 'ru':
        #         if len (self.wikiwordnet.get_synsets(word)) > 0:
        #             synset = self.wikiwordnet.get_synsets(word)[0]
        #         else: continue
        #         for w in synset.get_words():
        #             for query_word in query_synonyms:
        #                 if w.lemma() in query_synonyms[query_word]:
        #                     synonyms.append(w.lemma())
        #     print("### synonyms ru")
        #     print(synonyms)
        #     print("###")
        #     if self.language == 'en':
        #         for synset in wordnet.synsets(word):
        #             for w in synset.lemmas():
        #                 for query_word in query_synonyms:
        #                     if w.name() in query_synonyms[query_word] and w.name() not in synonyms:
        #                         synonyms.append(w.name())
        #     print("### synonyms en")
        #     print(synonyms)
        #     print("###")
        #     result[word] = synonyms
        
        # found = []
        # index = 0
        # for word in text_words:
        #     if self.language == 'ru':
        #         if len (self.wikiwordnet.get_synsets(word)) > 0:
        #             synset = self.wikiwordnet.get_synsets(word)[0]
        #         else: break
        #         synonyms = []
        #         for w in synset.get_words():
        #             for query_word in query_synonyms:
        #                 if w.lemma() in query_synonyms[query_word]:
        #                     found.append(index)
        #     index += 1

        # result = {}
        # if len(found) > 1:
        #     possible_words = []
        #     # if found < len(text_words - 1):
        #     #     possible_words.append(text_words[found+1])
        #     # if found > 0:
        #     #     possible_words.append(text_words[found-1])
        #     for i in range(len(found) - 2):
        #         if found[i] + 1 == found[i+1]:
        #             possible_words.append((text_words[found[i]], text_words[found[i+1]]))

        #     if possible_words:
        #         result['result'] = possible_words
        return json.dumps(result, ensure_ascii=False)

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        query = context['query']

        self.language = get_language(text)

        result = self.search(text, query)
        return result

    def post(self, request):
        result = self.get_answer(request.body)
        return JsonResponse(result, safe=False)