# 快速上手

## BatchDemo示例 ##
这一篇文章里，我们通过一点一点的修改 `BatchDemo` 例子，来了解一下`redbreast`中基本的函数和用法。`BatchDemo` 是一个简单的 Python 程序，定义一个工作流，
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
    
    process BatchWorkflow01:
    	flows:
    		S1 -> S2 -> S3 -> S4
    	end
    end

    
这里，我们定义了四个任务(`S1`,`S2`,`S3`,`S4`)，这四个任务都是简单结点，目前还没有定义实际任务功能，我们这里没有给每个task指定class，缺省的使用的是`redbreast.core.spec.AutoSimpleTask`，是一个自动向下流转的简单结点。

同时，我们也定义了一个工作流，名称为`BatchWorkflow01`。
流向的定义，就是顺序执行每个结点。

最后，我们把工作流的定义，保存到文件`BatchWorkflow01.spec`中。

## 撰写代码 ##

模块引入

	from redbreast.core.spec import CoreWFManager
	from redbreast.core import Task, Workflow

我们需要引入这样几个对象:

 * `CoreWFManager` 
 
 全局唯一的对象，用于管理工作流定义，缺省的存储storage使用的是从当前脚本的目录下读取.spec文件来加载工作流定义。在后面的例子中，如果我们按照uliwebapp的方式引入redbreast的包之后，缺省的storage则会是数据库。

 * `Task`, `Workflow`
 
 活动实例，和工作流实例对象。在运行中，我们会根据刚刚定义的工作流来生成这些对象。

加载工作流定义

	workflow_spec = CoreWFManager.get_workflow_spec('BatchWorkflow01')

事件绑定，我们只是在各个任务执行的时候，输出一句日志。
	
	def event_log(event):
    	print " -> spec %s, %s" % (event.task.get_name(), event.type)
    
	workflow_spec.on("executed", event_log)

实例化，启动工作流，运行之（run函数会执行到需要人工干预的结点为止，对于我们的流程，没有选择结点，都是自动流转结点，会一直执行到结束）

	workflow = Workflow(workflow_spec)
	workflow.start()
	workflow.run()

最后的运行结果如下：

	-> spec S1, task:executed
	-> spec S2, task:executed
	-> spec S3, task:executed
	-> spec S4, task:executed

## 增加逻辑 ##

下面，我们通过几种方式，在各个任务中，增加我们自己的业务逻辑。

方法一，直接在spec中定义，适合于一些简单逻辑，修改S1如下

    task S1
        
