    #第一步
    task S1:
    end

    #第二步
    task S2:
    end

    #第三步
    task S3:
    end

    #第四步
    task S4:
    end

    #批处理
    workflow BatchWorkflow01:
        #流向定义
        flows:
            S1 -> S2 -> S3 -> S4
        end
    end
