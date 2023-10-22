import os
import pandas as pd
import datetime,time
from sqlalchemy import create_engine
import arrow,calendar
from io import StringIO
import zipfile

def read_sql(database,sql,charset="utf8"):
    engine = create_engine(f'mysql+pymysql://root:kiss173@localhost/{database}?charset={charset}')
    df = pd.read_sql(sql,con=engine)
    # df.replace(",","",inplace = True,regex = True)
    # df = df.apply(pd.to_numeric,errors = 'ignore')
    return df

def save_to_sql(df,database,table_name,charset="utf8"):
    engine = create_engine(f'mysql+pymysql://root:kiss173@localhost/{database}?charset={charset}')
    df.to_sql(table_name,engine,if_exists='append',index=False)
    print(f"数据保存至：{table_name}")

def save_to_alsql(df,table_name):
    engine = create_engine('mysql+pymysql://root:kiss173@121.40.30.131/ryc?charset=utf8')
    df.to_sql(table_name,engine,if_exists='append',index=False)
    print(f"数据保存至：{table_name}")

def unzip(path,save_path):
    """
    解压
    :param path: 文件路径
    :param save_path: 保存路径
    :return:
    """
    zipFile = zipfile.ZipFile(path)
    for file in zipFile.namelist():
        zipFile.extract(file, save_path)
    zipFile.close()
    return


def print_(str,show_type=4,fore_color="",back_color=35):
    """
    格式：
        print("\033[显示方式;前景色;背景色m 要输出的内容 \033[m")
    显示方式：
        0：默认，1：高亮显示 ， 4：下划线， 5：闪烁， 7：反白可见，8：不可见
    颜色 ：前景色 （+10就是背景色）
        30: 黑色,
        31: 红色,
        32: 绿色,
        33: 黄色,
        34: 蓝色,
        35: 紫红色,
        36: 青蓝色,
        37: 白色,
    """
    # 默认颜色是紫色
    print(f"\033[{show_type};{fore_color};{back_color}m{str}\033[m")

def folder_exists(check_file,file_name):
    """
    :param check_file: 需要检查的文件路径
    :param file_name: 需要检查的文件名
    :return:
    """
    path = os.path.join(check_file,str(file_name))
    if os.path.exists(path):
        print(f"此路径已存在：{path}")
    else:
        os.mkdir(path)
        print(f"成功创建：{path}")
    return path

def get_cookies(cookie):
    "cookies 文本转字典"
    cookie = cookie.split(';')
    cookies = {}
    for i in cookie:
        x, y = i.split('=',1)
        cookies[x] = y
    return cookies

def prase_cookies(path1):
    "cookies转字典形式"
    import json
    with open(path1) as f:
        js = json.loads(f.read())
    cookies = {}
    for i in js:
        cookies[i["name"]] = i["value"]
    return cookies

def text_to_df(text_data):
    "文本转df格式"
    data_io = StringIO(text_data)
    df = pd.read_csv(data_io)
    return df

def format_dict(text):
    """爬虫get参数转字典"""
    ls = text.split("\n")
    d = {}
    for i in ls:
        a = i.split(": ")
        try:
            d[a[0]] = a[1]
        except:
            d[a[0]] = ""

    return d

def get_yesterday():
    yesterday = str(datetime.datetime.today()-datetime.timedelta(1))[:10]
    return  yesterday

def get_desk():
    return  os.path.join(os.path.expanduser("~"),"Desktop")

def get_down():
    "获取下载路径"
    return os.path.join(os.path.expanduser("~"),"Downloads")

def date_change(a):
    """
    :param a:日期的转化
    :return: 44000
    """
    if type(a) == int:
        delta = pd.Timedelta(str(int(a)) + 'days')
        time = pd.to_datetime('1899-12-30') + delta
        return time
    else:
        return a

def getMonthDate(timedelta = 1):
    """
    :param timedelta: 1：获取上月全部日期 ，0：获取本月全部日期
    :return: 全月日期列表
    """
    now = datetime.datetime.now()
    # now = datetime.date(now.year,now.month,1) - datetime.timedelta(timedelta)
    now = datetime.date(now.year, now.month - timedelta, 1)
    print(now)
    num = calendar.monthrange(now.year,now.month)[1]
    if now.month < 10 :
        month = "0" + str(now.month)
    else:
        month = str(now.month)
    date_ls =[]
    date = f"{now.year}-{month}-01"
    start_date = f"{now.year}-{month}-1"
    a = 0
    for i in range(num):
        date = arrow.get(start_date).shift(days = a).format("YYYY-MM-DD")
        a += 1
        date_ls.append(date)
    return date_ls

def text_date(a,days=0):
    """
    :param a: 20210505 格式的日期
    :return:  2021-05-05
    """
    a = str(a)
    year = int(a[:4])
    month = int(a[4:6])
    day = int(a[6:])
    one_day = datetime.timedelta(days)
    date = datetime.datetime(year, month, day) - one_day
    return str(date)[:10]

