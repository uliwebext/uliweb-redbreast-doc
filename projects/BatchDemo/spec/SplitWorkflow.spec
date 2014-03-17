task S1:
    class: AutoSplitTask
end

task A:
    class: split.Simple
end

task B:
    class: split.Simple
end

task S2:
    class: split.JoinTask
end

workflow SplitWorkflow:

    flows:
        S1 -> A -> S2
        S1 -> B -> S2
    end

end
