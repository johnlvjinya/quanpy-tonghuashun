

import sys
sys.path.append('../..')

import os
import time
import random
import config
import datetime
import numpy as np
import pandas as pd
import baostock as bs

from jinja2 import Environment, FileSystemLoader

class SelectIndex():
    def __init__(self):
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time()))  # 今天的日期
        f_path = os.path.join(config.f_path['excel'], 'myindex_%s.xlsx'%self.today)
        try:
            self.df = pd.read_excel(f_path)
        except:
            # myindex_2022-03-29.xlsx
            self.df = None
            self.df = pd.read_excel(os.path.join(config.f_path['excel'], 'myindex_2022-04-02.xlsx'))
            print('数据不存在')    

    def index1(self):
        df = self.df
        df = df[
            (df['低价系数']<1.02)
        ]
        res_dict = {
            'name':'01-低价系数1p02股票',
            'df':df
        }
        return res_dict

    def index2(self):
        df = self.df
        df = df[
            (df['5周涨幅']<-15)
            &(df['2日涨幅']>2)
        ]
        res_dict = {
            'name':'02-5周跌2日反弹',
            'df':df
        }
        return res_dict

    def index3(self):         ######### 低价股，最近上涨较大
        df = self.df
        df = df[
            (df['10周涨幅']>20)
            &(df['低价系数']<1.3)
        ]
        res_dict = {
            'name':'03-10周低价涨幅20',
            'df':df
        }
        return res_dict


    def create_stock(self):
        index_dict_list = [
        self.index1(),
        self.index2(),
        self.index3(),
        ]

        f_path = os.path.join(config.f_path['index'], '指标.xlsx')

        writer=pd.ExcelWriter(f_path)
        for i,dict_i in enumerate(index_dict_list):
            # print(df['算法模块'][i], type(df['算法模块'][i]))
            dict_i['df'].to_excel(writer,sheet_name=dict_i['name'],index=False)
            txt_path = os.path.join(config.f_path['index'], dict_i['name']+'.txt')
            with open(txt_path, 'w') as f2:
                for code_j in dict_i['df']['code']:
                    f2.write(code_j+'\n')
        writer.save()

    def run(self):
        if self.df is None:
            return
        print('数据的大小', self.df.shape)
        self.create_stock()






if __name__=='__main__':
    SelectIndex().run()






