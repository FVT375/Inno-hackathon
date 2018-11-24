from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class ContextQuestionAnswering(APIView):
    language = 'russian'

    def squad(self, text, question):
        if self.language == 'russian':
            # TODO: реализация ContextQuestionAnswering для russian
            answer = 'Текст: ' + text + '. Вопрос: ' + question + '. Ответ: ЮЮЮЮЮЮЮ'
        else:
            # TODO: реализация ContextQuestionAnswering для english
            answer = 'Text: ' + text + '. Question: ' + question + '. Answer: LLLLLLLLLL'

        return answer

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        question = context['question']
        result = self.squad(text, question)

        return '{answer: ' + result + '}'

    def post(self, request):
        # self.language = распознать язык
    
        result = self.get_answer(request.body)

        return Response(result)


class AutomaticSpellingCorrection(APIView):
    language = 'russian'

    def correct(self, text):
        if self.language == 'russian':
            # TODO: реализация AutomaticSpellingCorrection для russian
            corrected_text = 'Исправленный текст: ' + text
        else:
            # TODO: реализация AutomaticSpellingCorrection для english
            corrected_text = 'Corrected text: ' + text

        return corrected_text

    def get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        result = self.correct(text)

        return '{answer: ' + result + '}'

    def post(self, request):
        # self.language = распознать язык

        result = self.get_answer(request.body)

        return Response(result)