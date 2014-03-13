# 介绍

## 安装
  
    git clone https://github.com/Longwosion/uliweb-redbreast.git
    cd uliweb-redbreast
    python setup.py install

## 独立使用

    from redbreast.core.spec import CoreWFManager
    from redbreast.core import Task, Workflow
    
    workflow_spec = CoreWFManager.get_workflow_spec('Workflow')
    
    workflow = Workflow(workflow_spec)
    workflow.start()
    workflow.run()

## Uliweb中使用

在settings中增加:

    INSTALLED_APPS = [
        #------ redbreast -----------------------
        'redbreast.core',
        'redbreast.middleware',
        'redbreast.ui',
        'redbreast.daemon',
        'redbreast.moniter',
    ]





