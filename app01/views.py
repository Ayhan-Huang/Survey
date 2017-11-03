from django.shortcuts import render, HttpResponse
from . import models
import json


def survey(request, id):
    if request.method == 'GET':
        from django.middleware.csrf import get_token
        get_token(request)

        sheet = models.SurveySheet.objects.filter(id=id).first()
        options = sheet.surveyoption_set.all()

        context = {
            'sheet': sheet,
            'options': options
        }

        return render(request, 'survey.html', context)

    if request.method == 'POST':
        raw_data = request.POST.get('data')
        data = json.loads(raw_data)
        print(data)
        data = {
            '2': {'choose': '10', 'text': '啊手动阀手动阀'},
            '3': {'choose': None, 'text': '啊手动阀手动阀'},
            '4': {'choose': '7', 'text': '阿斯蒂芬阿斯顿发'},
            'err': False
        }
        data.pop('err')
        
        for k, v in data.items():
            id = int(k)
            question_obj = models.SurveyOption.objects.filter(id=id).first()
            models.Feedback.objects.create(
                score=v['choose'],
                answer=v['text'],
                question = question_obj
            )

        return HttpResponse('123')


def test(request):
    return render(request, 'test.html')
