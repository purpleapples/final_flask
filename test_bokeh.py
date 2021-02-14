import numpy as np
import pandas as pd
import pandas_bokeh
from bokeh.embed import json_item
"""
:param YearweekNum: 년도+주차숫자
:return: 통계시각화데이터
"""
x = np.arange(10)
y = np.arange(10)
df = pd.DataFrame([x, y])
df = df.T
df.columns = ['x', 'y']
plot = json_item(df.plot_bokeh(kind='scatter'))
print(plot)