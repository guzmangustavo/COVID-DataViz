from functools import reduce
import pandas as pd


def dataWrangling(dataset, column_name):
    dataset.rename(columns={"Country/Region": "Pais"}, inplace=True)
    dataset = pd.melt(
        dataset,
        id_vars=["Province/State", "Pais", "Lat", "Long"],
        var_name="Fecha",
        value_name=column_name
    )
    dataset["Fecha"] = dataset["Fecha"].astype("datetime64[ns]")
    dataset = dataset.sort_values(
        ["Fecha", "Pais"],
        ascending=True
    ).groupby(
        ["Pais", "Fecha"]
    ).sum()
    return dataset


def resetIndex(dataset):
    dataset = dataset.reset_index(level=["Pais", "Fecha"])
    return dataset


def removeMissingData(dataset):
    dataset = dataset.query("Pais != 'Diamond Princess' & \
                        Pais != 'Kosovo' & \
                        Pais != 'MS Zaandam'"
                            )
    return dataset


df_confirmados = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
df_fallecidos = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
df_recuperados = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

# Data wrangling
df_confirmados = dataWrangling(df_confirmados, "Confirmados")
df_fallecidos = dataWrangling(df_fallecidos, "Fallecidos")
df_recuperados = dataWrangling(df_recuperados, "Recuperados")

# Removing missing data
df_confirmados = removeMissingData(df_confirmados)
df_fallecidos = removeMissingData(df_fallecidos)
df_recuperados = removeMissingData(df_recuperados)

# Data unification
dataframes = [df_confirmados, df_recuperados, df_fallecidos]
df_covid_global = reduce(
    lambda left, right: pd.merge(left, right, on=["Pais", "Fecha"]), dataframes)
df_covid_global.drop(["Lat_x", "Long_x", "Lat_y", "Long_y"], axis=1,
                     inplace=True)

# Reset index
df_covid_global = resetIndex(df_covid_global)
df_confirmados = resetIndex(df_confirmados)
df_fallecidos = resetIndex(df_fallecidos)
df_recuperados = resetIndex(df_recuperados)

# Columns reordering
df_covid_global = df_covid_global[
    ["Pais", "Fecha", "Lat", "Long", "Confirmados", "Recuperados",
     "Fallecidos"]
]

# Argentina dataframe
df_covid_argentina = df_covid_global.query("Pais == 'Argentina'")
