from redbreast.core.spec import CoreWFManager, DONE
from redbreast.core import Task, Workflow

from redbreast.core.spec import AutoJoinTask, AutoSimpleTask

class Simple(AutoSimpleTask):
    
    def default_execute(self, task, workflow):
        print task.get_spec_name()
        print [t.get_spec_name() for t in task.parents]

        return DONE

class JoinTask(AutoJoinTask):

    def default_execute(self, task, workflow):
        print task.get_spec_name()
        print [t.get_spec_name() for t in task.parents]

        return DONE

def main():
    def event_log(event):
        print " -> spec %s, %s" % (event.task.get_name(), event.type)

    CoreWFManager.reset()
    workflow_spec = CoreWFManager.get_workflow_spec('SplitWorkflow')
    workflow_spec.on("executed", event_log)
    workflow_spec.on("enter", event_log)
    workflow_spec.on("ready", event_log)
    workflow_spec.on("completed", event_log)
    workflow = Workflow(workflow_spec)
    workflow.start()
    workflow.run()       

if __name__ == '__main__':
    main()
