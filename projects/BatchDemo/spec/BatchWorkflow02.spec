    #第一步
    task S1:
        code execute:
            print "Task S1 executed, defined in task"
            print task
            print workflow
            return DONE
        end
    end

    #第二步
    task S2:
    end

    #第三步
    task S3:
        class : mytask.CustomTask
    end

    #第四步
    task S4:
    end

    #批处理
    workflow BatchWorkflow02:
        #流向定义
        flows:
            S1 -> S2 -> S3 -> S4
        end

        code S2.execute:
            print "Task S2 executed, defined in process"
            return DONE
        end

    end
