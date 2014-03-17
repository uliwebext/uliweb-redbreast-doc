    #第一步
    task S1:
        class: choice.RandomTask
    end

    #第二步，分支A
    task A:
        code execute:
            #print "A"
            workflow.set_data("flow", "A")
            return DONE
        end
    end

    #第二步，B
    task B:
        default: True
        code execute:
            #print "B"
            workflow.set_data("flow", "B")
            return DONE
        end
    end

    #第三步
    task S2:
    end

    workflow ChoiceWorkflow02:

        flows:
            S1 -> A -> S2
            S1 -> B -> S2
        end

    end
