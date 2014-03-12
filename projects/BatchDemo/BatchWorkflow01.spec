task Step1Task:
"""Step One"""
    class : SimpleTask
end

task Step2Task:
"""Step Two"""
    class : SimpleTask
end

task Step3Task:
"""Step Three"""
    class : SimpleTask
end

task Step4Task:
"""Step Four"""
    class : SimpleTask
end

process BatchWorkflow01:
    tasks:
        # Alias
        Step1Task   as S1
        Step2Task   as S2
        Step3Task   as S3
        Step4Task   as S4
    end

    flows:
        S1 -> S2 -> S3 -> S4
    end

end
