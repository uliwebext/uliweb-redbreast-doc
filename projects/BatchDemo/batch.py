from redbreast.core.spec import CoreWFManager
from redbreast.core import Task, Workflow

def event_log(event):
    print " -> spec %s, %s" % (event.task.get_name(), event.type)

workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow')
workflow_spec.on("executed", event_log)

workflow = Workflow(workflow_spec)
workflow.start()
workflow.run()
        
