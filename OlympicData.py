import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.charts import Donut, show, output_file, TimeSeries
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.palettes import Spectral5

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
from bokeh.plotting import figure, output_file, show
yrs = oo_Year_Gender.Year

yrs=yrs.apply(str)
yrs = yrs.tolist()
print yrs
#print yrs.apply(str)

for i in range(29):
    if oo_Year_Gender.loc[i, 'Men'] == 0:
        oo_Year_Gender.drop([i], axis=0, inplace=True)
        print "Hello"


x = oo_Year_Gender.Year
y1 = oo_Year_Gender.Women#(columns=["Women"])
y2 = oo_Year_Gender.Men#(columns=['Men'])

#Data Stuff
TOOLS = [ HoverTool()]
p = figure(plot_width=600, plot_height=600, title="Overall Medal Count by Gender", tools=TOOLS)# , x_range=Range1d(1896, 2008))#, x_range=yrs,)  #x_range = x,
p.line(x, y1, line_width=3, color = "navy", alpha=0.3, legend="Womens Medal Count")
p.line(x, y2, line_width=3, color = "green", alpha=0.3, legend="Mens Medal Count")
p.circle(x, y1, color='navy', fill_color="white", size=6, legend="Womens Medal Count")
p.circle(x, y2, color='green', fill_color="white", size=6, legend="Mens Medal Count")
p.patch(x=[1915.4, 1915.4, 1916.6, 1916.6], y=[0, 1300, 1300, 0], color='black', alpha=0.5)
p.patch(x=[1939.4, 1939.4, 1944.6, 1944.6], y=[0, 1300, 1300, 0], color='black', alpha=0.5)
#Text Stuff
#p.title.text_font_size = '25px'
p.xaxis.axis_label = 'Year'
#p.xaxis.axis_label = '*data for the years of '
p.yaxis.axis_label = 'Medal Count'


# p.select_one(HoverTool).tooltips = [
#      ('Women', '@Women'),
#      ('Men', '@Men'),
# ]


# source = ColumnDataSource(
#         data=dict(
#             x=yrs,
#             y=yrs,))
#
# hover = HoverTool(
#         tooltips=[
#             ("index", "$index"),
#             ("(x,y)", "($x, $y)"),])

# hover = p.select(dict(type=HoverTool))
# hover.tooltips = [
#     # add to this
#     ("(x,y)", "($x, $y)"),
# ]

output_file("olympicdata.html")
show(p)









#Tutorial
oo_Beijing[['NOC','Medal', 'Edition']]  #grabs three series in dataframe
type(oo_Beijing)
oo.info() #gives info if there is missing data in dataframe
print oo_Beijing.Medal.value_counts()

#ValueCounts
oo.Edition.value_counts()  #how many times a value is repeated in Edition Series with most repeated showing first
#how many medals were won in each olympic year

print oo.Gender.value_counts()













#graph attempt using Bokeh Donut
top = pd.DataFrame()
top['Medal Count'] = oo_Beijing['NOC'].value_counts()[oo_Beijing['NOC'].value_counts()>=100]   #makes Series of countries with top metal counts
top['NOC'] = top.index
#top.columns = ['Nation', 'Medal Count']    #column names
#top = top.to_frame(name=None).T
#top['Medal Count'] = top.T
#top = top.T
print top['Medal Count']

#Hover Stuff:
data = top['Medal Count']

source = ColumnDataSource(data=dict(desc=['A', 'b', 'C', 'd', 'E']))
hover = p.select(dict(type=HoverTool))
hover.tooltips = [("desc", "@desc")]  #,('Value of Total',' @Total')]

p = Donut(data, tools='hover', source=source, fill_color=Spectral5) #, label='Medal Count', values='Medal Count')#, tools='hover')
show(p)



