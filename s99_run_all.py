

import s01_get_stock_history as s01
import s02_get_stock_index as s02
import s03_select_index as s03
import s04_insert_tonghuashun as s04

if __name__=='__main__':
    s01.RefreshLocalData().run()
    s02.RefreshLocalData().run()
    s03.SelectIndex().run()
    s04.InsertIndex().run()


