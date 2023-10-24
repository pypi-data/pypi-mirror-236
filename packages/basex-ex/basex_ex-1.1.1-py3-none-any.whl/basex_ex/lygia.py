### Lygia - Library for Graphics, Images and Art
### A tribute to Lygia Clark
### BASEX module for basic plots and graphics in EX context


# Imports
import pandas as pd
#from matplotlib_venn import venn2, venn2_circles
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Lista de todas as funções implementadas que podem ser
# importadas  com "from lygia import *"
_all = ['', '', '']


def grafico_barras(detalhamento, bar_color='#93c47d', benchmark=None, min_percentage=0, n_decimal_places=1,
                   text_fit=True, orientacao='horizontal', title='Título', keep_sorting=False):
    """
    Generates a bar chart based on the provided data.

    Parameters
    ----------
        detalhamento (pd.DataFrame): DataFrame containing the detailed data to generate the chart.
        bar_color (str, optional): Color of the bars in the chart. Default is '#93c47d'.
        benchmark (list, optional): List of alternatives to be highlighted with a different color. Default is None.
        min_percentage (float, optional): Minimum percentage to display an alternative in the legend. Default is 0.
        n_decimal_places (int, optional): Number of decimal places to display in the bar values. Default is 1.
        text_fit (bool, optional): Defines whether the text on the bars should fit the bar size. Default is True.
        orientacao (str, optional): Orientation of the chart. Can be 'vertical' (default) or 'horizontal'.
        keep_sorting (bool, optional): If True, keeps the original sorting from detalhamento.

    Returns
    -------
        matplotlib.pyplot: Object containing the generated bar chart.
    """

    # Filtrar as alternativas com percentual menor que min_percentage
    filtrado = detalhamento[(detalhamento['Percentual'] > min_percentage) |
                            (detalhamento['Alternativa'].isin(benchmark)) |
                            (detalhamento['Alternativa'].str.contains('\*'))]
    # Ordenar as alternativas em ordem decrescente de percentual
    if keep_sorting:
        df = filtrado.copy()
    else:
        df = filtrado.sort_values(by='Percentual', ascending=True)

    if benchmark is not None:
        # Verificar se os valores da coluna "Alternativa" estão presentes na lista "benchmark"
        condicao = df['Alternativa'].isin(benchmark)
        # Filtrar as linhas que correspondem aos valores da lista
        novo_df = df[condicao]
        # Remover as linhas do DataFrame original
        filt = df[~condicao]
        df = pd.concat([novo_df, filt], ignore_index=True)

    # Filtrar as alternativas com percentual menor que min_percentage para a legenda
    legenda = detalhamento[~detalhamento['Alternativa'].isin(filtrado['Alternativa'])]

    # Gerar as barras do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    if text_fit:
        n = 90
        df['Alternativa'] = df['Alternativa'].apply(lambda x: _add_line_breaks(x, n))
        legenda['Alternativa'] = legenda['Alternativa'].apply(lambda x: _add_line_breaks(x, n))
        if benchmark is not None:
            benchmark = [_add_line_breaks(i, n) for i in benchmark]

    # Definir eixo Y e eixo X conforme a orientação
    if orientacao == 'horizontal':
        y_pos = range(len(df))
        ax.barh(y_pos, df['Percentual'], color=bar_color)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df['Alternativa'], fontsize=18)
        ax.set_xticks([])  # Remover os valores no eixo X
    else:
        x_pos = range(len(df))
        ax.bar(x_pos, df['Percentual'], color=bar_color)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(df['Alternativa'], fontsize=18, rotation=0, ha='center')
        ax.set_yticks([])  # Remover os valores no eixo Y

    # Definir cor cinza para as alternativas presentes na lista de benchmark
    if benchmark is not None:
        for index, row in df.iterrows():
            if row['Alternativa'] in benchmark:
                if orientacao == 'horizontal':
                    ax.get_children()[index].set_color('#acacac')
                else:
                    ax.get_children()[index].set_color('#acacac')

    # Adicionar o valor da porcentagem no final de cada barra
    for i, v in enumerate(df['Percentual']):
        if orientacao == 'horizontal':
            ax.text(v, i, f'{v:.{n_decimal_places}f}%', color='black', ha='left', va='center', fontsize=15)
            # Adicionar a legenda das alternativas com percentual menor que min_percentage
            if legenda.shape[0] > 0:
                legenda_text = f'*Detalhamento:\n'
                for index, row in legenda.iterrows():
                    legenda_text += f'- {row["Alternativa"]}: {row["Percentual"]:.{n_decimal_places}f}%\n'

                plt.text(0, -0.1, legenda_text, transform=ax.transAxes, verticalalignment='top',
                         horizontalalignment='left',
                         fontsize=15, bbox=dict(facecolor='none', edgecolor='none'))
        else:
            ax.text(i, v, f'{v:.{n_decimal_places}f}%', color='black', ha='center', va='bottom', fontsize=15)
            if legenda.shape[0] > 0:
                legenda_text = f'*Detalhamento:\n'
                for index, row in legenda.iterrows():
                    legenda_text += f'- {row["Alternativa"]}: {row["Percentual"]:.{n_decimal_places}f}%\n'

                plt.text(1.2, -0.1, legenda_text, transform=ax.transAxes, verticalalignment='top',
                         horizontalalignment='center',
                         fontsize=15, bbox=dict(facecolor='none', edgecolor='none'))

    # Configurar os rótulos e o título
    ax.set_title(title, fontsize=20)

    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return plt


