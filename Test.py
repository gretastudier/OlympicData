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



#Graph gender medal data
#from bokeh.plotting import figure, output_file, show
#from bokeh.models import HoverTool, BoxSelectTool, ColumnDataSource

from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.models import BoxSelectTool, ColumnDataSource, HoverTool

yrs = oo_Year_Gender.Year

yrs=yrs.apply(str)
yrs = yrs.tolist()
print yrs
#print yrs.apply(str)

for i in range(29):
    if oo_Year_Gender.loc[i, 'Men'] == 0:
        oo_Year_Gender.drop([i], axis=0, inplace=True)
        #print "Hello"

TOOLS="hover,save"

#source1 = ColumnDataSource(oo_Year_Gender[['Year', 'Women']])
#source2 = ColumnDataSource(oo_Year_Gender[['Year', 'Men']])

#CORRRECT?
# source = ColumnDataSource(data=dict(
#     x=oo_Year_Gender[['Year']],
#     y1=oo_Year_Gender[['Women']],
#     y2=oo_Year_Gender[['Men']],
# ))


# hover = HoverTool(
#     tooltips=[
#         #( 'City','@City'),
#         ( 'Year','@Year'),
#         ( 'Medal Count','@Women')],)
# hover2 = HoverTool(
#     tooltips=[
#         #( 'City','@City'),
#         ( 'Year','@Year'),
#         ( 'Medal Count','@Men')],)

x = oo_Year_Gender.Year
y1 = oo_Year_Gender.Women
y2 = oo_Year_Gender.Men

#source=ColumnDataSource(x,y1,y2)

#Data Stuff
#TOOLS = "hover, save"
p = figure(x_range=[1895, 2009], y_range=[-10, 1300], x_axis_label='Year', y_axis_label='Medal Count',  #"pan,box_zoom,reset,save,hover"
            title="Overall Medal Count by Gender", tools=TOOLS)
p.line(x=x, y=y1,  line_width=3, color = "navy", alpha=0.3, legend="Womens Medal Count")
p.line(x=x, y=y2,  line_width=3, color = "green", alpha=0.3, legend="Mens Medal Count")
p.circle(x=x, y=y1, color='navy', fill_color="white", size=6, legend="Womens Medal Count")
p.circle(x=x, y=y2,   color='green', fill_color="white", size=6, legend="Mens Medal Count")
p.patch(x=[1915, 1915, 1917, 1917], y=[-10, 1300, 1300, -10], color='black', alpha=0.2)
p.patch(x=[1939, 1939, 1945, 1945], y=[-10, 1300, 1300, -10], color='black', alpha=0.2)

# #Hover Stuff:
# hover = p.select_one(HoverTool).tooltips = [
#     ("Years", "@x"),
#     ("Women", "@y1"),
#     ("Men", "@y2"),
# ]

p.select_one(HoverTool).tooltips = [
     ('Year', '@x'),
     ('Women', '@y1'),
     ('Men', '@y2'),
]

#Grid Color
p.grid.grid_line_color = "white"
p.background_fill_color = "#e2ddd5"
p.background_fill_alpha = 0.4


output_file("olympicdata.html")
show(p)



#Text Stuff
#p.title.text_font_size = '25px'
#p.xaxis.axis_label = '*data for the years of '