#coding=utf8

from uliweb import expose

@expose('/')
def index():
    return redirect('/yesno/list')