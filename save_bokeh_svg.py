def make_bokeh_to_svg():
    # module import
    import bokeh
    import pandas_bokeh
    from bokeh.io import show, export_svgs
    from bokeh.embed import json_item
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.layouts import gridplot
    from bokeh.embed import components
    from selenium import webdriver
    import pandas as pd
    import numpy as np
    import json

    # svg 파일 만들기위한 selenium headless driver 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(executable_path='./externallib/chromedriver.exe',
                          chrome_options=chrome_options)

    # plot 설정
    xy = np.arange(20)
    xy_df = pd.DataFrame(xy)

    figure = xy_df.plot_bokeh(kind='bar', title='xy')
    figure2 = xy_df.plot_bokeh(kind='bar', title='xy')
    figure.output_backend = 'svg'
    figure2.output_backend = 'svg'
    plot = gridplot([[figure, figure2]])
    #dir(figure)


    # html = file_html(plot, CDN, 'html_plot')
    # pandas_bokeh.output_file('chart.html')
    show(plot)
    export_svgs(plot, filename='plot.svg', webdriver=wd)


make_bokeh_to_svg()

