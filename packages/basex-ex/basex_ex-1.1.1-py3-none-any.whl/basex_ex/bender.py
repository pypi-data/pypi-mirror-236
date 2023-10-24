### Bender - Biblioteca de ENcapsulamento de Dados e Extrações Recorrentes
### BASEX module for ELT and data prep

# Imports
import pandas as pd
import re

# Lista de todas as funções implementadas que podem ser
# importadas  com "from bender import *"
_all = ['', '', '']


def preprocess_grouping(df: pd.DataFrame, grouping: dict):
    """
    *Created by ChatGPT on 01/09/2023.
    Groups data into new categories, creating new columns in the received
    DataFrame according to the info in the dict.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be preprocessed.
    groupings : dict
        3 level dict containing the original columns to be considered,
        and the new values - original values mapping.

    Returns
    -------
    pd.DataFrame
        Received DataFrame with the new categorical columns

    Notes
    -----
    Dict example:
    {
    column_a:
        {new_column_name:
            {new_value_1:
                [old_value_1, old_value_2],
            new_value_2:
                [old_value_3, old_value_4]}
        },
    column_b:
        {new_column_name:
            {new_value_1:
                [old_value_1, old_value_2],
            new_value_2:
                [old_value_3, old_value_4]}
        }
    ...
    }
    """
    # Create a copy of the original DataFrame to avoid modifying it directly
    df_copy = df.copy()

    # Loop through the grouping dictionary
    for column, new_columns in grouping.items():
        for new_column_name, mapping in new_columns.items():
            # Create a new column and initialize it with the original values
            df_copy[new_column_name] = df_copy[column]
            for new_value, old_values in mapping.items():
                # Update the new column based on the mapping
                df_copy[new_column_name] = df_copy[new_column_name].replace(old_values, new_value)

    return df_copy


def clean_column(df: pd.DataFrame, column_to_clean: str, keep_values: list, replacement_value: str) -> pd.DataFrame:
    """
    *Created by ChatGPT on 01/09/2023.
    Clean a specific column in a DataFrame by keeping specified values and replacing others.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.
    column_to_clean : str
        Name of the column to be cleaned.
    keep_values : list
        List of values to be kept in the specified column.
    replacement_value : str
        Value to replace any other value in the column.

    Returns
    -------
    pd.DataFrame
        DataFrame with the specified column cleaned.

    Examples
    --------
    >>> data = {'A': ['apple', 'banana', 'cherry', 'date', 'fig']}
    >>> df = pd.DataFrame(data)
    >>> df_cleaned = clean_column(df, 'A', ['apple', 'banana', 'cherry'], 'other')
    >>> print(df_cleaned)
          A
    0   apple
    1  banana
    2  cherry
    3   other
    4   other
    """
    # Create a copy of the DataFrame to avoid modifying it directly
    df_copy = df.copy()

    # Use the `replace` method to clean the specified column
    df_copy[column_to_clean] = df_copy[column_to_clean].apply(lambda x: x if x in keep_values else replacement_value)

    return df_copy

def rename_columns(column_name, name_dict):
    for pattern, replacement in name_dict.items():
        column_name = re.sub(pattern, replacement, column_name)
    return column_name
