#! user/bin/env python
# -*- coding: utf-8 -*-

from arya.service import sites
from . import models
from django.utils.safestring import mark_safe
from django.shortcuts import render, HttpResponse
from django.forms import ModelForm
from django.forms import fields


class UserInfoConfig(sites.AryaConfig):
    list_display = ['username', 'username']


class SurveySheetConfig(sites.AryaConfig):
    # 扩展路由
    def extra_urls(self):
        from django.conf.urls import url

        # http://127.0.0.1:8000/arya/app01/surveysheet/1/question_add/
        patterns = [
            url(r'^(?P<sheet_id>\d+)/question_add/$', self.question_add, name="question_add")
            ]
        return patterns

    def question_add(self, request, sheet_id):
        # 手动创建添加问卷问题页面，以支持批量添加
        # 问卷默认：sheet对象， 创建用户对象（登录后存入session)
        sheet_obj = self.model_class.objects.filter(id=sheet_id).first()
        # user_id = request.session.get('login_info').get('id')
        # creator = models.UserInfo.objects.filter(id=user_id).first()
        if request.method == 'GET':
            from django.middleware.csrf import get_token
            get_token(request)

            def generate_choices():
                option_type_choices = models.SurveyOption.option_type
                for item in option_type_choices:
                    yield item

            context = {
                'choices': generate_choices(),
                'sheet_obj': sheet_obj,
                # 'creator': creator
            }

            return render(request, 'question_add.html', context)

        else:
            data = request.POST.get('data')
            print(data)

            from django.http import JsonResponse
            return JsonResponse({'err':None, 'status':202})

    def add_option(self, obj=None, is_header=False):
        if is_header:
            return '创建问题'

        # reverse总是报错，先手写url吧。。。
        tpl = '<a href="/arya/app01/surveysheet/{sheet_id}/question_add/">' \
              '<span class="glyphicon glyphicon-plus"></span></a>'.format(sheet_id=obj.pk)
        return mark_safe(tpl)

    def list_display_edit(self, obj=None, is_header=False):
        # 重写编辑选项，增加预览支持
        if is_header:
            return '操作'
        else:
            tpl = "<a href='/survey/{id}'>预览</a> | " \
                  "<a href='{change}?{params}'>编辑</a> | " \
                  "<a href='{delete}?{params}'>删除</a>" \
                .format(id=obj.pk,
                        change=self.change_url(obj.pk),
                        delete=self.delete_url(obj.pk),
                        params=self.back_url_param())

            return mark_safe(tpl)

    list_display = ['theme', 'remark', 'creator', add_option, list_display_edit]

    def get_show_list_display(self):
        list_display = []
        if self.list_display:
            list_display.extend(self.list_display)
            list_display.insert(0, sites.AryaConfig.list_display_checkbox)

        return list_display


class SurveyOptionForm(ModelForm):
    option = fields.ChoiceField()

    class Meta:
        model = models.SurveyOption
        fields = '__all__'
        labels = {
            'option': '问题类型',
            'question': '问题',
            'sheet': '所属主表',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].choices = models.SurveyOption.option_type


class SurveyOptionConfig(sites.AryaConfig):

    def show_option_type(self, obj=None, is_header=False):
        if is_header:
            return '问题类型'
        return obj.get_option_display()

    list_display = [show_option_type, 'question', 'sheet']

    model_form = SurveyOptionForm


class FeedbackConfig(sites.AryaConfig):
    list_display = ['answer', 'question']


sites.site.register(models.UserInfo, UserInfoConfig)
sites.site.register(models.SurveySheet, SurveySheetConfig)
sites.site.register(models.SurveyOption, SurveyOptionConfig)
sites.site.register(models.Feedback, FeedbackConfig)
