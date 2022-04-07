
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
import matplotlib.pyplot as plt
from myutils.index_cal import calculate_one_index
from myutils.func_decorated import log_func_time
from multiprocessing import Pool


class RefreshLocalData():
    def __init__(self):
        pickle_path = os.path.join(config.f_path['excel'],'stock_list.pickle')
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time()))  # 今天的日期
        self.df = pd.read_pickle(pickle_path)  # 股票列表
        self.stock_pickle_list = os.listdir(config.f_path['pickle'])  # 已经下载的股票

    def read_one_pickle(self,stock_id, frequency='d'):
        # df.to_excel('test_%s.xlsx'%frequency, index=False)
        stp_name = '%s_%s.pickle'%(stock_id, frequency)
        if stp_name not in self.stock_pickle_list:
            return None
        df = pd.read_pickle(os.path.join(config.f_path['pickle'], stp_name))
        return df

    def calculate_one_stock(self, stock_id='sh.600000'):
        # print('test')
        df_d = self.read_one_pickle(stock_id, frequency="d")
        df_w = self.read_one_pickle(stock_id, frequency="w")
        if df_d is None or df_w is None:
            return None
        index_dict = calculate_one_index(df_d, df_w)
        return index_dict       

    def calculate_all_stock_multi_process(self):
        n = os.cpu_count()
        pool = Pool(processes=n-2)  # 默认cpu_count()

        f_path = os.path.join(config.f_path['excel'], 'stock_list.pickle')
        stock_list_df = pd.read_pickle(f_path).reset_index(drop=True)
        # print(stock_list_df.columns)
        N = 3  # stock_list_df.shape[0]
        N = stock_list_df.shape[0]
        wrong_list = []
        rows=[]
        res_list = []
        for i in range(N):
            index_dict = pool.apply_async(self.calculate_one_stock,args=(stock_list_df['code'][i],))#.get()
            res_list.append(index_dict)
        pool.close()
        pool.join()

        
        for i,res in enumerate(res_list):
            res = res.get()
            # print(res)
            try:
                if res is not None:
                    rows.append([stock_list_df['code'][i]]+list(res.values()))
            except:
                wrong_list.append(stock_list_df['code'][i])

        for res in res_list:
            if res.get() is not None:
                cols_list = ['code']+list(res.get().keys())
                break

        print('这些code报错了==>', wrong_list[:10])
        df = pd.DataFrame(rows, columns=cols_list)
        # print(df)
        df1 = stock_list_df['code,code_name'.split(',')]
        df = pd.merge(df1,df,on='code', how='inner')

        f_path = os.path.join(config.f_path['excel'], 'myindex_%s.xlsx'%self.today)
        df.to_excel(f_path, index=False)
        return df

    def run(self):

        self.calculate_all_stock_multi_process()
        pass

if __name__=='__main__':
    RefreshLocalData().run()