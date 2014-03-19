task CreateTask:
    class : simple_task
end

task ApproveTask:
    class : choice_task
end

task YesTask:
    class : simple_task
    automatic: True
end

task NoTask:
    class : simple_task
    automatic: True
end

process YesNoTask:
    tasks:
        CreateTask  as C
        ApproveTask as A
        YesTask     as Yes
        NoTask      as No
    end

    flows:
        
        C -> A -> Yes
             A -> No
    end

end
