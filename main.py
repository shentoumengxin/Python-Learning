from pyecharts.charts import Map
from pyecharts.options import *
import json
import os


def data_input():
    global f
    try:
        f = open(os.getcwd() + "\疫情.txt", "r", encoding="UTF-8")
    except:
        print(os.getcwd() + "未找到文件")
    data_dict = json.load(f)  # json转化 注意这里load的用法是直接对文件read
    f.close()
    data_China = data_dict["areaTree"][0]["children"]  # 取到中国
    data_list = []  # 绘图数据
    for province in data_China:
        province_name = province["name"]+"省"   # 加上省份才可以连接到地图上
        province_confirm = province["total"]["confirm"]
        data_list.append((province_name, province_confirm))  # 绘制地图数据需要一个列表，里面是多个元组，名称和数据
    return data_list


if __name__ == '__main__':
    map = Map()  # map对象
    map.add("各省份确诊人数", data_input(), "china")
    # global setting 定制分段视觉映射
    map.set_global_opts(
        title_opts=TitleOpts(title="全国疫情地图"),
        visualmap_opts=VisualMapOpts(
            is_show=True,
            is_piecewise=True,  # 是否分段
            pieces=[  # 设置分段，列表加字典格式如下
                {"min": 1, "max": 99, "label": "1-99", "color": "#CCFFFF"},
                {"min": 100, "max": 999, "label": "100-999", "color": "#FFFF99"},
                {"min": 1000, "max": 4999, "label": "1000-99", "color": "#FF9966"},
                {"min": 5000, "max": 9999, "label": "5000-9999", "color": "#FF6666"},
                {"min": 10000, "max": 99999, "label": "10000-99999", "color": "#CC3333"},
                {"min": 100000, "label": "100000+", "color": "#990033"},
            ]
        )
    )
    map.render("China epidemic chart.html")  # 生成图表
