from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class ContextQuestionAnswering(APIView):
    def squad(self, text, question):
        # TODO: реализация ContextQuestionAnswering

        answer = 'Text: ' + text + '. Question: ' + question + '. Answer: AAAAAAAAAA'

        return answer

    def squad_get_answer(self, context):
        context = json.loads(context.decode('utf-8'))
        text = context['text']
        question = context['question']
        result = self.squad(text, question)

        return '{answer: ' + result + '}'

    def post(self, request):
        result = self.squad_get_answer(request.body)

        return Response(result)