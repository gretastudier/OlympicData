import pandas as pd
from math import pi

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
from bokeh.models import BoxSelectTool, ColumnDataSource, HoverTool,  CDSView, IndexFilter, Title, Label

#Years String
# yrs = oo_Year_Gender.Year
# yrs=yrs.apply(str)
# yrs = yrs.tolist()
x = oo_Year_Gender.Year   #x data: years

#Figure Stuff
p = figure(x_range=[1895, 2009], y_range=[-10, 1300], x_axis_label='Year', y_axis_label='Medal Count',  #"pan,box_zoom,reset,save,hover"
            title="Total Medal Count by Gender per Year")

#Filter Data for World War cancellation
view = CDSView(filters=[IndexFilter([0,1,2,3,4,6,7,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])])
patch1 =p.patch(x=[1912, 1912, 1920, 1920], y=[-10, 1300, 1300, -10], color='white', alpha=0.22, line_width=0)
patch2 = p.patch(x=[1936, 1936, 1948, 1948], y=[-10, 1300, 1300, -10], color='white', alpha=0.22, line_width=0)
p.add_tools(HoverTool(renderers=[patch1], tooltips=[("Year", "@x"),
                                                    ("Cancellation", "World War 1"),]))

#Women
y = oo_Year_Gender.Women
p.line(x=x, y=y, line_width=3, color = "#cc99ff", alpha=0.5, legend="Womens Medal Count", view=view)
c1 = p.circle(x=x, y=y, color='#cc99ff', fill_color="#cc99ff", size=6, legend="Womens Medal Count", view=view)
p.add_tools(HoverTool(renderers=[c1], tooltips=[("Years", "@x"),
                                                 ("Women", "@y"),]))
# #Men
y = oo_Year_Gender.Men
p.line(x=x, y=y,  line_width=3, color = "#33cc33", alpha=0.5, legend="Mens Medal Count", view=view)
c2 = p.circle(x=x, y=y,  color='#33cc33', fill_color="#33cc33", size=6, legend="Mens Medal Count", view=view)
p.add_tools(HoverTool(renderers=[c2], tooltips=[("Years", "@x"),
                                                ("Men", "@y"),]))

#Grid and Labels
p.grid.grid_line_color = "#808080"

p.background_fill_color = "#404040"
p.background_fill_alpha = 0.95
p.title.text_font_size = '20px'
p.add_layout(Title(text="The 1916, 1940, and 1944 Olympic Games were canceled due to World War I and II.", align="center"), "above")
p.xaxis.major_label_orientation = pi/4

#p.xaxis.axis_label = 'Years'

#Add Label to WW blocks:
# citation1 = Label(x=60, y=110, x_units='screen', y_units='screen', text_font_size = '15px',
#                  text='World War I', render_mode='css', text_alpha=0.7)
# citation2 = Label(x=180, y=150, x_units='screen', y_units='screen', text_font_size = '15px',
#                  text='World War II', render_mode='css', text_alpha=0.7)
# p.add_layout(citation1)
# p.add_layout(citation2)


output_file("olympicdata.html")
show(p)