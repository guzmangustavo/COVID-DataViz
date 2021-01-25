from data import df_covid_global
import plotly.express as px
from plotly.offline import plot

# Choroplet Map
fig = px.choropleth(
    df_covid_global.query("Fecha == Fecha.max()"),
    locations="Pais",
    locationmode="country names",
    color="Confirmados",
    hover_name="Pais",
    hover_data={
        "Confirmados": True,
        "Fallecidos": True,
        "Pais": False
    },
    color_continuous_scale=px.colors.sequential.Sunset
)

fig.update_layout(
    title_text="Casos confirmados de COVID-19 a nivel mundial al " +
               f"{''.join(['0', str(df_covid_global.Fecha.max().day)]) if len(str(df_covid_global.Fecha.max().day)) == 1 else df_covid_global.Fecha.max().day}" +
               "/" +
               f"{''.join(['0', str(df_covid_global.Fecha.max().month)]) if len(str(df_covid_global.Fecha.max().month)) == 1 else df_covid_global.Fecha.max().month}" +
               "/" +
               f"{''.join(str(df_covid_global.Fecha.max().year))}",
    annotations=[
        dict(
            showarrow=False,
            text="Fuente: Johns Hopkins CSSE",
            xanchor='right',
            x=0.85,
            yanchor='top',
            y=-0.05
        ),
        dict(
            showarrow=False,
            text="por Gustavo Guzmán",
            xanchor='right',
            x=0.85,
            yanchor='top',
            y=-0.10
        )
    ],
    geo_scope="world"
)
plot(fig)
