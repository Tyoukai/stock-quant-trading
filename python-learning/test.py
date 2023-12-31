import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    'trade_date': ['20230901', '20230904', '20230905', '20230906', '20230907', '20230908', '20230911', '20230912', '20230913'
                  , '20230914', '20230915', '20230918', '20230919', '20230920', '20230921', '20230922', '20230925', '20230926'
                  , '20230927', '20230928'],
    'close': [11.32, 11.56, 11.39, 11.43, 11.33, 11.27, 11.34, 11.28, 11.25, 11.29, 11.22, 11.23, 11.21, 11.15, 11.05
              , 11.24, 11.22, 11.16, 11.17, 11.20],
    'avg_10': [11.295, 11.271, 11.295, 11.297, 11.315, 11.335, 11.339, 11.321, 11.318, 11.330, 11.346, 11.336, 11.303
               , 11.285, 11.257, 11.229, 11.226, 11.214, 11.202, 11.194]},
    index=np.flip(np.arange(0, 20, 1), 0)

)

# print(df)

# fig = plt.figure(1, (15, 10))
# ax = fig.add_subplot(111)
#
# ax.plot(df['trade_date'], df['close'], 'b-', label='close')
# ax.plot(df['trade_date'], df['avg_10'], 'r--', label='avg_10')
#
# ax.set_ylim([8, 12])
# ax.set_xticks(['20230901', '20230911', '20230919', '20230927'])
# ax.legend(loc=3)
# fig.show()

df['avg_5'] = df['close'].rolling(5, closed='left').mean()
df['avg_10'] = df['close'].rolling(10, closed='left').mean()
# df = df.loc[9:0]


# print(df)

df = df.drop(['avg_5'], axis=1)
print(df)
print(df[1:3])
print(df[-2:-1])
