
import sys
sys.path.append('../..')
import os
import json
import time
import config
import random
import datetime
import pandas as pd
import baostock as bs

from multiprocessing import Pool
import myutils.dict_json_saver as mdjs

# f_handler=open('out.log', 'w')
# sys.stdout=f_handler

class RefreshLocalData():
    def __init__(self):     # N_Period K线的周期
        self.t1_start = time.time()
        self.stock_list_date = '2022-03-16'
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time()))  # 今天的日期
        pickle_path = os.path.join(config.f_path['excel'],'stock_list.pickle')
        if __name__=='__main__':
            if os.path.exists(pickle_path) is False:
                bs.login()          # 登陆系统
                rs = bs.query_all_stock(self.stock_list_date)   # self.today
                data_list = []
                while (rs.error_code == '0') & rs.next():data_list.append(rs.get_row_data())
                df = pd.DataFrame(data_list, columns=rs.fields)
                df['tradeStatus'] = df['tradeStatus'].astype(int)
                df = df[(df['code']>='sh.600000')&(df['code']<'sz.310000')&(df['tradeStatus']==1)]  # 排除各类指数

                df.to_excel(os.path.join(config.f_path['excel'],'stock_list.xlsx'), index=False)
                df.to_pickle(pickle_path)

        self.df = pd.read_pickle(pickle_path).reset_index()
        print(self.df.shape)

    
    def get_one_stock(self,stock_id='sh.600000', frequency="d"):
        now = datetime.datetime.now()
        if frequency=="d":delta = datetime.timedelta(days=80)
        if frequency=="w":delta = datetime.timedelta(days=250*7)  # 周线和月线日期要移动更多
        if frequency=="m":delta = datetime.timedelta(days=80*30)
        n_days = now - delta
        start_date =  n_days.strftime('%Y-%m-%d')
        ######### 注意安装路径下修改代码，不打印登录成功信息
        ######### C:\myinstall\python\python3.7.7\Lib\site-packages\baostock\login\loginout.py
        bs.login()          # 登陆系统
        rs = bs.query_history_k_data(stock_id, config.query_str,  start_date, end_date=self.today, frequency=frequency, adjustflag="2") # adjustflag=2前复权
        data_list = []
        while (rs.error_code == '0') & rs.next():
            row_i = rs.get_row_data()
            add_bool = True
            for j in row_i:
                if len(j)<=4:
                    add_bool = False
                    break
            if add_bool:
                data_list.append(row_i)
        df = pd.DataFrame(data_list, columns=rs.fields)
        df = df.fillna(method='bfill').fillna(method='ffill').fillna(0)
        
        ####### 列类型转换
        type_dict = {}
        for ci in config.float_str.split(','):
            type_dict[ci] = float
        df = df.astype(type_dict)
        f_path = os.path.join(config.f_path['pickle'], '%s_%s.pickle'%(stock_id, frequency))
        df.to_pickle(f_path)
        return df


    def get_remote_data_date(self):
        choose_stock = 'sh.600000' # 浦发银行，选择一个股票进行对比，查看需不需要全量更新
        bs.login()          # 登陆系统
        n_days = datetime.datetime.now() - datetime.timedelta(days=10)
        start_date =  n_days.strftime('%Y-%m-%d')
        rs = bs.query_history_k_data(choose_stock, 'date,code,close',  start_date, end_date=self.today, frequency='d', adjustflag="2") # adjustflag=2前复权
        data_list = []
        while (rs.error_code == '0') & rs.next():
            row_i = rs.get_row_data()
            add_bool = True
            for j in row_i:
                if len(j)<=4:
                    add_bool = False
                    break
            if add_bool:
                data_list.append(row_i)
        df = pd.DataFrame(data_list, columns=rs.fields)
        remote_data_date = df['date'].tolist()[-1]
        print(remote_data_date)  # 最近的日期
        return choose_stock,remote_data_date


    def get_all_stock_pickle(self):
        
        choose_stock,remote_data_date = self.get_remote_data_date()
        try:
            df = pd.read_pickle(os.path.join(config.f_path['pickle'], '%s_d.pickle'%(choose_stock)))######### 本地数据
            local_data_date = df['date'].tolist()[-1]
        except:
            local_data_date = 0
        print('choose_stock, remote_data_date, local_data_date', choose_stock, remote_data_date, local_data_date) 
        if remote_data_date==local_data_date:          ########### 如果两个日期相同直接返回
            print('不用更新')
            return

        n = os.cpu_count()
        pool = Pool(processes=n-2)  # 默认cpu_count()
        f_list = os.listdir(config.f_path['pickle'])
        for i,r in self.df.iterrows():
            if i%300==0:
                print('*'*10, '已下载(支)数据', i)
            # print(stock_list_df['code'][i])
            # print('...................................................', i,'/',N)
            # if '%s_d.pickle'%r['code'] not in f_list:
            res = pool.apply_async(self.get_one_stock,args=(r['code'],'d',))#.get()
            res = pool.apply_async(self.get_one_stock,args=(r['code'],'w',))#.get()
        pool.close()
        pool.join()
        


    def run(self):
        # self.get_one_stock()
        self.get_all_stock_pickle()
        pass

if __name__=='__main__':
    RefreshLocalData().run()