def generate_vertical_bar_chart(data, var_type, add_total=None, values_order=True, n_decimal_places=1, text_fit=True):
    """
       Generates a vertical bar chart based on the provided data.

       Parameters
       ----------
           data (list or pd.DataFrame): Data to be plotted on the bar chart.
           var_type (str): Type of variable to be plotted. Can be 'nps' (Net Promoter Score) or 'favorability'.
           add_total (str, optional): Alternative to be added as a totalizing bar. Default is None.
           values_order (bool or None, optional): Defines whether the values should be ordered. Default is True.
           n_decimal_places (int, optional): Number of decimal places to display in the bar values. Default is 1.
           text_fit (bool, optional): Defines whether the text on the bars should fit the bar size. Default is True.

       Returns
       -------
           matplotlib.pyplot: Object containing the generated vertical bar chart.
    """

    # Ordenar os valores, se necessário
    if values_order is not None:
        data = pd.DataFrame(data)
        data = data.sort_values(by='Percentual', ascending=False)

    # Paleta de cores
    colors = ['#93c47d', '#f1c232', '#0097a7', '#ee4c4a']

    # Verificar se há mais recortes do que cores disponíveis
    if len(data) > len(colors):
        repetitions = len(data) // len(colors) + 1
        colors = colors * repetitions

    # Adicionar barra para o total de respondentes, se necessário
    if add_total is not None:
        data = data.set_index('Alternativa').loc[[add_total]].append(data.set_index('Alternativa').drop([add_total]))
        data = data.reset_index()

    # Gerar o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(data))

    # Plotar as barras
    ax.bar(x_pos, data['Percentual'], color=colors[:len(data)])
    if add_total is not None:
        ax.patches[0].set_facecolor('#acacac')

    if text_fit:
        data['Alternativa'] = data['Alternativa'].apply(lambda x: _add_line_breaks(x, 10))

    # Remover os valores no eixo Y
    ax.set_yticks([])

    # Adicionar o nome de cada alternativa no eixo X
    ax.set_xticks(x_pos)
    ax.set_xticklabels(data['Alternativa'], fontsize=10, ha='center')

    # Titulo
    if var_type == 'nps':
        ax.set_title('Gráfico de Barras (NPS)')
        # Adicionar o valor da porcentagem acima de cada barra
        for i, v in enumerate(data['Percentual']):
            ax.text(i, v, f'{v:.{n_decimal_places}f}', color='black', ha='center', va='bottom', fontsize=18)
    elif var_type == 'favorability':
        ax.set_title('Gráfico de Barras (Favorabilidade)')
        # Adicionar o valor da porcentagem acima de cada barra
        for i, v in enumerate(data['Percentual']):
            ax.text(i, v, f'{v:.{n_decimal_places}f}%', color='black', ha='center', va='bottom', fontsize=18)
    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return plt


