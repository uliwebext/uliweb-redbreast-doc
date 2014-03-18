# 快速上手之BatchDemo示例

这一章里，我们通过一点一点的修改 `BatchDemo` 例子，来了解一下`redbreast`中最基本的函数和用法。`BatchDemo` 是一个简单的 Python 程序，定义一个工作流，
完成一系列的任务。使用`redbreast`来加载各个任务，完成一个统一的流程。

## 定义流程 ##

我们先设想一个使用的场景，一个批处理的事情，可以分成四步来做，根据需要，我们可以定义如下的流程：

        
    task S1:
    end
    
    task S2:
    end
    
    task S3:
    end
    
    task S4:
    end
    
    workflow BatchWorkflow01:
    	flows:
    		S1 -> S2 -> S3 -> S4
    	end
    end

    
这里，我们定义了四个任务(`S1`,`S2`,`S3`,`S4`)，这四个任务都是简单结点，目前还没有定义实际任务功能，我们这里没有给每个task指定class，缺省的使用的是`redbreast.core.spec.AutoSimpleTask`，是一个自动向下流转的简单结点。

同时，我们也定义了一个工作流，名称为`BatchWorkflow01`。
流向的定义，就是顺序执行每个结点。

最后，我们把工作流的定义，保存到文件`BatchWorkflow01.spec`中。

## 撰写代码 ##

首先，需要模块引入

	from redbreast.core.spec import CoreWFManager
	from redbreast.core import Task, Workflow

我们引入了这样几个对象:

 * `CoreWFManager` 
 
 全局唯一的对象，用于管理工作流定义，缺省的存储storage使用的是从当前脚本的spec子目录下读取.spec文件来加载工作流定义(要求工作流的名称和保存的文件名是一致的)。在后面的例子中，如果我们按照uliwebapp的方式引入redbreast的包之后，缺省的storage则会是数据库。

 * `Task`, `Workflow`
 
 活动实例和工作流实例对象。在运行中，我们会根据刚刚定义的工作流来生成这些对象。

加载工作流定义

	workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow01')

事件绑定，这里只是在各个任务执行的时候，输出一句日志。
	
	def event_log(event):
    	print " -> spec %s, %s" % (event.task.get_name(), event.type)
    
	workflow_spec.on("executed", event_log)

实例化，启动工作流，运行之（run函数会重复执行到需要人工干预的结点为止，对于我们的流程，没有选择结点，都是自动流转结点，会一直执行到流程结束）

	workflow = Workflow(workflow_spec)
	workflow.start()
	workflow.run()

最后的运行结果如下：

	-> spec S1, task:executed
	-> spec S2, task:executed
	-> spec S3, task:executed
	-> spec S4, task:executed

## 增加逻辑 ##

### 怎么增加逻辑代码 ###

下面，通过几种方式，在各个任务中，增加我们自己的业务逻辑。

方法一，直接在spec中定义，适合于一些简单逻辑，修改task_spec:S1如下

    task S1
        code execute:
            print "Task S1 executed, defined in task"
            print task
            print workflow
            return DONE
        end
    end

或者修改workflow_spec如下：

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

我们可以在task_spec或者workflow_spec中直接定义简单的execute代码，返回值DONE是表示通知工作流继续执行transfer到下一个结点的操作。代码的上下文中缺省的包括两个参数task, workflow, 分别是当前的任务实例和工作流实例。如果task_spec, workflow_spec中都定义了某个任务的代码，workflow_spec 中定义的代码，有更高的优先级。

如果我们的逻辑很复杂，就不适合在此处直接撰写了。我们可以去增加一个新的TaskSpec类来做这个事。

方法二，使用自定义的TaskSpec类，重写default_execute方法，示例如下：

```
from redbreast.core.spec import AutoSimpleTask
from redbreast.core.spec import DONE

class CustomTask(AutoSimpleTask):
    def default_execute(self, task, workflow):
        print "Task %s executed, defined in CustomClass."%task.get_spec_name()
        return DONE
```

然后修改spec文件中的task_spec:S3的任务如下：

    #第三步
    task S3:
        class : mytask.CustomTask
    end

