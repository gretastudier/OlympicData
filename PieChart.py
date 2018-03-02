from numpy import pi
from random import shuffle
from math import sin,cos
from bokeh.plotting import ColumnDataSource, output_notebook, figure
from bokeh.charts import show, Donut
from bokeh.models import HoverTool, Text
#from bokeh.palettes import viridis as palette #@UnresolvedImport
#from bokeh import palettes
from bokeh.palettes import magma  #Spectral11
#from bokeh.palettes import Category20
import pandas as pd


#PIE CHART CLASS
class CustomPieBuilder:
    green ="#50ee70"
    red = "#ff7070"
    x_range = 1.1
    y_range = 1.1

    def __init__(self,df,label_name,column_name,tools='hover',tooltips=None,
                 reverse_color=False,colors=None,random_color_order=False,
                 plot_width=400,plot_height=400,title='Untitled',*args,**kwargs):
        p = self.setup_figure(tools,plot_width,plot_height,title)
        df = self.add_columns_for_pie_chart(df,column_name,colors,reverse_color,random_color_order)
        self.df = df
        self.plot_pie(p,df,label_name,*args,**kwargs)
        if tooltips:
            self.set_hover_tooltip(p,tooltips)

        self.add_text_label_on_pie(p,df,label_name)
        self.plot = p

    def setup_figure(self,tools,plot_width,plot_height,title):
        p = figure(
            x_range=(-self.x_range, self.x_range),
            y_range=(-self.y_range, self.y_range),
            tools=tools,
            plot_width=plot_width,
            plot_height=plot_height,
            title=title,
        )
        p.axis.visible = False
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        return p

    @staticmethod
    def plot_pie(p,df,label_name,*args,**kwargs):
        for key, _df in df.groupby(label_name):
            source = ColumnDataSource(_df.to_dict(orient='list'))
            p.annular_wedge(
                x=0,
                y=0,
                inner_radius=0,
                outer_radius=1,
                start_angle='starts',
                end_angle='ends',
                color='colors',
                source=source,
                legend=key,
                *args,**kwargs)

    @staticmethod
    def set_hover_tooltip(p,tooltips):
        hover = p.select({'type':HoverTool})
        hover.tooltips = tooltips

    @staticmethod
    def add_columns_for_pie_chart(df,column_name,colors=None,reverse_color=False,random_color_order=False):
        r = 0.7
        df = df.copy()
        column_sum = df[column_name].sum()
        df['percentage'] = (df[column_name]/column_sum)
        percentages = [0]  + df['percentage'].cumsum().tolist()
        df['starts'] = [p * 2 * pi for p in percentages[:-1]]
        df['ends'] = [p * 2 * pi for p in percentages[1:]]

        df['middle'] = (df['starts'] + df['ends'])/2
        df['text_x'] = df['middle'].apply(cos)*r
        df['text_y'] =df['middle'].apply(sin)*r
        df['text_angle'] = 0.0

        if colors:
            df['colors'] = colors
        else:
            if 'colors' not in df:
                reverse_color = -1 if reverse_color else 1
                #palette = magma(len(df))[::reverse_color]
                #palette = Spectral11
                colors = palettes.magma(len(df))[::reverse_color]
                if random_color_order:
                    shuffle(colors)
                df['colors'] = colors
        return df

    @staticmethod
    def add_text_label_on_pie(p,df,label_name):
        source=ColumnDataSource(df.to_dict(orient='list'))
        txt = Text(x="text_x", y="text_y", text=label_name, angle="text_angle",
               text_align="center", text_baseline="middle",
               text_font_size='10pt',)
        p.add_glyph(source,txt)

def build_plot(df,label_name,column_name,tools='hover',tooltips=None,
                 reverse_color=False,colors=None,random_color_order=False,
                 plot_width=400,plot_height=400,title='Untitled',*args,**kwargs):

    customPie = CustomPieBuilder(df,label_name,column_name,tools,tooltips,
                 reverse_color,colors,random_color_order,
                 plot_width,plot_height,title,*args,**kwargs)

    return customPie.plot

#CODE
d = {'posa': ['US','IT','FR','ES','DE','GB','CA','BE','AU','NL','NO','SE','DK'],
 'values': [4464, 989, 875, 824, 773, 733, 598, 307, 140, 132, 118, 112, 65]}
df = pd.DataFrame(d)

p = build_plot(
    df,
    'posa',
    'values',
    tooltips=[('percentage', '@percentage{0.00%}'), ('POSa', '@posa'), ('count','@values')],
    title='Testing',
    reverse_color=True,
    random_color_order=True,
    plot_height=700,
    plot_width=700)

show(p)