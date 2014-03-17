from redbreast.core.spec import CoreWFManager
from redbreast.core import Task, Workflow

def event_log(event):
    print " -> spec %s, %s" % (event.task.get_name(), event.type)

print "\n---- Workflow01 ------------------------------"
CoreWFManager.reset()
workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow01')
workflow_spec.on("executed", event_log)

workflow = Workflow(workflow_spec)
workflow.start()
workflow.run()
        
print "\n---- Workflow02 ------------------------------"
CoreWFManager.reset()
workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow02')

workflow = Workflow(workflow_spec)
workflow.start()
workflow.run()
        
print "\n---- Workflow03 ------------------------------"
CoreWFManager.reset()
workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow03')

workflow = Workflow(workflow_spec)
workflow.start()
workflow.run()       


