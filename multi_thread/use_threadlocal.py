# -*- coding: utf-8 -*-
import threading
# 本文件介绍ThreadLocal的使用
# 在多线程环境下，每个线程都有自己的数据。一个线程使用自己的局部变量比使用全局变量好，
# 因为局部变量只有线程自己能看见，不会影响其他线程，而全局变量的修改必须加锁。

# 解决问题：多线程情况下，线程间的变量传递

# --------使用局部变量传递--------------
def local_para():
    def process_student(name):   # 单独的一个进程
        std = Student(name)   #局部变量std
        # std是局部变量，但是每个函数都要用它，因此必须传进去
        do_task_1(std)
        do_task_2(std)
    def do_task_1(std):
        do_subtask_1(std)
        do_subtask_2(std)
    def do_task_2(std):
        do_subtask_1(std)
        do_subtask_2(std)
# 问题：使用函数不停的传递参数很麻烦

# ----------定义全局dict----------------
# 用一个全局dict存放所有的Student对象，然后以thread自身作为key获得线程对应的Student对象
def global_para():
    # 先定义一个全局dict
    global_dict = {}

    def std_thread(name):
        std = Student(name)  # 局部变量std
        # 把std放到全局变量global_dict中
        global_dict[threading.current_thread()] = std
        do_task_1()
        do_task_2()
    def do_task_1():
        # 不传入std，而是根据当前线程查找
        std = global_dict[threading.current_thread()]
        # ...其余地方用std
    def do_task_2():
        # 不传入std，而是根据当前线程查找
        std = global_dict[threading.current_thread()]
        # ...
# 上述方案解决了在每层函数间参数传递的问题，但是代码有点丑

# --------------------threadlocal的方式-------------------------
def use_threadlocal():
    local_school = threading.local()  # 定义一个全局threadlocal对象
    def process_student():
        # 获取当前线程关联的student
        std = local_school.student
        print('Hello, %s (in %s)' % (std, threading.current_thread().name))

    def process_thread(name):
        # 绑定ThreadLocal的student
        local_school.student = name
        process_student()

    # 测试主程序
    t1 = threading.Thread(target=process_thread, args=('ZGH',), name='Thread-A')
    t2 = threading.Thread(target=process_thread, args=('abc',), name='Thread-B')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # 全局变量local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，
    # 但互不影响。你可以把local_school看成全局变量，但每个属性如local_school.student都是
    # 线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。
    # 理解为全局变量local_school是一个dict，不但可以用local_school.student，还可以绑定
    # 其他变量，如local_school.teacher等等.
    # ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，
    # 这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源