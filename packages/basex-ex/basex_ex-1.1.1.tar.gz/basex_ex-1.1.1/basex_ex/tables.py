### Need a name
###
### BASEX module for heatmaps and tables creation


# Imports
import pandas as pd
import numpy as np
import ada
import bender

# Lista de todas as funções implementadas que podem ser
# importadas  com "from tables import *"
_all = ['', '', '']


def hierarchical_heatmap(df: pd.DataFrame, column_indexes: list, target_variables: list,
                         variables_type: str, min_conf: int = 5, min_conf_value=np.nan,
                         add_heatmap: bool = False, decimal_places: int = 1, **kwargs):
    """
    Descrição da função, contendo objetivo, explicações de condicionais,
    corner cases e o que mais for relevante para que o usuário saiba como
    ulitizar a função.

    Parameters
    ----------
    df : tipo_do_parametro
        Explicação do parâmetro
    df : tipo_do_parametro
        Explicação do parâmetro
    mode : str, default = 'valor_especifico'


    Returns
    -------
    tipo_do_retorno
        Explicação do retorno

    Raises
    ------
    Erros levantados, se houver

    Notes (opcional)
    -----
    Outras informações que possam ser relevantes, opcional.

    Examples
    --------
    >>> nome_da_função(par1)
    retorno
    >>> nome_da_função(par1, par2)
    retorno
    """

    # Defines max_value
    if variables_type == 'nps':
        max_value = 10
    elif variables_type == 'favorability':
        max_value = 5

    # Take columns of interest from the original df
    heat = df[target_variables + column_indexes].copy()
    heat = heat.replace('-', np.nan)

    # Adds count for further filter
    final = heat.groupby(column_indexes)[target_variables[0]].count() \
        .reset_index().rename(columns={target_variables[0]: 'values'})
    final[f'level_{str(len(column_indexes))}'] = 'count'

    # Adds total metric, either nps or favorability
    if kwargs.get('total'):
        metric = heat.groupby(column_indexes)[target_variables] \
            .apply(lambda x: ada.favorability_nps_calculation_df(x, max_value)) \
            .reset_index().rename(columns={target_variables[0]: 'values'})
        metric[f'level_{str(len(column_indexes))}'] = 'total'
        final = pd.concat([final, metric]).round(decimal_places)

    # Adds percentages of promoters, neutrals and detractors
    if kwargs.get('percentages'):
        perc = heat.groupby(column_indexes)[target_variables] \
            .apply(lambda x: ada.favorability_nps_percentages_df(x, max_value)) \
            .rename(columns={0: 'values'}).reset_index()
        final = pd.concat([final, perc])

    # Adds conversion
    if kwargs.get('conversion'):
        conv = (heat.groupby(column_indexes)[target_variables[0]].count() * 100 / len(heat)) \
            .reset_index().rename(columns={target_variables[0]: 'values'}).round(decimal_places)

        conv[f'level_{str(len(column_indexes))}'] = 'conversion'
        final = pd.concat([final, conv]).round(decimal_places)

        # Transform df format into pivot table
    final = final.pivot_table(index=column_indexes, values='values',
                              columns=f'level_{str(len(column_indexes))}',
                              aggfunc='first').reset_index().round(decimal_places)

    # Parse dicts
    if kwargs.get('percentages'):
        for i in target_variables:
            data = pd.json_normalize(final[i])
            if len(target_variables) > 1:
                data.columns = [f"{i} - {col}" for col in data.columns]
            final = pd.concat([final, data], axis=1)
        final = final[final.columns.drop(target_variables).tolist()]

    # Hide values if the group does not meet the confidentiality minimum
    keep = column_indexes + ['count', 'conversion']
    final.loc[final['count'] < min_conf, [c for c in final.columns if c not in keep]] = min_conf_value

    # Keep or drop count column
    if not kwargs.get('count'):
        final.drop('count', axis=1, inplace=True)

    # Send conversion to bottom
    if kwargs.get('conversion'):
        final = final[[c for c in final.columns if c != 'conversion'] + ['conversion']]

    # Rename columns
    if variables_type == 'favorability':
        name_dict = {'perc_favorable': 'Favoráveis',
                     'perc_neutral': 'Neutros',
                     'perc_non_favorable': 'Não favoráveis'}
    else:
        name_dict = {'perc_favorable': 'Promotores',
                     'perc_neutral': 'Neutros',
                     'perc_non_favorable': 'Detratores'}
    name_dict.update({'count': 'Respostas'})
    name_dict.update({'total': 'Total'})
    name_dict.update({'conversion': 'Representatividade'})

    final = final.rename(columns=lambda x: bender.rename_columns(x, name_dict))
    original_columns = final.columns

    # Round values and transpose df
    pivo = final.pivot_table(index=column_indexes, aggfunc='first', dropna=False)
    pivo = pivo.reindex(columns=[c for c in original_columns if c not in pivo.index.names])
    pivo = pivo.round(decimal_places).transpose()

    return pivo
