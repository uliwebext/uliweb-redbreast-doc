    #第一步
    task S1:
        class: AutoChoiceTask
        code execute:
            print "aaaa"
            task.set_next_task("A")
            return DONE
        end
    end

    #第二步，分支A
    task A:
        code execute:
            print "flow A"
            return DONE
        end
    end

    #第二步，B
    task B:
        default: True
        code execute:
            print "flow B"
            return DONE
        end
    end

    #第三步
    task S2:
    end

    workflow BatchWorkflow04:

        flows:
            S1 -> A -> S2
            S1 -> B -> S2
        end

    end
