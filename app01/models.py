from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)

    def __str__(self):
        return self.username


class SurveySheet(models.Model):
    """
    问卷主表
    """
    theme = models.CharField(verbose_name='主题', max_length=64)
    date = models.DateField(verbose_name='日期', auto_now_add=True)
    remark = models.TextField(verbose_name='备注')

    creator = models.ForeignKey(verbose_name='创建人',to='UserInfo', null=True)

    def __str__(self):
        tpl = '{date} {theme}（问卷id:{id}）'.format(date=self.date, theme=self.theme, id=self.id)
        return tpl


class SurveyOption(models.Model):
    """
    问卷选项
    """
    option_type = [
        (1, "打分"),
        (2, '问答'),
    ]

    option = models.IntegerField(verbose_name='问题类型', choices=option_type, default=1)
    question = models.CharField(verbose_name='问题', max_length=256)

    sheet = models.ForeignKey(verbose_name='所属主表', to=SurveySheet)

    def __str__(self):
        return self.question


class Feedback(models.Model):
    # 问卷问题有三种类型，回答是否应该考虑三种？
    score = models.IntegerField(verbose_name='打分', null=True)
    answer = models.CharField(verbose_name='反馈', max_length=256)
    date = models.DateField(verbose_name='日期', auto_now_add=True, null=True)

    question = models.ForeignKey(to='SurveyOption')





