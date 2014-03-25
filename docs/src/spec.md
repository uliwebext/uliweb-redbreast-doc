# 工作流定义文件格式

这一章里，我们介绍redbreast中的spec文件格式，即工作流定义文件格式。

## 数据需求

工作流的定义分成如下几部分：

* 工作流(Workflow)基本信息描述
    - 工作流名称 name
    - 描述 desc
 
* 工作流任务(Task)列表
    - 工作流上的任务列表。每个任务需要有一个唯一的标识（名称）
    - 任务的定义支持下面的字段：
        + name, 任务名称
        + class, 任务关联类名，比如 AutoSimpleTask, AutoJoinTask之类，
            如果是用户自定义的类，需要写全路径。比如my.path.EmailTask
        + desc, 任务描述
        + automatic [True, False], 是否自动流转结点
        + default [True, False], 是否是缺省流向（适用于分支选择）
        + 其他附加的属性(key:value对)，运行时，可以用get_spec_data(key)方法读取。

* 工作流流向(Flow)定义
    - 采用符号化的形式定义结点与结点之间的关系，
    - 如 A->B->C 表示A是B结点的输入结点，B是C的输入结点。
    - 支持多行定义，-> 前后可以包含空格。

* 工作流任务自定义逻辑代码
    - 简单逻辑时，不需要继承子类，只需在spec文件中增加一点代码就可以。
    - ready，状态从ACTIVE变成READY时调用。
    - execute，状态从READY变成EXECUTED调用。
    - choose，多选，分支任务，状态从READY变成EXECUTED前调用。
  

## 流向定义示例

如下图的工作流，

<img src="img/figure01.svg"/>

我们可以采用多种形式来定义，一种是链式，一次定义多个关系：

    A -> B -> C -> G -> H
    A -> D -> E -> F -> G

或者每行只定义一个流向，如下：
    
    A -> B
    A -> D
    B -> C
    C -> G
    D -> E
    E -> F
    F -> G
    G -> H


## 配置文件格式

spec文件的格式类似于写一个Python的类 (缩进形式，关键字 workflow, task, flow…)，
在一个文件中定义只一个工作流，并且工作流的名称最好与文件名称保持一致。

### Task

先定义该工作流中用到各个Task, 一个Task一个块，以task关键字开头，end关键字结束。如下：

```
# 定义Task
task TaskName:
"""Task Desc"""
    class : AutoSimpleTask
    default: True
    key1: val1
    key2: val2
    code ready:
        print "ready"
        return YES
    end
end
```

说明：

 * `#`号开头的行为注解
 * task 后面定义该任务的名称，实例化之后，为object上的name属性
 * `"""`或者`'''`对中包含的文字为desc定义，实例后化为object上的desc属性
 * 普通的值都用kev:value形式定义
 * 代码块，使用code [code_name]: ... end形式定义。
    - 中间部分为合法的python代码
    - 上下文可访问对象有task, workflow, 分别是运行态下当前任务实例和工作流实例
    - 上下文可访问常量有：YES, NO, DONE, DOING
    - ready代码块，返回值要求YES，NO，表示是否同意转换到READY状态
    - execute代码块，返回值要求DONE，DOING，NO，表示是否同意转换到EXECUTED状态或者EXECUTING状态。
    - choose代码块，返回值为数组对象，为欲流转分支任务名称列表。

### Workflow
Workflow的定义分成三块，第一块是基本属性，第二块是别名定义，第三块是流向定义。

```
# 我的工作流
workflow MyWorkflow:
    '''
    My 1st workflow spec
    '''

    #基本属性
    k1 : value1
    k2 : value2

    #别名定义
    tasks:
        CreateApproveTask   as Create
        GroupApproveTask    as Group
        DepartApproveTask   as Depart
        ManagerApproveTask  as Manager
        BossApproveTask     as Boss
        CheckerTask         as Checker
        ArchiverTask        as Archiver
    end

    # 流向定义
    flows:
        # 流向可以分成多行
        Create -> Group -> Depart
            Depart -> Manager -> Checker
            Depart -> Boss -> Checker
        Checker -> Archiver
    end

    code Create.ready:
        print "ready"
    end

end   
```

说明：

* `#`号开头的行为注解
* workflow或者process 后面定义该工作流的名称，实例化之后，为object上的name属性
* `"""`或者`'''`对中文字为desc定义，实例后为object上的desc属性
* 普通的值都用kev:value形式定义
* tasks: end块定义任务别称，两个作用，一个简单化flows部分的定义, 另外一个，如果多个任务结点使用同一份Task的定义，一定需要别名不同，用于在flows定义时区分。
* 未定义别名的task, 直接使用task的name
* 代码块，使用taskname.code [code_name]: ... end形式定义, 优先级比task中定义的高。其他情况同上。
