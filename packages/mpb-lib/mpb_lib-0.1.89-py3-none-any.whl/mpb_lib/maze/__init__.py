#coding:utf-8
# 10×10のリストに01で表現された迷路を表示するプログラム
#
# Copyright (c) 2023 Atsush Shibata(shivata@m-info.co.jp)
#
# Released under the MIT license.

from string import Template
from IPython.display import display, HTML

try:
    from google.colab.output import eval_js
    HTML_fook = HTML
    display_hook = display


except:
    from IPython.display import IFrame
    from IPython.display import FileLink
    def eval_js(js):
        body = HTML(f"""<script>
        {js}
        </script>""")
        display(body)


    def HTML_fook(body):
        f = open('./tmp.html', 'w')
        f.write(body)
        f.close()

    def display_hook(html):
        display(IFrame('./tmp.html', width="100%", height="400px"))



HTML_TEMPLATE = """
<style>
#maze {
    font-family: 'Liberation Serif', 'Noto Sans CJK JP',  /* Linux/Android/ChromeOS */
        'TakaoGothic', 'VL Gothic',  /* Debian/Ubuntu */
        'Yu Gothic', 'MS Gothic',  /* Windows */
        'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Osaka-Mono',  /* Mac/iOS */
        'Noto Sans JP', Monospace;
    font-size: 12pt;
    line-height: 1em;
}
</style>

<div id="maze">
${body}
</div>
"""

def show_maze(maze_list):
    """
    10×10のリストで表現された迷路を表示する
    """
    maze_str = "" # 迷路の文字列を初期化
    for line in maze_list:
        line_str = ""  # 迷路の文字列(一列)を初期化
        for block in line:
            if block == 1:
                line_str += "■"
            elif block == 0:
                line_str += "　"
            else:
                line_str += "&#"+str(9310+block)+";"
        maze_str += line_str+"<br/>\n"

    html_source = Template(HTML_TEMPLATE)

    html_body = HTML_fook(html_source.substitute({'body':maze_str}))
    display_hook(html_body)


def show_route(maze_list, route_list):
    """
    最短経路を表示
    """
    maze_str = "" # 迷路の文字列を初期化
    for y in range(10):
        line_str = ""
        for x in range(10):
            if maze_list[y][x] == 1:
                line_str += "■"
            else:
                if [x, y] in route_list:
                    idx = route_list.index([x, y])
                    line_str += "&#"+str(9310+idx+2)+";"
                else:
                    line_str += "　"
        maze_str += line_str+"<br/>\n"

    html_source = Template(HTML_TEMPLATE)

    html_body = HTML_fook(html_source.substitute({'body':maze_str}))
    display_hook(html_body)
