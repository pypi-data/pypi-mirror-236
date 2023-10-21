# Python装饰器原理浅见

## 1. 装饰器的定义

装饰器是一个函数，它接受一个函数作为输入并返回另一个函数作为输出。

装饰器的作用是在不改变原函数的情况下，为原函数添加新的功能。

## 2. 装饰器的原理：
装饰器的使用方法是在原函数的定义前加上@装饰器名，如下所示：
```
@decorator
def func(*args, **kwargs):
     pass
```
其调用形式等同于以下代码：
```
## 完全等价（间接形式）
func = decorator(func)
result = func(*args, **kwargs)
## 完全等价（直接形式）
result = decorator(func)(*args, **kwargs)
```
同理，如果在一个函数上使用了多个装饰器
```
@decorator1
@decorator2
def func(*args, **kwargs):
     pass
```
则其调用形式等同于以下代码：
```
## 完全等价（间接形式）
func1 = decorator1(func2)
func2 = decorator2(func)
result = func1(*args, **kwargs)
## 完全等价（直接形式）
result = decorator1(decorator2(func))(*args, **kwargs)
```
## 3. 装饰器实现
由上节可见，decorator函数只能有一个传入参数func，无论decorator函数本身怎么实现。
### 简单装饰器
极简装饰器（无任何功能、无法修改传入参数、多此一举）
```
def decorator(func):
    return func

@decorator
def func(*args, **kwargs):
    pass
```
极简装饰器进阶版（可修改传入参数）
```
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def func(*args, **kwargs):
    pass
```
### 带参装饰器
带参数的装饰器根据上面的等价公式应当形如下面所示
```
results = decorator(func)(*args, **kwargs)
        = decorator_with_params(*dargs, **dkwargs)(func)(*args, **kwargs)
```
依据原理简单替换decorator
```
def decorator_with_params(*dargs, **dkwargs):
    def wrapper(func):
        print(dargs, dkwargs)
        return func
    return wrapper

@decorator_with_params(*dargs, **dkwargs)
def func(*args, **kwargs):
    pass

```
可以发现，上面的代码形似极简装饰器，装饰器的参数不能传给func函数。如果要将dargs,dkwargs应用于func函数内，需要进行深度嵌套
```
def decorator_with_params(*dargs, **dkwargs):
    def wrapper(func):
        def wrapper_(*args, **kwargs):
            print(dargs, dkwargs, args, kwargs)
            # return func(*args, *dargs, **kwargs, **dkwargs)
            return func(*args, **kwargs) 
        return wrapper_
    return wrapper

@decorator_with_params(*dargs, **dkwargs)
def func(*args, **kwargs):
    pass
```
***
理解了上面的内容，装饰器再如何变形都能一下子写出来了。

以下是本文的参考与进阶链接:  
- [恶补了 Python 装饰器的八种写法，你随便问~](https://zhuanlan.zhihu.com/p/269012332)