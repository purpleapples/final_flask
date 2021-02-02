def save_bokeh_json():
    import bokeh
    import pandas_bokeh
    from bokeh.io import show
    from bokeh.embed import json_item
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.layouts import gridplot
    import pandas as pd
    import numpy as np
    import json
    #from selenium import webdriver

    xy = np.arange(20)
    xy_df = pd.DataFrame(xy)
    p =xy_df.plot_bokeh()

    #show(p)

    print(json.dumps(json_item(p)))

save_bokeh_json()


