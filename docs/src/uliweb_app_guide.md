
# 在Uliweb app中使用 `redbreast`

redbreast包，目前包括了五个app：

* `redbreast.core`
    - 工作流核心代码
    - 作为uliweb app使用时，支持spec保存到数据库
    - 提供uliweb命令 clearspec, syncspec, reloadspec

* `redbreast.middleware`
    - 提供对工作流实例对象的序列化支持
    - 支持通过uliweb settings方式，配置spec的事件响应

* `redbreast.moniter`
    - 提供一个简单基于plugs的流程监控页面，缺省超级用户可用。

* `redbreast.ui`
    - ui相关代码，目前只提供一个显示流转意见的模板页。

* `redbreast.daemon`
    - 提供几个uliweb命令: daemon, daemon-client。用来创建后台跑批运行工作流的守护。
    
## 配置

首先，在uliweb的settings中增加我们使用到的app

    INSTALLED_APPS = [
        #------ redbreast -----------------------
        'redbreast.core',
        'redbreast.middleware',
        'redbreast.ui',
        'redbreast.daemon',
        'redbreast.moniter',
    ]

## 放置spec文件

缺省的情况下，我们可以把spec文件放置到任何一个app的workflow_specs目录下，文件扩展名称为spec。如果你个人有特别的位置要求，需要覆盖下面的settings配置项：

    [REDBREAST]
    SPEC_SUFFIX = '.spec'
    SPEC_DIR    = 'workflow_specs'

一般情况下，一个spec文件只配置一个工作流定义。

定义好之后，我们需要使用下面的命令，解析所有spec文件到数据库中。

    uliweb syncspec

另外两个命令，clearspec, reloadspec 分别是清空解析结果和清空后重新解析。
syncspec 只是增量的解析，不会清除原有的记录，只有同名的 TaskSpec 和 WorkflowSpec 会被更新。

## 使用工作流

redbreast只负责工作流程的流转部分，实际的工作中，一个流程可能涉及到人员权限，额外的数据表读书等等，这些数据都不包话的流程引擎之中的。

我们使用YesNoDemo来简单说明一下，怎么在代码中使用工作流。

首先，YesNoWorkflow.spec是一个很简单的流程，如下：

    task CreateTask:
        class : simple_task
        automatic: True
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
    workflow YesNoWorkflow:
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

有四个结点，除了ApproveTask是手动结点，其他结点都是自动的(automatic)。
流程发起者，创建流程，调用run()，会停到ApproveTask结点上，用户选择Yes还是No，流程结束。

我们这里假设用户是对一个内容(content)进行YesNo流程的操作。简单创建一个用户表，如下：

    class YesNo(Model):
      content         = Field(TEXT, verbose_name='内容', required=True)
      submitter       = Reference('user', verbose_name='提交人')
      submitter_date  = Field(datetime.datetime, verbose_name='提交时间')
      approver        = Reference('user', verbose_name='审核人')
      approver_date   = Field(datetime.datetime, verbose_name='审核时间')
      approve_result  = Field(str, max_length=100, verbose_name="审核结果")
      workflow        = Reference('workflow', verbose_name='关联工作流', collection_name='yesno')

数据表只有 content 是用于审批，其他字段都是记录操作者和操作时间。

workflow字段，构造了一个用户数据表和工作流实例记录表之间的交叉引用。

接下来，我们可以使用我们熟知的 AddView, EditView, DetailView 来读写这个表的数据，创建UI。这些都是常规。我们需要在关键的一些位置，把工作流的代码插入进去。

### 启动流程

我们选择在 AddView 的 post_save 方法中启动工作流，相当于用户数据表内容保存完整，可以进行审批了。代码如下：

```
    def post_save(obj, data):
        # import 
        from redbreast.middleware import Workflow, Task

        # create workflow
        workflow = Workflow.create("YesNoWorkflow", operator=request.user)

        # set ref_unique_id for cross reference
        workflow.ref_unique_id = "yesno,%d" % obj.id

        workflow.start()
        workflow.run()
        # cross reference
        obj.workflow = workflow.get_id()
        obj.save()
```

