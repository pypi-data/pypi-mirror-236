import datetime, calendar
import re

class MTime:
    @staticmethod
    def from_str(timestr:str, format="%Y-%m-%d %H:%M:%S", utc=False):
        dt = datetime.datetime.strptime(timestr, format)
        if utc:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    
    @staticmethod
    def from_timestamp(timestamp:float, ms=True, utc=False):
        if utc:
            return datetime.datetime.utcfromtimestamp(timestamp / (1000 if ms else 1))
        else:
            return datetime.datetime.fromtimestamp(timestamp / (1000 if ms else 1))
    
    @staticmethod
    def to_timestamp(dt:datetime.datetime, ms=True):
        return dt.timestamp() * (1000 if ms else 1)
                   
    @staticmethod
    def to_str(dt:datetime.datetime, format="%Y-%m-%d %H:%M:%S"):
        return dt.strftime(format)

    @staticmethod
    def months_ago(dt:datetime.datetime, months=1, day_of_month=1):
        for _ in range(months):
            dt = dt.replace(day=1) - datetime.timedelta(days=1)
        return dt.replace(day=day_of_month)

    @staticmethod
    def months_later(dt:datetime.datetime, months=1, day_of_month=1):
        for _ in range(months):
            _, days_of_month = calendar.monthrange(dt.year, dt.month)
            dt = dt.replace(day=days_of_month) + datetime.timedelta(days=1)
        return dt.replace(day=day_of_month)

    @staticmethod
    def days_ago(dt:datetime.datetime, days=1):
        return dt + datetime.timedelta(days=days)

    @staticmethod
    def days_later(dt:datetime.datetime, days=1):
        return dt - datetime.timedelta(days=days)


def auto_parse_time_with_datefmt(timestr, datefmt):
    pattern = datefmt.replace("%Y", "(\d{4})")\
                    .replace("%j", "([0-2][0-9]{2}|3[0-5][0-9]|36[0-6])")\
                    .replace("%m", "(0[1-9]|1[0-2])")\
                    .replace("%d", "(0[1-9]|[1-2][0-9]|3[0-1])")\
                    .replace("%H", "(0[0-9]|1[0-9]|2[0-3])")\
                    .replace("%M", "([0-5][0-9])")\
                    .replace("%S", "([0-5][0-9])")
    pattern = f"{pattern}"
    match = re.findall("(%[YjHMSmd])", datefmt)
    if match is None:
        return []
    datefmt_new = "".join(match) if match else ""
    match = re.findall(pattern, timestr)
    datestr_new = ["".join(i) for i in match] if match else []
    return [datetime.datetime.strptime(i, datefmt_new) for i in datestr_new]


def datetimes_split_to_columns(dataframe, column:str="datetime", index:bool=False, times_first:bool=True):
    """将时间列拆分为(年, 月, 月中日, 年中日, 时, 分, 秒)等列

    Parameters
    ----------
    dataframe : pandas.DataFrame
        待处理的DataFrame
    column : str, optional
        列名称, 当index参数为False时, 使用列名获取时间列表, by default "datetime"
    index : bool, optional
        时间列是否是DataFrame的索引, by default True
    times_first : bool, optional
        是否要把拆分的时间列放在所有列的最前面, by default True

    Returns
    -------
    pandas.DataFrame
        处理后的DataFrame
    """
    import pandas as pd
    # 检查输入是否是DataFrame
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Input dataframe is not a pandas.DataFrame object")
    # 复制DataFrame
    df = dataframe.copy()
    # 保存原始列名
    t_columns = list(df.columns)
    # 获取时间列表
    if index: # 如果时间列表是DataFrame的索引
        df_time_list = df.index.to_list()
    else: # 如果时间列表是DataFrame的列
        df_time_list = df[column].to_list()
    # 添加时间列
    df["year"] = [i.year for i in df_time_list]
    df["month"] = [i.month for i in df_time_list]
    df["day"] = [i.day for i in df_time_list]
    df["yday"] = [i.timetuple().tm_yday for i in df_time_list]
    df["hour"] = [i.hour for i in df_time_list]
    df["minute"] = [i.minute for i in df_time_list]
    df["second"] = [i.second for i in df_time_list]
    if times_first: # 判断时间列是否放在最前面
        # 调整列顺序
        df_columns_new = list(df.columns[len(t_columns):]) + list(t_columns)
        df = df.loc[:, df_columns_new]
    return df


