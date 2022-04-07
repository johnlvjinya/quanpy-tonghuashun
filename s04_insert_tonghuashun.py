
########### 参考https://blog.csdn.net/lau_jw/article/details/118224627
########### pip install -i https://pypi.douban.com/simple pyautogui
########## 看鼠标位置软件：链接：https://share.weiyun.com/BlSWOrLx 密码：idhiwy
############# https://www.cnblogs.com/thgpddl/p/12555332.html
import os
import config
import pyautogui as pg
from time import sleep

app_dir = r'D:\同花顺软件\同花顺\hexin.exe'

class InsertIndex():
    def __init__(self):
        index_list = os.listdir(config.f_path['index'])
        self.txt_list = [x.split('.txt')[0] for x in index_list if '.txt' in x]
        print('txt指标的数量', len(self.txt_list))
        self.index_n = len(self.txt_list)          ######### 导入的指标数量

        pass

    def open_app(self):
        os.startfile(app_dir)
        sleep(3)

    def mouse_move_click(self,xy=[]):
        pg.moveTo(xy[0],xy[1])
        sleep(0.02)
        pg.click()
        sleep(1)

    def insert_index(self):
        d = {
        '全屏':[1533,172],
        '工具':[271,10],
        '自选股板块设置':[349,35],
        '自选股':[720,356],

        '板块改名':[1222,411],
        '板块改名输入点击':[961,516],
        '板块改名确定':[999,580],

        '文件空白点击':[],
        '导入':[1227,439],
        '从文件导入':[1244,462],
        '导入文件':[1449,711],
        '选择第一个文件':[877,384],
        '打开1':[1424,750],
        '打开2':[1060,659],
        '完成后确定':[1139,742],
        '自选菜单':[303,38],
        '我的板块':[112,78],
        }
        self.open_app()  # 打开软件
        self.mouse_move_click(d['全屏'])  ### 工具
        self.mouse_move_click(d['工具'])  ### 工具
        sleep(1)
        self.mouse_move_click(d['自选股板块设置'])  ### 自选股板块设置
        for i in range(1, self.index_n+1):  ## 选择第几个自选股模块
            ########## 选择板块
            self.mouse_move_click(d['自选股'])  ### 点击我的自选股
            for j in range(i):
                pg.press('down') # 按向左键


            ########板块改名
            self.mouse_move_click(d['板块改名'])  ### 点击我的自选股
            # self.mouse_move_click(d['板块改名输入点击'])  ### 点击我的自选股
            pg.press('backspace')
            # for x in range(20):pg.press('backspace') # 选择txt
            # for x in self.txt_list[i-1]:pg.write(x)
            sleep(0.1)
            ########### pip install -i https://pypi.douban.com/simple pyperclip
            import pyperclip
            pyperclip.copy(self.txt_list[i-1])
            pg.hotkey('Ctrl','v') # 复制文件名
            sleep(0.1)
            pg.press('enter') # 选择txt
            self.mouse_move_click(d['板块改名确定'])  ### 点击我的自选股


            ##### 文件导入
            self.mouse_move_click(d['导入'])  ### 点击我的自选股
            self.mouse_move_click(d['从文件导入'])  ### 点击从文件导入
            self.mouse_move_click(d['导入文件'])  ### 点击从文件导入
            pg.press('down') # 按向左键
            pg.press('enter') # 选择txt
            self.mouse_move_click(d['选择第一个文件'])  ### 选择第一个文件
            for j in range(i-1):
                pg.press('down') # 按向左键
            self.mouse_move_click(d['打开1'])  ### 点击打开
            self.mouse_move_click(d['打开2'])  ### 点击打开

        self.mouse_move_click(d['完成后确定'])  ### 完成后确定
        self.mouse_move_click(d['自选菜单'])  ### 完成后确定
        self.mouse_move_click(d['我的板块'])  ### 完成后确定

    def run(self):
        self.insert_index()
        pass


if __name__ == "__main__":
    InsertIndex().run()