def generate_venn_chart(payload, intersection, adjust_circle=False):
    """
    Generates a Venn diagram based on the provided data.

    Parameters
    ----------
        payload (list): List containing the data of the sets to be represented in the diagram.
            Each item in the list should be a dictionary with the keys 'label', 'value', and 'enps'.
            'label' is the label of the set, 'value' is the percentage of the set, and 'enps' is the eNPS value.
        intersection (dict): Dictionary containing the data of the intersection between the sets.
            It should have the keys 'value' and 'enps' representing the percentage and eNPS value of the intersection.
        adjust_circle (bool, optional): Defines whether the Venn diagram circle should be adjusted for the provided values.
            Default is False.

    Returns
    -------
        matplotlib.pyplot: Object containing the generated Venn diagram.
    """
    # Obter as chaves e valores do dicionário
    labels = [x['label'] for x in payload]
    values = [x['value'] for x in payload]
    enpss = [x['enps'] for x in payload]

    # Converter os valores para inteiros
    values = [int(v) for v in values]

    # Criar o gráfico de Venn
    fig, ax = plt.subplots(figsize=(6, 6))
    if adjust_circle:
        venn = venn2(subsets=(values[0], values[1], intersection['value']), set_labels=(labels[0], labels[1]), ax=ax)

    else:
        venn = venn2(subsets=(10, 10, 5), set_labels=(labels[0], labels[1]), ax=ax)

    # Adicionar os valores dentro dos subconjuntos
    subset_labels = [f'{value}%\neNPS{enps}' for value, enps in zip(values, enpss)]
    subset_labels.append(f'{intersection["value"]}%\neNPS{intersection["enps"]}')
    for text in venn.subset_labels:
        text.set_fontsize(12)
    for text, label in zip(venn.subset_labels, subset_labels):
        text.set_text(label)
    return plt


def grafico_sentimentos(dataframe, n_decimal_places=0):

    """
    Generate a sentiment analysis chart using horizontal bars.

    Parameters
    ----------
        dataframe (pd.DataFrame): DataFrame containing sentiment data.
        n_decimal_places (int, optional): Number of decimal places to round the percentages (default: 0).

    Returns
    -------
        plt: Matplotlib plot object.

    """
    # Arredondar os valores percentuais
    dataframe = dataframe.round(n_decimal_places)

    # Ordenar o DataFrame pelo percentual positivo, seguido pelo percentual neutro
    dataframe = dataframe.sort_values(by=['Positivo', 'Neutro'], ascending=False)

    # Gerar as barras do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    y_pos = range(len(dataframe))

    # Barra Positivo (verde)
    ax.barh(y_pos, dataframe['Positivo'], color='#93c47d')

    # Barra Neutro (cinza)
    ax.barh(y_pos, dataframe['Neutro'], left=dataframe['Positivo'], color='#acacac')

    # Barra Negativo (preto)
    ax.barh(y_pos, 100 - dataframe['Positivo'] - dataframe['Neutro'], left=dataframe['Positivo'] + dataframe['Neutro'],
            color='#000000')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(dataframe.index, fontsize=18)
    ax.set_xticks([])  # Remover os valores no eixo X

    # Adicionar o valor da porcentagem em cada barra
    for i, (positivo, neutro, negativo) in enumerate(
            zip(dataframe['Positivo'], dataframe['Neutro'], 100 - dataframe['Positivo'] - dataframe['Neutro'])):
        ax.text(positivo / 2, i, f'{positivo:.{n_decimal_places}f}%', color='white', ha='center', va='center',
                fontsize=15)
        ax.text(positivo + neutro / 2, i, f'{neutro:.{n_decimal_places}f}%', color='black', ha='center', va='center',
                fontsize=15)
        ax.text(positivo + neutro + negativo / 2, i, f'{negativo:.{n_decimal_places}f}%', color='white', ha='center',
                va='center', fontsize=15)

    # Configurar os rótulos e o título
    ax.set_title('Análise de Sentimentos', fontsize=18)

    # Adicionar a legenda das alternativas
    pos_patch = mpatches.Patch(color='#93c47d', label='Positivo')
    neu_patch = mpatches.Patch(color='#acacac', label='Neutro')
    neg_patch = mpatches.Patch(color='#000000', label='Negativo')

    # ax.legend(handles=[pos_patch, neu_patch, neg_patch], loc='lower right')
    ax.legend(handles=[pos_patch, neu_patch, neg_patch], loc='upper center', bbox_to_anchor=(0.5, 0), ncol=3)

    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return plt


def _add_line_breaks(text, n):
    """
    Add line breaks to the input text at whitespace boundaries, ensuring each substring
    has a length as close to the specified number of characters (n) as possible.

    Parameters
    ----------
        text (str): The input text.
        n (int): The desired length of each substring.

    Returns
    -------
        str: The modified text with line breaks added.

    """
    words = text.split()  # Split the text into individual words
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) <= n:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return '\n'.join(lines)
