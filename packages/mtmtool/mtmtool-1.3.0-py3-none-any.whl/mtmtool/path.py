import os


def desktop():
    # 获取桌面路径
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def auto_make_dirs(path:str, is_dir:bool=False, is_file:bool=False):
    """根据路径创建文件夹. 如果路径是文件, 创建父文件夹; 如果路径是文件夹, 直接创建该文件夹.
    如果没有指定is_dir和is_file参数, 则根据路径是否有后缀名智能判断路径是否是文件路径.

    Parameters
    ----------
    path : str
        要创建的路径
    is_dir : bool, optional
        路径是否是文件夹路径, by default False
    is_file : bool, optional
        路径是否是文件路径, by default False
    """
    abspath = os.path.abspath(path)
    # 如果is_dir和is_file参数都为True，则抛出异常
    if is_dir and is_file:
        raise ValueError("is_dir and is_file can't be True at the same time")
    # 如果没有指定is_dir和is_file参数，则根据路径是否有后缀名智能判断是否是文件
    if not is_dir and not is_file:
        if os.path.splitext(abspath)[1] == "":
            is_dir = True
        else:
            is_file = True
    # 根据is_dir和is_file参数判断路径是文件还是文件夹
    if is_dir:
        obj_path = abspath
    elif is_file:
        obj_path = os.path.dirname(abspath)
    else:
        raise ValueError("Code error! Can't reach here")
    # 如果路径不存在，则创建路径
    if not os.path.exists(obj_path):
        os.makedirs(obj_path)



