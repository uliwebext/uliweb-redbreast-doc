#coding=utf8
from uliweb.orm import *
import datetime

class YesNo(Model):
    content         = Field(TEXT, verbose_name='内容', required=True)
    submitter       = Reference('user', verbose_name='提交人')
    submitter_date  = Field(datetime.datetime, verbose_name='提交时间')
    approver        = Reference('user', verbose_name='审核人')
    approver_date   = Field(datetime.datetime, verbose_name='审核时间')
    approve_result  = Field(str, max_length=100, verbose_name="审核结果")

    task_spec_desc  = Field(str, max_length=255, verbose_name="当前阶段")
    task_spec_name  = Field(str, max_length=100, verbose_name="当前阶段标识")
    workflow        = Reference('workflow', verbose_name='关联工作流', collection_name='yesno')

    class AddForm:
        fields = [
            'content',
        ]

    class EditForm:
        fields = [
            'content',
        ]

    class Table:
        fields = [
            {'name':'approve_result', 'width':30, 'sortable':True},
            {'name':'content', 'width':100, 'sortable':True},
            {'name':'task_spec_desc', 'width':100, 'sortable':True},
            {'name':'task_spec_name', 'width':100, 'sortable':True},
            {'name':'submitter', 'width':100, 'sortable':True},
            {'name':'submitter_date', 'width':100, 'sortable':True},
            {'name':'approver', 'width':100, 'sortable':True},
            {'name':'approver_date', 'width':100, 'sortable':True},
        ]

