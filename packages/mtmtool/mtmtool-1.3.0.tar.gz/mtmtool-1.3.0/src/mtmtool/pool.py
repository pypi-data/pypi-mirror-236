from functools import partial, update_wrapper
from itertools import product
from mtmtool.log import stream_logger
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os, sys
from collections.abc import Callable, Generator
import dill


logger = stream_logger("MtmPool")

CPUNUM = os.cpu_count()

""" 
map 与 starmap 函数的区别:
    map只展开一次, 只能向函数掺入一个参数
    starmap可展开两次, 可以向函数传入多个参数
product 函数:
    输入多个可迭代参数, 返回所有笛卡尔积元组
"""


def pool_process(par_func, iterables, worker_num=CPUNUM):
    with Pool(worker_num) as p:
        res_list = p.map(par_func, iterables)
    return res_list


def pool_thread(par_func, iterables, worker_num=CPUNUM):
    with ThreadPool(worker_num) as p:
        res_list = p.map(par_func, iterables)
    return res_list


def starmap(func, *args, is_test=False, worker_num=None, ptype="Process"):
    """输入args必须可迭代
    usage:
        >>> result = starmap(pow, [10,15], [3,5], worker_num=4, ptype="Thread")
        >>> result
        [1000, 100000, 3375, 759375]
    """
    iters = product(*args)
    pool = Pool if ptype == "Process" else ThreadPool
    worker_num = CPUNUM if worker_num is None else worker_num
    if is_test:
        res = []
        for args_t in iters:
            res.append(func(*args_t))
    else:
        with pool(worker_num) as p:
            res = p.starmap(func, iters)
    return res


def is_mp_main():
    return sys.modules["__mp_main__"].__name__ == "__mp_main__"


class MapPool:
    def __init__(self, func:Callable=None, max_workers:int=None, pool_type:str="Thread", **kwargs) -> None:
        self.max_workers = max_workers # 最大worker数量
        self.buffer = [] # 任务缓冲区
        self.pool_type = pool_type # 进程池类型
        # 将函数序列化，以便在子进程中使用
        self.function_dill = dill.dumps(func)
        # 复制函数属性
        update_wrapper(self, func)
        self.__wrapped__ = self.function_dill
        

    def __call__(self, *args, **kwargs):
        workers = kwargs.get("workers", self.max_workers)
        if "workers" in kwargs:
            kwargs.pop("workers")        
        if workers is None:
            # 如果没有传入worker数量, 则像普通函数一样运行
            func = dill.loads(self.function_dill)
            return func(*args, **kwargs)
        else:
            # 如果指定了worker数量, 则将任务放入缓冲区
            self.buffer.append((args, kwargs))

    def worker_wrapper(self, arg:tuple, func:Callable=None):
        args, kwargs = arg
        if func is None or sys.modules["__mp_main__"].__name__ == "__mp_main__":
            # 如果是在子进程中, 则需要重新加载函数
            import dill
            if not hasattr(self, "_func"):
                self._func = dill.loads(self.function_dill)
            return self._func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    
    def result(self, workers:int=None, pool_type:str=None, **kwargs)->Generator:
        # 如果没有传入参数, 则使用构造时的参数
        if workers is None:
            workers = self.max_workers
        if pool_type is None:
            pool_type = self.pool_type
        # 如果缓冲区为空, 则直接返回
        if workers == 1 or workers is None:
            # 如果只有一个worker, 或者没有传入worker数量, 则直接运行，不使用线程池或进程池
            _func = dill.loads(self.function_dill)
            result = [_func(*args, **kwargs) for args, kwargs in self.buffer]
        else:
            logger.info("Running ({} workers, {} tasks)".format(workers, len(self.buffer)))
            # 如果有多个worker, 则运行缓冲区中的任务
            if pool_type is not None and pool_type.lower() == "process":
                # 如果是进程池, 则需要将函数序列化，否则会报错
                worker_wrapper = partial(self.worker_wrapper, func=None)
                pool_executor = ProcessPoolExecutor
            else:
                # 如果是线程池, 则不需要将函数序列化
                worker_wrapper = partial(self.worker_wrapper, func=dill.loads(self.function_dill))
                pool_executor = ThreadPoolExecutor
            # 使用线程池或进程池运行任务
            with pool_executor(max_workers=workers) as executor:
                result = executor.map(worker_wrapper, self.buffer)
        # 清空缓冲区
        self.buffer = []
        # 清空函数self._func
        if hasattr(self, "_func"):
            del self._func
        # 返回结果
        return result


def pooling(func:Callable=None, max_workers:int=None, pool_type:str=None, **kwargs):
    """这是一个装饰器，用于将函数转换为MapPool对象

    Parameters
    ----------
    func : Callable, optional
        输入函数,使用形式为@pooling, 不能传入参数, by default None
    max_workers : int, optional
        默认最大工作数目,使用形式为@pooling(), by default None
    pool_type : str, optional
        默认类型,使用形式为@pooling(), by default None

    Returns
    -------
    Callable
        返回MapPool对象
    """
    if func is not None and isinstance(func, Callable) and max_workers is None and pool_type is None:
        return MapPool(func, max_workers, pool_type)
    
    def _MapPoolDecorator(_func):
        return MapPool(_func, max_workers, pool_type)