最终程序的输出结果是这样的：

```
Task S1 executed, defined in task
<Task (S1) in state READY at 0x1fc6090>
<redbreast.core.workflow.Workflow object at 0x01FC6A30>
Task S2 executed, defined in process
Task S3 executed, defined in CustomClass.
```

这几种方法的优先级是这样的，workflow_spec定义最高，task_spec定义其次，类中的default_execute最次，如果有几种定义都存在，只有优先级高的会被执行，其他的就被忽略了。

### 怎么在工作流任务间中保留和传递数据

有些时候，两步任务之间，会需要有一些数据交换，在redbreast中如何实现呢？

数据定义有两种方式，一种是直接定义在spec文件中，比如直接写到task_spec里或者 workflow_spec，如下面的d1，d2, d3。这些数据会在所有的同一个spec生成的工作流之间共享，适用于一些配置项，固定参数之类，只读为主。如果某个工作流修改了其中的数据。其他的工作流访问时也会得到新的数据。另一种，是在运行的代码中，通过set_data存储到task或者workflow的实例中去（这种数据只会影响。我们可以根据运行态的数据不同，写入不同的数据。

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
    ...
    #批处理
    workflow BatchWorkflow03:
        d3 : data3
        ...
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

使用的方法如下：

* 第一种数据
 - 任务实例, 读：get_spec_data(key)，写：set_spec_data(key, value)
 - 工作流实例，读：get_spec_data(key)，写：set_spec_data(key, value)

* 第二种数据
 - 任务实例, 读：get_data(key)，写：set_data(key, value)
 - 工作流实例，读：get_data(key)，写：set_data(key, value) 

### 更复杂的例子，一个有分支流向的示例

有了数据的传递，我们就可以在运行态中修改工作流的走向，下面我们来定义一个有简单分支的工作流，有两条分支，运行中，随机选择一条路径来走。

首先，定义spec如下：

```
    #第一步
    task S1:
        class: AutoChoiceTask
    end

    #第二步，分支A
    task A:
        code execute:
            workflow.set_data("flow", "A")
            return DONE
        end
    end

    #第二步，B
    task B:
        default: True
        code execute:
            workflow.set_data("flow", "B")
            return DONE
        end
    end

    #第三步
    task S2:
    end

    workflow ChoiceWorkflow01:

        flows:
            S1 -> A -> S2
            S1 -> B -> S2
        end

    end
```

几点说明，分支选择结点，类选择为AutoChoiceTask，缺省的情况下，这个任务会根据用户设置在task实例上的next_tasks来选择流向进行流转。分成如下几种情况：

* next_tasks 包含唯一流向，比如 ["A"], 选择流向"A"
* next_tasks 包含多于一个流向，抛出异常
* next_tasks 为空，spec中定义了default流向，选择流向"B"
* next_tasks 为空，spec中未定义缺省流向，选择第一分支，选择流向"A"

我们可以修改spec中的S1定义，加上随机选择流向的代码， 如下：

```
    #第一步
    task S1:
        class: AutoChoiceTask
        code execute:
            from random import randint
            flow = ["A", "B"]
            task.set_next_tasks(flow[randint(0,1)])
            return DONE
        end
    end
```

也可以采用重定义类的方式，如下：

```
class RandomTask(AutoChoiceTask):

    def default_choose(self, task, workflow):
        from random import randint
        flow = ["A", "B"]
        return flow[randint(0, 1)]
```

这里，我们并没有定义default_execute, 而是定义了AutoChoiceTask的default_choose方法，缺省的default_choose 就是我们上面提及的逻辑，会读取next_tasks的返回值，你在这里覆盖缺省行为，可以直接返回流向名称。

完整的程序见
projects/BatchDemo/choise.py, 

流程定义文件为
projects/BatchDemo/spec/ChoiceWorkflow01.spec
projects/BatchDemo/spec/ChoiceWorkflow02.spec

### 更多的例子
我们可以在BatchDemo中找到更多的例子：

并行结点
project/BatchDemo/split.py 

多选分支
project/BatchDemo/multi.py