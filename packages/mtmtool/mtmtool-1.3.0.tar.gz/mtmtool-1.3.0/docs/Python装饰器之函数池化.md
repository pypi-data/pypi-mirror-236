# Python装饰器之函数池化（直接调用/多线程池/多进程池）

Python是默认单核单线程运行的，跑满CPU需要调用多进程。作者此前在使用多进程中感觉很麻烦，故学习并完成这个装饰器。

## 痛点  
1. 每次调用池需要先构建池
2. 传入池的参数需要可迭代，需要将已有的输入参数再处理

## 原理
1. 使用装饰器，构造一个新类对象来封装目标函数，调用函数时实际调用这个类。
2. 这个类会根据传入参数判断执行多线程还是多进程。
3. 如果没有找到某些传入参数，则跟直接调用原函数效果一样，来达到无感运行的目的。
4. 使用缓冲区来保存每次调用传入的参数，不用自己再手动准备，只需按照原来的方式调用类对象，在需要结果的时候调用类对象的result函数即可
5. 调用多进程时，Python内置库multiprocessing使用的pickle无法打包函数内的本地函数(local)等，故统一使用dill库对目标函数进行序列化封装，在运行过程中加载序列化后的目标函数，不然会提示出错。（这一步可能会降低运行效率）

## 代码
### 1. 源代码
#### 类名来源：  
- 单词map有映射含义，且功能之一使用缓冲区来将用户的输入参数映射到进程池本身需要的参数上。
- 单词map包含multiprocessing的简写mp两个字母
```
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

    
    def result(self, workers:int=None, pool_type:str=None)->Generator:
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

def pooling(func:Callable=None, max_workers:int=None, pool_type:str=None):
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
    
    return _MapPoolDecorator

```
### 2. 测试代码
测试代码既是测试也是示例，基本运行方式都在里面。分为两种：
- 对已有的函数封装，详见test_MapPool
- 在函数定义时装饰，详见test_pooling
```
# FileName: test_pooling.py
def test_MapPool():
    def add(a, b):
        return a + b
    pow = MapPool(add)
    result = pow(10,5)
    assert result == 15

    pow = MapPool(add, max_workers=2, ptype="Thread")
    result = pow(10,5)
    result = pow(10,5)
    assert list(pow.result()) == [15, 15]

    pow = MapPool(add, max_workers=2, ptype="process")
    result = pow(10,5)
    result = pow(10,5)
    assert list(pow.result()) == [15, 15]

    pow = MapPool(add, max_workers=None, ptype="process")
    result = pow(10,5)
    assert result == 15

    pow = MapPool(add, max_workers=None, ptype="Thread")
    result = pow(10,5)
    assert result == 15

def test_pooling_no_params():
    # 构造装饰器后的函数，装饰时不带传入参数，（推荐）
    @pooling
    def add(a, b):
        return a + b

    # 单线程运行
    assert add(1, 2) == 3

    # 多线程运行
    add(1, 2, workers=2)
    add(1, 3, workers=2)
    assert list(add.result(workers=2, pool_type="Thread")) == [3, 4]

    # 多进程运行
    add(1, 2, workers=2)
    add(1, 3, workers=2)
    assert list(add.result(workers=2, pool_type="Process")) == [3, 4]

    # 测试装饰器后更改max_workers，是否生效
    add.max_workers = 2
    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Thread")) == [3, 4]
    
    # 测试装饰器后更改pool_type，是否生效
    add.max_workers = 2
    add.pool_type = "Process"
    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Thread")) == [3, 4]
    
def test_pooling_with_params():
    # 构造装饰器后的函数, 装饰时带传入参数
    @pooling(max_workers=2, pool_type="Thread")
    def add(a, b):
        return a + b
    
    # 单线程运行
    assert add(1, 2, workers=None) == 3

    # 多线程运行
    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Thread")) == [3, 4]

    # 多进程运行
    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Process")) == [3, 4]

    # 测试装饰器后的函数属性
    assert add.__name__ == "add"

    # 测试装饰器后更改max_workers，是否生效
    add.max_workers = None
    assert add(1, 2) == 3
    add.max_workers = 2
    add(1, 2)
    assert list(add.result(pool_type="Process")) == [3]
    add(1, 2)
    assert list(add.result(pool_type="Process")) == [3]

```
## 简单示例
对已有的函数封装
```
def add(a, b):
    return a+b

add_ = MapPool(add, max_workers=2, pool_type="Process")
for i in range(10):
    add_(i, i)
print(add_.result())
```
在函数定义时装饰
```
# 装饰函数
@pooling
def add_(a, b):
    return a+b

# 无参数直接调用
for i in range(10):
    # 在装饰时没有传入参数
    print(add_(i, i)) # 调用时不传worker参数，直接返回结果，不适用池

# 带参数放入缓冲区
for i in range(10):
    add_(i, i, workers=2) # 在装饰时传入大于0的worker参数，添加到缓冲区，不直接返回结果
    
print(add_.result()) # 默认是Thread，使用线程池

# 无参数放入缓冲区
add_.workers = 2 # 修改类对象的参数，当不添加workers参数时，使用类对象参数
for i in range(10):
    add_(i, i)
print(add_.result(pool_type="Process")) # Process，使用进程池    
```
***
上面的代码在Github上的个人工具库内，可以通过pip安装```pip install mtmtool==1.2.9```，导入代码为```from mtmtool.pool import MapPool, pooling```。由于是个人库，不会考虑前后兼容问题，小伙伴们注意下版本号，与此篇一样的代码最新版本号为1.2.9。  
在完全理解了上一篇原理和这一篇的示例以后，希望大家都可以自定义装饰器完成复杂功能


参考链接
- [Python装饰器原理浅见](https://zhuanlan.zhihu.com/p/638017255)
- [imutum_python_tool](https://github.com/imutum/imutum_python_tool)
- [What can multiprocessing and dill do together?](https://stackoverflow.com/questions/19984152/what-can-multiprocessing-and-dill-do-together)