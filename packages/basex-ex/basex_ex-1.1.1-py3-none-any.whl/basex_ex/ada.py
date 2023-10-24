### ADA - Algorithms for Data Arithmetics
### A tribute to Ada Lovelace
### BASEX module for basic calculations in EX context


# Imports
import numpy as np
import pandas as pd
from scipy import stats
from datetime import date


# Lista de todas as funções implementadas que podem ser
# importadas  com "from ada import *"
_all = ['', '', '']


def favorability_nps_calculation(values, max_value=5):
    """
    Calculate the favorability or NPS of an array of scores
    according to the maximum value in `max_value`.
    If ``max_value = 5`` or 7, it'll treat `values` as favorability values;
    if ``max_value = 10``, it'll treat `values` as nPS values.
    Return NaN for an empty array

    Parameters
    ----------
    values : array-like (np.array or pd.Series)
        The numerical array os scores
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    Float
        Favorability or NPS score
    """

    n_answers = values.size
    if n_answers == 0:
        return np.nan

    assert (max_value == 5 or max_value == 7 or max_value == 10)

    if max_value == 5:
        assert (max(values) <= 5)
        favorable_values = values[values >= 4]
        perc_favorability = 100 * len(favorable_values) / n_answers
    elif max_value == 7:
        assert (max(values) <= 7)
        favorable_values = values[values >= 6]
        perc_favorability = 100 * len(favorable_values) / n_answers
    elif max_value == 10:  # NPS
        favorable_values = len(values[values >= 9]) - len(values[values <= 6])
        perc_favorability = 100 * favorable_values / n_answers

    return perc_favorability


def favorability_nps_calculation_df(df_values, max_value=5):
    """
    Calculate the favorability or the NPS for all columns
    of a DataFrame. Favorability and NPS variables are discriminated
    according to the maximum value in `max_value`.
    All columns must have only favorability questions or only NPS questions, not both.

    Parameters
    ----------
    df_values : pd.DataFrame
        DataFrame with all numeric columns
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    pd.Series
        Favorability or NPS score for each column of `df_values`
    """

    df_favorabilities = df_values.apply(lambda x: favorability_nps_calculation(x.dropna(), max_value=max_value), axis=0)

    return df_favorabilities


def favorability_nps_percentages(values, max_value=5):
    """
    Calculate the percentage of promoters (or favorables),
    neutrals and detractors (or non favorables) of an array of scores
    according to the maximum value in `max_value`.
    If ``max_value = 5`` or 7, it'll treat `values` as favorability values;
    if ``max_value = 10``, it'll treat `values` as nPS values.
    Return NaN for an empty array

    Parameters
    ----------
    values : array-like (np.array or pd.Series)
        The numerical array os scores
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    Dict
        Percentages of promoters (or favorables),
        neutrals and detractors (or non favorables)
    """

    n_answers = values.size
    if n_answers == 0:
        return np.nan

    assert (max_value == 5 or max_value == 7 or max_value == 10)

    if max_value == 5:
        assert (max(values) <= 5)
        favorable_values = values[values >= 4]
        neutral_values = values[values == 3]
        non_favorable_values = values[values <= 2]
        perc_favorable = 100 * len(favorable_values) / n_answers
        perc_neutral = 100 * len(neutral_values) / n_answers
        perc_non_favorable = 100 * len(non_favorable_values) / n_answers
    elif max_value == 7:
        favorable_values = values[values >= 6]
        neutral_values = values[values == 5]
        non_favorable_values = values[values <= 4]
        perc_favorable = 100 * len(favorable_values) / n_answers
        perc_neutral = 100 * len(neutral_values) / n_answers
        perc_non_favorable = 100 * len(non_favorable_values) / n_answers
    elif max_value == 10:  # NPS
        favorable_values = values[values >= 9]
        neutral_values = values[(values == 8) | (values == 7)]
        non_favorable_values = values[values <= 6]
        perc_favorable = 100 * len(favorable_values) / n_answers
        perc_neutral = 100 * len(neutral_values) / n_answers
        perc_non_favorable = 100 * len(non_favorable_values) / n_answers

    percentages = {'perc_favorable': perc_favorable,
                   'perc_neutral': perc_neutral,
                   'perc_non_favorable': perc_non_favorable}

    return percentages


