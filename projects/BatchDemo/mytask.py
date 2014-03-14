from redbreast.core.spec import AutoSimpleTask
from redbreast.core.spec import DONE

class CustomTask(AutoSimpleTask):

    def default_execute(self, task, workflow):
        print "Task %s executed, defined in CustomClass." % task.get_spec_name()
        return DONE