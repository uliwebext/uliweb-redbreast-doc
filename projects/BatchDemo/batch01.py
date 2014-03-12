from redbreast.core.spec import CoreWFManager
from redbreast.core import Task, Workflow
from os.path import dirname, join

def event_log(event):
    print " -> spec %s, %s" % (event.task.get_name(), event.type)

workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow01')
#workflow_spec.on("ready", event_log)
workflow_spec.on("executed", event_log)
#workflow_spec.on("completed", event_log)

workflow_spec.dump()

workflow = Workflow(workflow_spec)
print "---------START-------------------"
workflow.start()
workflow.run()
print "---------RUN-------------------"
workflow.task_tree.dump()
        
