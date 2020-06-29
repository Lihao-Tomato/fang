import pymysql
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager

class Fang():
    def __init__(self):
        '''从数据库读取房价信息'''
        self.conn = pymysql.connect(host = 'localhost',
                               user = 'root',
                               passwd = 'root',
                               db = 'fang',
                               charset = 'utf8')
        sql_query = 'select * from fang.fang_info'
        self.df = pd.read_sql(sql_query, con=self.conn)
        # print(df.head(10))
        # print(df.info())

    def extract_shanxi(self):
        '''选取陕西省的房价信息'''
        df_shanxi = self.df[(self.df['province'] == '陕西')]

        # 去掉重复信息
        df_shanxi_info = df_shanxi.drop_duplicates('name')
        # 取出所有不包含'/套'的数据
        df_shanxi_info = df_shanxi_info[~(df_shanxi_info['price'].map(lambda x:x.split('/')[-1]).isin(['套']))]
        # 只提取价格中的数字 3000元/㎡------->3000并与之前的数据合并
        self.df['price_num'] = df_shanxi_info['price'].str.extract(r'(\d+)', flags=0, expand=False).astype('float64')
        df_shanxi_info = df_shanxi_info.join(self.df['price_num'])
        df_shanxi_info = df_shanxi_info[pd.notnull(self.df['price_num'])]

        # 按照城市分组求每个城市的平均价格
        shanxi_grouped = self.df['price_num'].groupby(df_shanxi_info['city']).mean().sort_values(ascending=False)
        print(type(shanxi_grouped))

        self.conn.close()
        return shanxi_grouped

    def draw_fang(self, shanxi_grouped):
        '''画图'''
        fig = plt.figure(figsize=(20, 8), dpi=80)
        my_font = font_manager.FontProperties(fname="C:/WINDOWS/FONTS/SIMHEI.TTF", size=20)
        text_font = font_manager.FontProperties(fname="C:/WINDOWS/FONTS/MSYHL.TTC", size=50)
        _x = range(len(shanxi_grouped.index))
        _y = shanxi_grouped.values

        plt.bar(_x, _y, width=0.2, color='blue')
        plt.xticks(_x, shanxi_grouped.index, fontproperties=my_font, size=13)
        plt.xlabel('城市', fontproperties=my_font, color='orange')
        plt.ylabel('平均房价（元/㎡）', fontproperties=my_font, color='orange')
        plt.title('陕西省各个城市的平均房价统计', fontproperties=my_font, color='orange')

        # 网格
        plt.grid(linestyle="--", alpha=0.4)
        # 水印
        fig.text(x=0.4,
                 y=0.7,
                 s='好吃的小西红柿',
                 color='gray',
                 fontproperties=text_font,
                 rotation=45,
                 alpha=0.2)

        plt.savefig('./fang.png')
        plt.show()

    def run(self):
        shanxi_grouped = self.extract_shanxi()
        self.draw_fang(shanxi_grouped)


if __name__ == '__main__':
    fang = Fang()
    fang.run()

