task S1:
    class: multi.MultiTask
end

task A:
    class: multi.Simple
end

task B:
    class: multi.Simple
end

task C:
    class: multi.Simple
end

task S2:
    class: multi.JoinTask
end

workflow MultiChoiceWorkflow:

    flows:
        S1 -> A -> S2
        S1 -> B -> S2
        S1 -> C -> S2
    end

end
