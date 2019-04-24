import pandas as pd



def data_country():
    countries = pd.read_csv('/Users/Bandeep/PycharmProjects/Gather/disease/countries/country.csv')

    countries['value'] = countries['value'].apply(lambda x: (x,x))

    #print(countries['value'].values)
    return tuple(countries['value'].values)



def get_country(abbreviation):
    countries = pd.read_csv( '/Users/Bandeep/PycharmProjects/Gather/disease/countries/country.csv' )

    abbre = countries['id'].values

    return countries['value'].values[list(abbre).index(abbreviation)]
