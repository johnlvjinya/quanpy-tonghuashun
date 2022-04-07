
import pandas as pd

def pre_deal(df):
    df['total_v'] = (df['volume']*df['close']*100/(df['turn']+0.0000000001)/100000000).astype(int) # 亿元

    return df

def calculate_one_index(df_d, df_w):
    ######## 预处理
    df_d = pre_deal(df_d)
    df_w = pre_deal(df_w)

    if __name__=='__main__':
        df_d.to_excel(os.path.join(config.f_path['excel'], 'sh.600000.xlsx'), index=False)

    def last_v(df, col):           ### 得到一列的最后一个值
        return df[col].tolist()[-1]

    def low_index(df, col):           ### 向低空间,越小越好
        return round(df[col].tolist()[-1]/df[col].min(),2)

    def high_index(df, col):           ### 向高指标,越大越好
        return round(df[col].max()/df[col].tolist()[-1],2)

    def price_grow(df, n_period=5):
        N = df.shape[0]
        if N>n_period+3:
            res1 = (df['close'][N-1]-df['close'][N-1-n_period])/df['close'][N-1-n_period]
        else:
            res1 = 0     
        return round(100*res1,1)

    def create_all_index():
        col_v_dict = {              # 注意这个字典的值都是List, key用都好分割字符
        '总市值':last_v(df_d,'total_v'),
        '低价系数':low_index(df_w,'close'),
        '高价系数':high_index(df_w,'close'),
        '2日涨幅':price_grow(df_d, n_period=2),
        '5日涨幅':price_grow(df_d, n_period=5),
        '5周涨幅':price_grow(df_w, n_period=5),
        '10周涨幅':price_grow(df_w, n_period=5),

        }
        return col_v_dict#list(col_v_dict.keys()), list(col_v_dict.values())


    res = create_all_index()
    return res


if __name__=='__main__':

    import sys
    sys.path.append('..')
    import os
    import config
    df_d = pd.read_pickle(os.path.join(config.f_path['pickle'], 'sh.600000_d.pickle'))
    df_w = pd.read_pickle(os.path.join(config.f_path['pickle'], 'sh.600000_w.pickle'))

    res=calculate_one_index(df_d, df_w)
    print(res)
