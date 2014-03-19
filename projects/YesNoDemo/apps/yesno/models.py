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
    workflow        = Reference('workflow', verbose_name='关联工作流', collection_name='yesno')

    class AddForm:
        fields = [
            'content',
        ]

    class EditForm:
        fields = [
            'content',
        ]

    class DetailView:
        fields = [
            'content', 'submitter', 'submitter_date', 'approve_result'
        ]

    class Table:
        fields = [
            {'name':'id', 'width':40, 'sortable':True, 'verbose_name': '标识'},
            {'name':'approve_result', 'width':100, 'sortable':True},
            {'name':'content', 'width':100, 'sortable':True},
            {'name':'submitter', 'width':100, 'sortable':True},
            {'name':'submitter_date', 'width':100, 'sortable':True},
            {'name':'approver', 'width':100, 'sortable':True},
            {'name':'approver_date', 'width':100, 'sortable':True},
        ]