几点说明：

 * Workflow对象是来自 redbreast.middleware, 而不是之前的 redbreast.core, 前者有数据库的支持，任务工作流状态的变化，会插入或者更新相关的数据库记录。
 * ref_unique_id 用来形成工作流反查数据表的唯一标识，字符串类型

### 流转

这里的流转，只有简单的Yes，No两个流向，我们可以创建一个Form和两个按钮来展现这个界面，加上一个填写意见的文本框，用于在流转上记录下操作的说明。代码这里省略了。我们看一下，用户点了按钮之后，工作流怎么操作的？

```
    # 恢复工作流状态，obj上记录了工作流的id
    workflow = Workflow.load(obj._workflow_, operator=request.user)

    if workflow.is_running():
        # 获得当前active的结点
        tasks = workflow.get_active_tasks()
        # to_task = “Yes” or "No"
        tasks[0].deliver(trans_message, next_tasks=[to_task], async=False)

        # 结束流程
        workflow.run()
```

说明：

 * Workload.load用于从数据库中根据保存的记录，恢复工作流状态，与Workload.create相对。
 * get_active_tasks() 获流工作流上所有的ACTIVE结点。
 * 找到当前的活动结点，执行deliver方法，传入流转消息和下一个结点（如果没有分支，next_tasks参数可以省略。）async 告诉引擎是同步还是异步执行。如果是异步的话，我们还需要启到一个daemon来执行具体的流转逻辑。

### 事件绑定

一般我们通过 workflow 的事件绑定来基于回调形式处理一些工作流之外的事务。相当于把我们的逻辑插入到工作流的合适的位置上去。除了之前我们介绍的传统的事件订阅的方式。

我们还可以使用settings的配置来进行工作流的事情绑定，比如：

```
[REDBREAST_BINDS]
# Format
# bind_name = 'spec_name', 'event_type_name', 'func'
log_every_event = '*', '*', 'dashboard.workflow_log_handler'
```

这句话，是说所有的工作流的所有事件，都交给函数workflow_log_handler来处理。
我们当然也可以定制的写上具体的事件名称和工作流名称，

对于spec_name，我们支持下面几种形式: 具体的名称, 星号和问号通配置符。
\* 表示任何多的字符或者空, ?表示任一字符。

下面的示例都是可以的：Yes*, Yes??Workflow, YesNoWorkflow

event_type_name，只支持’*’（全部事件）和具体事件（如executed）的名称，不支持通配符。

### 异步执行引擎

异步执行引擎被封装成为一个uliweb的command命令。如下：

    uliweb daemon workflow_engine

目前引擎的逻辑处理是，读取数据库中工作流所有READY的结点，恢复工作流状态，执行流转操作。


## ApproveDemo 说明

### 数据初始化

```
 uliweb reset
 uliweb syncspec
 uliweb dbinit

```

前三个命令分别是：初始化数据库表；解析spec文件并同步到数据库；初始化测试用户。

测试用户如下：
  
  * admin, 管理员, 超级用户，wf_all
  * zhang3，张三，wf_create
  * li4, 李四, wf_create
  * wang5, 王五, wf_create
  * test1, 组内评审员, wf_group
  * test2, 部门管理员, wf_depart
  * boss1, 分管领导, wf_manager
  * boss2, 大领导, wf_boss
  * test3, 审核员, wf_checker
  * test4, 归档员, wf_archiver

密码都为1，最后一个值为所属角色。

### 运行系统

    uliweb runserver -p 8000
    uliweb daemon workflow_engine

加载网站在8000端口，加载工作流守护进程。
然后可以用浏览器打开`http://localhost:8000`查看效果。

### 代码片断

* 创建工作流

```
    workflow = Workflow.create("ApproveWorkflow", operator=user)
    workflow.start()
    workflow.get_id() # ID in database
```

* 基于数据库恢复工作流

```
Workflow.load(datebase_id, operator=user)
```

* 流转

```
    tasks = workflow.get_active_tasks()
    next_tasks = task.get_next_tasks()

    workflow.deliver(task.uuid, message=message, 
        next_tasks=next_tasks, async=False)
```


or 

```
task.deliver(message=message, next_tasks=next_tasks, async=True)
```