def get_mtd_date():
    """
    :return:返回的是列表，["2022-01-01","2022-01-31","2021-01-01","2022-01-31"]
    """
    # today = datetime.datetime.today()
    today = datetime.datetime.today() - datetime.timedelta(1)

    start_date = datetime.date(today.year, today.month, 1)
    end_date = today # 2022-01-24 13:42:09.517008

    last_start_date = datetime.date(start_date.year - 1, start_date.month, start_date.day)
    last_end_date = datetime.date(end_date.year - 1, end_date.month, end_date.day)

    ls = [str(start_date)[:10], str(end_date)[:10], str(last_start_date)[:10], str(last_end_date)[:10]]
    return ls

def df_sort(df,ls,colum_name):
    """
    :param df: Datefram
    :param ls: 自定义的顺序
    :param colum_name : 需要排序的列名
    :return: DF
    """
    df[colum_name] = df[colum_name].astype('category').cat.set_categories(ls)
    df.sort_values(by=[colum_name], ascending=True, inplace=True)
    return  df



def get_files(path):
    """
    获取全部文件，包括文件夹内的
    :param path: 一级路径
    :return:
    """
    ls  = []
    def append(path):
        with os.scandir(path) as files:
            for file in files:
                if file.is_dir() :
                    append(file)
                elif file.is_file():
                    ls.append(file.path)
    append(path)
    return ls

def concat_dict(*dict_args):
    "合并字典"
    d = {}
    for i in dict_args:
        d.update(i)
    return d


def get_file_path(path):
    """
    :param path:文件夹路径
    :return: 路径下文件路径
    """
    ls = []
    with os.scandir(path) as it :
        for file in it:
            if "ini" not in file.path and "~$" not in file.path:
                ls.append(file.path)
    return ls

def millisecond_to_time(millis):
    """13位时间戳转换为日期格式字符串"""
    return time.strftime('%Y-%m-%d',time.localtime(millis/1000))

def get_millisecond():
    """
    :return: 获取精确毫秒时间戳,13位
    """
    millis = int(round(time.time() * 1000))
    return millis

def save_desk(file_name):
    """
    :param file_name:  自定义文件名称
    :return: 路径
    """
    desk_p = os.path.join(os.path.expanduser("~"),"Desktop")
    return os.path.join(desk_p,file_name)

def first_appear(a,dic):
    if a not in dic:
        dic[a] = 1
        return 1
    return 0

def df_excel_concat(path_ls,skip_num=0):
    """
    :param path_ls: 文件路径的列表
    :return:  df
    """
    df_ls =[]
    for path in path_ls:
        try:
            df = pd.read_excel(path,skiprows=skip_num)
            df_ls.append(df)
            print(path)
        except:
            df = pd.read_csv(path,skiprows=skip_num)
            df_ls.append(df)
            print(path)
    df = pd.concat(df_ls)
    return df

# 年份
def isLeapYear(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    # 断言：年份不为整数时，抛出异常。
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, '不是闰年')
        days_sum = 365
        return days_sum


def getAllDayPerYear(years):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))
    print()
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)
    # print(all_date_list)
    return all_date_list


def find_dict_differences(dict1, dict2):
    # 比较键的差异
    keys_diff = set(dict1.keys()) - set(dict2.keys())
    keys_diff.update(set(dict2.keys()) - set(dict1.keys()))

    # 比较值的差异
    values_diff = {}
    for key in dict1.keys():
        if key in dict2 and dict1[key] != dict2[key]:
            values_diff[key] = (dict1[key], dict2[key])
    print("键的差异:", keys_diff)
    print("值的差异:", values_diff)
    return keys_diff, values_diff


def find_missing_dates(sql_df1):
    # 获取当前日期
    end_date = datetime.datetime.now().date()
    # 计算30天前的日期
    start_date = end_date - datetime.timedelta(days=29)
    # 连接数据库并查询日期数据，得到一个日期列表dates
    dates = sql_df1.iloc[:, 0].tolist()
    # 生成一个包含所有日期的列表
    expected_dates = [start_date + datetime.timedelta(days=x) for x in range(30)]
    # 找到缺漏的日期
    missing_dates = [date for date in expected_dates if date not in dates]
    return missing_dates

def text_to_df(text):
    """
    "店铺","入会渠道","会员数","会员成交数","会员成交占比"
    "京东特步风行专卖店","手淘-扫码-云码入会页面-入会后二级页面","41","0","0.0"
    """
    # 通过 StringIO 将文本转换为类文件对象
    file_like_object = StringIO(text)
    # 使用 read_csv 读取类文件对象，并设置适当的参数
    df = pd.read_csv(file_like_object, quotechar='"', skipinitialspace=True)
    return df

if __name__ == '__main__':
    print(1)
    print(get_mtd_date())