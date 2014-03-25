
def get_approve_obj(id):
    from uliweb.orm import get_model
    Approve = get_model('approve')
    return Approve.get(int(id))

def workflow_task_enter(event):
    from uliweb.orm import get_model

    if hasattr(event, 'workflow'):
        wf = event.workflow
        if not wf.deserializing:

            ref_unique_id = wf.ref_unique_id
            obj_id = ref_unique_id.split("-")[1]
            obj = get_approve_obj(obj_id)
            if obj:
                obj.task_spec_desc = event.task.get_desc()
                obj.task_spec_name = event.task.get_name()
                obj.save()

def workflow_running(event):
    if hasattr(event, 'workflow'):
        pass

def workflow_finished(event):
    if hasattr(event, 'workflow'):
        pass