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
        f = open(os.getcwd() + "\\1960-2019ȫ��GDP����.csv", "r", encoding="GB2312")
        data_lines = f.readlines()  # �������ݣ�readlines���Ƿ����б�
        data_lines.pop(0)  # ������Ϣ
        f.close()
    except NameError as e:
        print(os.getcwd() + "\\1960-2019ȫ��GDP����.csv������")
    return data_lines

def data_build():
    # ���ݽṹ����Ϊ��{��ݣ�[[���ң�gdp][����2��gdp]],���2:[[,],[,]]
    data_dict = {}
    for subjects in init():
        country = subjects.split(",")[1]
        year = int(subjects.split(",")[0])
        GDP = float(subjects.split(",")[2])  # ��������
        try:
            data_dict[year].append([country, GDP])  # �������Ѵ������׷�ӣ������û�У����ڸ�����ֵ��Ӧֵ�ϼ�һ���б�append
        except KeyError:
            data_dict[year] = []
            data_dict[year].append([country, GDP])
    # sorted ������������ֵ��Ƚ�������
    sorted_year = sorted(data_dict.keys())  # �ֵ������һ��keys
    # ÿһ�괴��һ��bar������󹹽�ʱ����Timeline����
    timeline = Timeline({"theme": ThemeType.DARK})  # ���⵼��global��themetype
    # ����ȡǰ�ˣ�����bar bar����ֻ��x���y��������
    # .sort�����÷���keyҪ��һ����������������Ԫ�أ�������������ݣ�����lambda���
    for i in sorted_year:
        data_dict[i].sort(key=lambda element: element[1], reverse=True)
        data_chart_year = data_dict[i][0:8]   # ������Ƭ����ǰ�����
        x_data = []
        y_data = []
        for element in data_chart_year:
            x_data.append(element[0])
            y_data.append(element[1])
        x_data.reverse()
        y_data.reverse()
        bar = Bar()  # bar����
        bar.add_xaxis(x_data)
        bar.add_yaxis("GDP(��)", y_data, label_opts=LabelOpts(position="right"))
        # ȫ������ ��ʽ����f"{����}ddd��
        bar.reversal_axis()
        bar.set_global_opts(
            title_opts=TitleOpts(title=f"{i}��GDPǰ�˹�������"),
            yaxis_opts=options.AxisOpts(
                name_location='center',
            )

        )
        timeline.add(bar, str(i))  # bar�����ʱ�䣨string��
    timeline.add_schema(  # ʱ��������
            play_interval=1000,  # ʱ����
            is_timeline_show=True,
            is_auto_play=True,
            is_loop_play=False,

        )
    timeline.render("1960-2019ȫ��GDPǰ�˹���.html")



if __name__ == '__main__':
    data_build()

