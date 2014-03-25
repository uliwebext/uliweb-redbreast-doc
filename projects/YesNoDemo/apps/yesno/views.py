#coding=utf8

from uliweb import expose, functions, settings, decorators
from uliweb.i18n import gettext_lazy as _
from uliweb.contrib.flashmessage import flash
import datetime

def __begin__():
    from uliweb import functions
    return functions.require_login()

def get_yesno_form(from_task, to_tasks):
    from uliweb.form import Form, Button, TextField, HiddenField

    btns = []
    for k, v in to_tasks:
        btns.append(Button(value=k, _class="btn btn-primary btnDeliver",
            type='button', id='%s'%k))

    class YesNoForm(Form):
        form_buttons = btns
        trans_message = TextField(label='流转意见', html_attrs={'style':'width:80%'}, required=True)
        from_task_id = HiddenField(label='id',
            html_attrs={'style':'display:none'}, default=from_task.get_unique_id())

    return YesNoForm()    

@expose('/yesno/')
class YesNoView(object):

    def __init__(self):
        self.model = functions.get_model('yesno')

    def list(self):
        from uliweb.utils.generic import ListView, get_sort_field

        def id(value, obj):
            return "<a href='/yesno/view/%d'>%d</a>" % (value, value)

        fields_convert_map = {'id': id}
        view = ListView(self.model, fields_convert_map=fields_convert_map)

        if 'data' in request.values:
            return json(view.json())
        else:
            result = view.run(head=True, body=False)
            result.update({'table':view})
            return result

    def add(self):
        from uliweb.utils.generic import AddView

        def pre_save(data):
            data['submitter'] = request.user.id
            data['submitter_date'] = datetime.datetime.now()

        def post_save(obj, data):
            Workflow = functions.get_workflow()

            workflow = Workflow.create("YesNoWorkflow", operator=request.user)

            workflow.ref_unique_id = "yesno,%d" % obj.id
            workflow.start()
            workflow.run()

            obj.workflow = workflow.get_id()
            obj.save()

        view = AddView(self.model, url_for(self.__class__.list),
             pre_save=pre_save, post_save=post_save)

        result = view.run()
        return result

    def view(self, id):
        from uliweb.utils.generic import DetailView
        Workflow = functions.get_workflow()

        obj = self.model.get(int(id))

        workflow = Workflow.load(obj._workflow_, operator=request.user)

        view = DetailView(self.model, obj=obj)
        result = view.run()

        data = {
            'detailview': result['view'],
            'obj': result['object'],
            'workflow': workflow,
            'task_desc': None,
        }


        if workflow.is_running():
            tasks = workflow.get_active_tasks()
            if len(tasks) == 1:
                next_tasks = tasks[0].get_next_tasks()
                data.update({
                    'show_deliver_form':True,
                    'deliverform': get_yesno_form(tasks[0], next_tasks),
                    'task_desc': tasks[0].get_desc(),
                    'task_name': tasks[0].get_name(),
                })
            else:
                data.update({
                    'show_deliver_form':False,
                })
        else:
            data.update({'show_deliver_form': False})

        return data

    def deliver(self, id):

        Workflow = functions.get_workflow()
        obj = self.model.get(int(id))
        workflow = Workflow.load(obj._workflow_, operator=request.user)

        if workflow.is_running():
            tasks = workflow.get_active_tasks()
            if len(tasks) == 1:
                task_id = tasks[0].get_unique_id()
                next_tasks = tasks[0].get_next_tasks()

                from_task_id = request.POST.get('from_task_id')
                if from_task_id != task_id:
                    return json({'success': False, 'message': '无效的标识，请求的活动可能已经被他人流转。'})

                trans_message = request.POST.get('trans_message', '')
                to_task = request.POST.get('to_task', None)
                if not to_task:
                    return json({'success': False, 'message': '无效的请求，您没有指定需要流转的流向。'})

                tasks[0].deliver(trans_message, next_tasks=[to_task], async=False)

                obj.approve_result = to_task
                obj.approver = request.user.id
                obj.approver_date =  datetime.datetime.now()

                obj.save()

                workflow.run()

            return json({'success': True})
        else:
            return json({'success': False, 'message': '无效的请求，请求的活动可能已经被他人流转。'})




