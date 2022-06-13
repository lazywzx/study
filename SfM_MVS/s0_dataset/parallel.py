import threading, time, queue
from ..s0_dataset import log


def parallel_map(func, items, max_workers=1):
    """
    parallel process map

    :param func:
    :param items:
    :param max_workers:
    :param single_thread_fallback:
    """
    exitFlag = 0

    class myThread(threading.Thread):
        def __init__(self, threadID, name, q):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q

        def run(self):
            log.logINFO("Start thread: " + self.name)
            process_data(self.q)
            log.logINFO("Exit thread: " + self.name)

    def process_data(q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                pathdict = q.get()
                queueLock.release()
                func(pathdict)
            else:
                queueLock.release()
            time.sleep(1)

    queueLock = threading.Lock()
    workQueue = queue.Queue(int(len(items) * 1.5))

    threads = []
    threadID = 1
    for t in range(max_workers):
        tname = "Thread-" + str(t)
        thread = myThread(threadID, tname, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for word in items:
        workQueue.put(word)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    log.logINFO("Parallel process done!")
