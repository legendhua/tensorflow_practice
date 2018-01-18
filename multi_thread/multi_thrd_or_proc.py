# -*- coding: utf-8 -*-
import os, time, random, threading
import subprocess
from multiprocessing import Process, Pool, Queue


# python中多进程、多线程学习
#------------第一部分：多进程 multiprocessing-----------

def do_fork():
    # Unix/Linux操作系统提供了一个fork()系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，
    # 但是fork()调用一次，返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），
    # 然后，分别在父进程和子进程内返回。
    # 子进程永远返回0，而父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，
    # 父进程要记下每个子进程的ID，而子进程只需要调用getppid()就可以拿到父进程的ID。
    print('Process (%s) start...' & os.getpid)
    # only works on Unix/Linux/Mac
    pid = os.fork()
    if pid == 0:
        print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
    else:
        print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

def multi_processing():
    # multiprocessing模块就是跨平台版本的多进程模块。
    # multiprocessing模块提供了一个Process类来代表一个进程对象，下面的例子演示了启动一个子进程并等待其结束
    # 子进程要执行的代码
    def run_proc(name):
        print('Run child process %s (%s)...' % (name, os.getpid()))
    
    print('Parent process %s.' % os.getpid())
    # 创建子进程时，只需要传入一个执行函数和函数的参数
    # 创建一个Process实例，用start()方法启动
    # join()方法可以等待子进程结束后再继续往下进行，通常用于进程间的同步
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')

# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程
def pooled_processing():
    def long_time_tast(name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name,(end-start)))
    
    print('Parent process %s.' % os.getpid())
    p = Pool(4) # 设置进程池为4，最多同时执行4个进程。默认大小是CPU的核数
    # 下面的程序会先执行前4个程序,然后再执行最后一个程序
    for i in range(5):
        p.apply_async(long_time_tast, args = (i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


# 很多时候，子进程并不是自身，而是一个外部进程。我们创建了子进程后，还需要控制子进程的输入和输出。
# subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出
def do_subprocess():
    # 代码中运行命令 nslockup www.python.org
    print('$ nslockup www.python.org')
    r = subprocess.call(['nslockup', 'www.python.org'])
    print('Exit code:', r)
    # 下面的代码相当于在命令行执行nslockup，然后手动输入：
    # set q=mx
    # python.org
    # exit
    print('$ nslockup')
    p = subprocess.Popen(['nslockup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('utf-8'))
    print('Exit code:', p.returncode)

# Process之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。
# Python的multiprocessing模块包装了底层的机制，提供了Queue、Pipes等多种方式来交换数据
def do_queue():
    # 以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据
    # 写数据进程执行的代码
    def write(q):
        print('Process to write； %s' % os.getpid())
        for value in ['A', 'B', 'C']:
            print('Put %s to queue...' % value)
            q.put(value)
            time.sleep(random.random())
    # 读数据进程执行的代码
    def read(q):
        print('Process to read: %s' % os.getpid())
        while True:
            value = q.get(True)
            print('Get %s from queue.' % value)
    
    # 主程序
    # 父进程创建Queue,并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入
    pw.start()
    # 启动子进程pr，读取
    pr.start()
    # 等待pw结束
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止
    pr.terminate()

# ---------------第二部分:多线程学习 multi_thread------------------
# Python的标准库提供了两个模块：_thread和threading，_thread是低级模块，
# threading是高级模块，对_thread进行了封装。绝大多数情况下，我们只需要使用threading这个高级模块
# 启动一个线程就是把一个函数传入并创建Thread实例，然后调用start()开始执行
def multi_threading():
    # 新线程执行的代码
    def loop():
        print('thread %s is running...' % threading.current_thread().name)
        n = 0
        while n < 5:
            n = n + 1
            print('thread %s >>> %s' % (threading.current_thread().name, n))
            time.sleep(1)
        print('thread %s ended' % threading.current_thread().name)
    
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)
# 由于任何进程默认就会启动一个线程，我们把该线程称为主线程，主线程又可以启动新的线程，
# Python的threading模块有个current_thread()函数，它永远返回当前线程的实例。主线程
# 实例的名字叫MainThread，子线程的名字在创建时指定，我们用LoopThread命名子线程。名字
# 仅仅在打印时用来显示，完全没有其他意义，如果不起名字Python就自动给线程命名为Thread-1，Thread-2……

def do_lock():
    # 假定这是你的银行存款
    balance = 0
    def change_it(n):
        # 先存后取，结果应该为0
        global balance
        balance = balance + n
        balance = balance - n

    def run_thread(n):
        for i in range(1000000):
            # 先要获取锁：
            lock.acquire()
            try:
                # 放心地改吧
                change_it(n)
            finally:
                # 改完了一定要释放锁
                lock.release()
    
    # 主程序
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)

if __name__ == '__main__':
    pooled_processing()