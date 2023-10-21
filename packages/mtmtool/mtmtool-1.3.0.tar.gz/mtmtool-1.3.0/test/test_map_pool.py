from mtmtool.pool import pooling, MapPool

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

    # 测试装饰器中，多进程运行时，是否能打印日志
    import os
    from mtmtool.log import create_stream_logger, logging
    logger = create_stream_logger("test", log_level=logging.INFO)
    logger.info(f"pid: 0, ppid: 0")

    @pooling(max_workers=4, pool_type="Process")
    def add(a, b):
        pid = os.getpid()
        ppid = os.getppid()
        # 注意此时的logger很奇怪，是warning级别，而不是期望的info级别
        # 此处logger获取全局变量里的logger设置,获取上一级函数本地变量的logger名称。
        logger.info(f"pid: {pid}, ppid: {ppid}")
        logger.warning(f"pid: {pid}, ppid: {ppid}")
        return a + b

    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Process")) == [3, 4]

if __name__ == '__main__':
    test_pooling_with_params()
