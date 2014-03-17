from redbreast.core.spec import CoreWFManager, AutoChoiceTask, DONE
from redbreast.core import Task, Workflow


class RandomTask(AutoChoiceTask):

    def default_choose(self, task, workflow):
        from random import randint
        flow = ["A", "B"]
        return flow[randint(0, 1)]

def main():

    def event_log(event):
        print " -> spec %s, %s" % (event.task.get_name(), event.type)
    
    CoreWFManager.reset()
    workflow_spec = CoreWFManager.get_workflow_spec('ChoiceWorkflow01')

    count = [0, 0]
    for i in range(0, 100):
        workflow = Workflow(workflow_spec)
        workflow.start()
        workflow.run()       

        flow = workflow.get_data("flow")
        if flow == "A":
            count[0] = count[0] + 1
        else:
            count[1] = count[1] + 1

    print "flow A: %d" % count[0]
    print "flow B: %d" % count[1]

if __name__ == '__main__':
    main()
