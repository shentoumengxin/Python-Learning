# coding=gb2312
import os

from pyecharts import options
from pyecharts.charts import Bar, Timeline
from pyecharts.options import *
from pyecharts.globals import ThemeType


def init():
    global data_lines, f
    data_lines = []
    try:
        f = open(os.getcwd() + "\\1960-2019全球GDP数据.csv", "r", encoding="GB2312")
        data_lines = f.readlines()  # 读入数据，readlines才是返回列表
        data_lines.pop(0)  # 无用信息
        f.close()
    except NameError as e:
        print(os.getcwd() + "\\1960-2019全国GDP数据.csv不存在")
    return data_lines

def data_build():
    # 数据结构设置为：{年份：[[国家，gdp][国家2，gdp]],年份2:[[,],[,]]
    data_dict = {}
    for subjects in init():
        country = subjects.split(",")[1]
        year = int(subjects.split(",")[0])
        GDP = float(subjects.split(",")[2])  # 处理数据
        try:
            data_dict[year].append([country, GDP])  # 如果年份已储存过则追加，若年份没有，就在该年份字典对应值上加一个列表并append
        except KeyError:
            data_dict[year] = []
            data_dict[year].append([country, GDP])
    # sorted 接下来对年份字典先进行排序
    sorted_year = sorted(data_dict.keys())  # 字典可以有一个keys
    # 每一年创造一个bar对象，随后构建时间条Timeline对象
    timeline = Timeline({"theme": ThemeType.DARK})  # 主题导入global的themetype
    # 排序取前八，存入bar bar对象只有x轴和y轴两个集
    # .sort函数用法：key要是一个函数，输入排序元素，返回排序的依据，可用lambda表达
    for i in sorted_year:
        data_dict[i].sort(key=lambda element: element[1], reverse=True)
        data_chart_year = data_dict[i][0:8]   # 序列切片满足前开后闭
        x_data = []
        y_data = []
        for element in data_chart_year:
            x_data.append(element[0])
            y_data.append(element[1])
        x_data.reverse()
        y_data.reverse()
        bar = Bar()  # bar对象
        bar.add_xaxis(x_data)
        bar.add_yaxis("GDP(亿)", y_data, label_opts=LabelOpts(position="right"))
        # 全局设置 格式化：f"{变量}ddd”
        bar.reversal_axis()
        bar.set_global_opts(
            title_opts=TitleOpts(title=f"{i}年GDP前八国家数据"),
            yaxis_opts=options.AxisOpts(
                name_location='center',
            )

        )
        timeline.add(bar, str(i))  # bar对象和时间（string）
    timeline.add_schema(  # 时间线设置
            play_interval=1000,  # 时间间隔
            is_timeline_show=True,
            is_auto_play=True,
            is_loop_play=False,

        )
    timeline.render("1960-2019全球GDP前八国家.html")



if __name__ == '__main__':
    data_build()

