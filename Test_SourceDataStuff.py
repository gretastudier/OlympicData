import pandas as pd

oo = pd.read_csv('/Users/gretastudier/PycharmProjects/OlympicData/SummerOlympicmedallists1896to2008.csv')
#add skiprows=4 to pd.read_cvs to skip 4 first rows
#can use read_excel()

# oo_Beijing = oo[oo.Edition == 2008].sort_values('NOC')
# oo_Athens = oo[oo.Edition == 1896].sort_values('Gender', ascending=False)
# oo_Athens.head(20)
# oo_Athens.Gender.value_counts(ascending=True)

#Men vs women competitors graph
oo_Year_Gender = pd.DataFrame()
oo_Year_Gender['Year'] = ""
oo_Year_Gender['Men'] = ""
oo_Year_Gender['Women'] = ""

#loop for adding metal counts for women and men per year
for i in range(0, 29):
    year = 1896 + i * 4
    oo_Year = oo[oo.Edition == (year)].sort_values('Gender', ascending=False)

    oo_Year_Gender.loc[i, 'Year'] = year                          #Year series
    m_f = oo_Year.Gender.value_counts()
    if m_f.shape[0] == 2:                                         #if both men and women are competing
        men = oo_Year[oo_Year.Gender == 'Men']
        men = men.Gender.value_counts()
        women = oo_Year[oo_Year.Gender == 'Women']
        women = women.Gender.value_counts()         #Series
        oo_Year_Gender.loc[i, 'Men'] = men.loc['Men']
        oo_Year_Gender.loc[i, 'Women'] = women.loc['Women']
    elif m_f.shape[0] == 1:                                       #if only men are competing
        women = 0
        men = oo_Year[oo_Year.Gender == 'Men']
        men = men.Gender.value_counts()
        oo_Year_Gender.loc[i, 'Men'] = men.loc['Men']
        oo_Year_Gender.loc[i, 'Women'] = women
    else:                                                         #if neither compete
        women=0
        men=0
        oo_Year_Gender.loc[i, 'Men'] = men
        oo_Year_Gender.loc[i, 'Women'] = women
print oo_Year_Gender.head()

#Graph
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.models import BoxSelectTool, ColumnDataSource, HoverTool

data_source = ColumnDataSource(data=oo_Year_Gender)
#Years String
yrs = oo_Year_Gender.Year
yrs=yrs.apply(str)
yrs = yrs.tolist()
x = oo_Year_Gender.Year   #x data: years



#Figure Stuff
p = figure(x_range=[1895, 2009], y_range=[-10, 1300], x_axis_label='Year', y_axis_label='Medal Count',  #"pan,box_zoom,reset,save,hover"
            title="Total Medal Count by Gender per Year")
p.title.text_font_size = '20px'
#Women
#y = oo_Year_Gender.Women

# t1 = x[0:5]
# t2 = x[6:11]
# t3 = x[13:28]
# y1 = y[0:5]
# y2 = y[6:11]
# y3 = y[13:28]
# print t1, y1
# nan=float('nan')
# print nan

#p.line(x=x, y=[[t1, t2, t3 ],[y1, y2, y3]],  line_width=3, color = "navy", alpha=0.3, legend="Womens Medal Count")
p.line(x='Years', y='Women', line_width=3, color = "navy", alpha=0.3, legend="Womens Medal Count", source=data_source)

c1 = p.circle(x='Years', y='Women', color='navy', fill_color="white", size=6, legend="Womens Medal Count", source=data_source)
# p.add_tools(HoverTool(renderers=[c1], tooltips=[("Years", "@x"),
#                                                  ("Women", "@y"),]))
# #Men
# y = oo_Year_Gender.Men
# p.line(x=x, y=y,  line_width=3, color = "green", alpha=0.3, legend="Mens Medal Count")
# c2 = p.circle(x=x, y=y,  color='green', fill_color="white", size=6, legend="Mens Medal Count")
# p.add_tools(HoverTool(renderers=[c2], tooltips=[("Years", "@x"),
#                                                 ("Men", "@y"),]))
p.patch(x=[1915, 1915, 1917, 1917], y=[-10, 1300, 1300, -10], color='black', alpha=0.2, line_width=0)
p.patch(x=[1939, 1939, 1945, 1945], y=[-10, 1300, 1300, -10], color='black', alpha=0.2, line_width=0)

#Grid Color
p.grid.grid_line_color = "white"
p.background_fill_color = "#e2ddd5"
p.background_fill_alpha = 0.4


output_file("olympicdata.html")
show(p)