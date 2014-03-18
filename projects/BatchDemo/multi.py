from redbreast.core.spec import CoreWFManager, DONE
from redbreast.core import Task, Workflow

from redbreast.core.spec import AutoMultiChoiceTask, AutoJoinTask, AutoSimpleTask

class MultiTask(AutoMultiChoiceTask):
    def default_choose(self, task, workflow):
        from random import randint
        flows = randint(1,3)
        next = ["A", "B", "C"]
        ret = []
        while len(ret) < flows:
            flow = next[randint(0,2)]
            if not flow in ret:
                ret.append(flow)
        return ret

class Simple(AutoSimpleTask):
    
    def default_execute(self, task, workflow):
        return DONE

class JoinTask(AutoJoinTask):

    def default_execute(self, task, workflow):
        flows = [t.get_spec_name() for t in task.parents]
        print flows
        workflow.set_data("flows", flows)
        return DONE

def main():
    CoreWFManager.reset()
    workflow_spec = CoreWFManager.get_workflow_spec('MultiChoiceWorkflow')

    count = [0, 0, 0]
    for i in range(0, 100):
        workflow = Workflow(workflow_spec)
        workflow.start()
        workflow.run()       

        flows = workflow.get_data("flows")
        for flow in flows:
            if flow == "A":
                count[0] = count[0] + 1
            elif flow == "B":
                count[1] = count[1] + 1
            elif flow == "C":
                count[2] = count[2] + 1

    print count

if __name__ == '__main__':
    main()
