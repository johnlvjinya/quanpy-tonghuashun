

import os
import time
import platform
import datetime

####### 同花顺自选股的路径，

####### baostock选择的字段
float_str = 'open,high,low,close,turn,volume'
query_str =  'date,code,%s'%float_str  ### baostock查询的字段



ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
###################################################### 数据和文件保存的路径
current_system = platform.system()
if current_system is 'Windows':
    pre_data_str = 'D:/stock'             # windows系统
    python = 'python'
else:
    pre_data_str = "/lvf/stock"       # linux系统
    python = 'python3.7'
f_stop_point_list = ['D:/', '/lvf']    # 文件展示停止递归的节点

f_path = {
    'temp':os.path.join(pre_data_str, 'temp'),
    'pickle':os.path.join(pre_data_str, 'pickle'),
    'index':os.path.join(pre_data_str, 'index'),
    'stock':os.path.join(pre_data_str, 'stock'),
    'data_analysis_res':os.path.join(pre_data_str, 'data_analysis_res'),
    'json':os.path.join(pre_data_str, 'json'),
    'ec_json':os.path.join(pre_data_str, 'ec_json'),
    'excel':os.path.join(pre_data_str, 'excel'),
    'log':os.path.join(pre_data_str, 'log'),  # 检查数据输入是否规范
}
for k,v in f_path.items():
    if os.path.exists(v) is False:
        os.makedirs(v)
