import numpy as np


def ema(df_local, cycle, according_to_column):
    """
    指数平均，在pd上增加一列ema

    :param df_local: 原始pd数据，需要有收盘价
    :param cycle: ema周期，例如6，12，22等
    :param according_to_column: 根据哪一行计算ema
    :return:
    """
    alpha = 2.0 / (cycle + 1)
    df_local['ema'] = np.zeros(len(df_local.index))
    df_local.loc[0, 'ema'] = df_local.loc[0, according_to_column]
    for i in range(1, len(df_local.index)):
        df_local.loc[i, 'ema'] = (alpha * df_local.iloc[i][according_to_column] +
                                  (1 - alpha) * df_local.iloc[i - 1]['ema'])
    return df_local