def favorability_nps_percentages_df(df_values, max_value=5):
    """
    Calculate the percentage of promoters (or favorables),
    neutrals and detractors (or non favorables) for all columns
    of a DataFrame. Favorability and NPS variables are discriminated
    according to the maximum value in `max_value`.
    All columns must have only favorability questions or only NPS questions, not both.

    Parameters
    ----------
    df_values : pd.DataFrame
        DataFrame with all numeric columns
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    pd.Series
        Percentage of promoters (or favorables),
        neutrals and detractors (or non favorables)
        for each column of `df_values`
    """
    df_percentages = df_values.apply(lambda x: favorability_nps_percentages(x.dropna(), max_value=max_value))
    df_percentages = pd.DataFrame(df_percentages)

    return df_percentages


def enps_confidence_interval(values, c_level):
    """
    Evalute the NPS confidence interval according to https://measuringu.com/nps-confidence-intervals/.
    Method: adjusted-wald (3,T).

    Parameters
    ----------
    values : array-like
        The eNPS values.
    c_level : float
        The confidence level.

    Returns
    -------
    l_bound : float
        The lower bound of the confidence level.
    u_bound : float
        The upper bound of the confidence level.
    enps : float
        The eNPS.
    """

    n = len(values)  # sample size
    n_detractors = values[values <= 6].count()
    n_promoters = values[values >= 9].count()
    # n_passives = n_detractors = values[(values>6) & (values<9)].count()
    enps = (n_promoters - n_detractors) / n

    adj_n = n + 3
    adj_n_detractors = n_detractors + 3 / 4
    adj_n_promoters = n_promoters + 3 / 4

    adj_prop_promoters = adj_n_promoters / adj_n
    adj_prop_detractors = adj_n_detractors / adj_n
    adj_enps = adj_prop_promoters - adj_prop_detractors

    adj_var = adj_prop_promoters + adj_prop_detractors - (adj_prop_promoters - adj_prop_detractors) ** 2
    adj_se = np.sqrt(adj_var / adj_n)
    z_value = stats.norm.ppf(c_level)
    moe = z_value * adj_se

    l_bound = adj_enps - moe
    u_bound = adj_enps + moe

    return l_bound, u_bound, enps, moe*100


def enps_confidence_interval2(values, delta):
    n = len(values)  # sample size
    n_detractors = values[values <= 6].count()
    n_promoters = values[values >= 9].count()
    # n_passives = n_detractors = values[(values>6) & (values<9)].count()
    enps = (n_promoters - n_detractors) / n
    print(enps)
    adj_n = n + 3
    adj_n_detractors = n_detractors + 3 / 4
    adj_n_promoters = n_promoters + 3 / 4

    adj_prop_promoters = adj_n_promoters / adj_n
    adj_prop_detractors = adj_n_detractors / adj_n
    # adj_enps = adj_prop_promoters - adj_prop_detractors

    adj_var = adj_prop_promoters + adj_prop_detractors - (adj_prop_promoters - adj_prop_detractors) ** 2
    adj_se = np.sqrt(adj_var / adj_n)

    # l_bound = adj_enps - delta
    # u_bound = adj_enps + delta

    # code

    # stat.norm.cdf(1.64)
    z_value = delta / adj_se
    c_level = stats.norm.cdf(z_value)

    return c_level

def run_date(numbered_month=False):
    """
    Returns the current date in a specific format.

    Parameters
    ----------
        numbered_month (bool): if True, returns month as numeral

    Returns
    -------
        str: Current date in the specified format.
    """
    data_atual = date.today()
    ano = data_atual.year
    mes = data_atual.month
    meses = {1: 'Janeiro',
             2: 'Favereiro',
             3: 'Março',
             4: 'Abril',
             5: 'Maio',
             6: 'Junho',
             7: 'Julho',
             8: 'Agosto',
             9: 'Setembro',
             10: 'Outubro',
             11: 'Novembro',
             12: 'Dezembro'}

    if numbered_month:
        return f'{mes}/{ano}'

    return f'{meses[mes]}, {ano}'
