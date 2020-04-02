import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

df = px.data.gapminder()
fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60, title='GDP Per Capita')

df2 = px.data.gapminder()
gdp = df['pop'] * df['gdpPercap']
fig2 = px.bar(df2, x='year', y=gdp, color='continent', labels={'y':'gdp'},
             hover_data=['country'],
             title='Evolution of world GDP')

layout = html.Div([
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig)
])

