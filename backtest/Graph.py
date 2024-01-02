import matplotlib.pyplot as plt
import numpy as np


def draw_return_on_assets(init_fund, df):
    """
    绘制收益相关折线图
    :param init_fund: 初始投入金额
    :param df:  date + total_asset + rate_of_return 时间 总资产 收益率
    :return:
    """
    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False

    figure = plt.figure(1, (10, 8))
    ax = figure.add_subplot(111)

    ax.plot(df['date'], df['total_asset'], 'r--', label='总资产')
    ax.plot(df['date'], np.ones(len(df.index)) * init_fund, 'k-', label='初始投入金额')
    ax.set_ylabel('总资产变化')

    ax1 = ax.twinx()
    ax1.plot(df['date'], df['rate_of_return'], 'r--', label='收益率')
    ax1.set_ylabel('收益率变化')

    figure.legend(loc=3, bbox_to_anchor=(0, 0), bbox_transform=ax1.transAxes)
    plt.show()


