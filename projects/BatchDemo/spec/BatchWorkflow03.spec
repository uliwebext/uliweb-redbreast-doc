    #第一步
    task S1:
        d1 : s1-d1
        d2 : s1-d2
        code execute:
            print "Task S1 executed, defined in task"
            print "  > d1 from task_spec:%s" % task.get_spec_data("d1")
            print "  > d2 from task_spec:%s" % task.get_spec_data("d2")
            print "  > d3 from workflow_spec:%s" % workflow.get_spec_data("d3")

            task.set_data("c1", "s1-c1")
            workflow.set_data("c2", "s1-c2")
            return DONE
        end
    end

    #第二步
    task S2:
        d1 : s2-d1
    end

    #第三步
    task S3:
        class : mytask.CustomTask
    end

    #第四步
    task S4:
    end

    #批处理
    workflow BatchWorkflow03:

        d3 : data3

        #流向定义
        flows:
            S1 -> S2 -> S3 -> S4
        end

        code S2.execute:
            print "Task S2 executed, defined in process"
            print "  > d1 from task_spec:%s" % task.get_spec_data("d1")
            print "  > d2 from task_spec:%s" % task.get_spec_data("d2")
            print "  > d3 from workflow_spec:%s" % workflow.get_spec_data("d3")

            print "  > c1 from task-S1:%s" % task.parents[0].get_data("c1")
            print "  > c2 from workflow:%s" % workflow.get_data("c2")

            return DONE
        end

    end
