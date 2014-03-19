



## ApproveDemo 说明

### 数据初始化

```
 uliweb reset
 uliweb syncspec
 uliweb dbinit

 uliweb runserver -p 8000
```

前三个命令分别是：初始化数据库表；解析spec文件并同步到数据库；初始化测试用户。
然后可以用Chrome打开`http://localhost:8000`查看效果。

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

### 代码片断解说

