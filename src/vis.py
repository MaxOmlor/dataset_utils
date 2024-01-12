def time_to_units(time_obj, time_unit):
    """ Konvertiert ein datetime.time-Objekt in die gewählte Zeiteinheit. """
    if time_unit == 'seconds':
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    elif time_unit == 'minutes':
        return time_obj.hour * 60 + time_obj.minute + time_obj.second / 60
    elif time_unit == 'hours':
        return time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
    elif time_unit == 'milliseconds':
        return (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1000 + time_obj.microsecond / 1000
    elif time_unit == 'microseconds':
        return (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1000000 + time_obj.microsecond

def determine_time_unit(column):
    """ Bestimmt die passende Zeiteinheit basierend auf dem Bereich der Werte in der Spalte. """
    total_seconds = column.apply(lambda t: t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6)
    max_time = total_seconds.max()
    min_time = total_seconds.min()

    if max_time - min_time < 60:  # Bereich ist weniger als 1 Minute
        if max_time - min_time < 1:  # Bereich ist weniger als 1 Sekunde
            return 'milliseconds' if max_time < 1 else 'seconds'
        return 'seconds'
    elif max_time - min_time < 3600:  # Bereich ist weniger als 1 Stunde
        return 'minutes'
    else:
        return 'hours'
    
import matplotlib.pyplot as plt
import numpy as np
import datetime

def scatterplot_matrix(dataframe, color_column=None, plot_size=2.5, subplot_spacing=0.05):
    n_vars = dataframe.shape[1]
    fig, axes = plt.subplots(n_vars, n_vars, figsize=(n_vars * plot_size, n_vars * plot_size))

    # Umwandeln von datetime.time Spalten in numerische Werte
    num_dataframe = dataframe.copy()
    for col in num_dataframe.columns.copy():
        if isinstance(num_dataframe[col].iloc[0], datetime.time):
            time_unit = determine_time_unit(num_dataframe[col])
            num_dataframe[col] = num_dataframe[col].apply(lambda t: time_to_units(t, time_unit))
            num_dataframe = num_dataframe.rename(columns={col: f'{col}_{time_unit}'})
            
    # Farbkodierung einrichten
    if color_column is not None and color_column in num_dataframe.columns:
        unique_values = num_dataframe[color_column].unique()
        colormap = plt.cm.get_cmap('viridis', len(unique_values))
        color_dict = {val: colormap(i) for i, val in enumerate(unique_values)}
        colors = num_dataframe[color_column].map(color_dict)
    else:
        colors = 'b'

    # Erstellen der Scatterplots
    for i in range(n_vars):
        for j in range(n_vars):
            ax = axes[i, j]
            if i == j:
                ax.text(0.5, 0.5, num_dataframe.columns[i], horizontalalignment='center', verticalalignment='center', fontsize=12)
                ax.set_xticks([])
                ax.set_yticks([])
            else:
                ax.scatter(num_dataframe.iloc[:, j], num_dataframe.iloc[:, i], c=colors)

            # Setzen der Ticklabels
            if i != n_vars - 1:
                ax.set_xticklabels([])
            if j != 0:
                ax.set_yticklabels([])

            # Setzen der Achsenbeschriftungen
            if j == 0:
                ax.set_ylabel(num_dataframe.columns[i])
            if i == n_vars - 1:
                ax.set_xlabel(num_dataframe.columns[j])

    # Anpassen der Abstände zwischen den Subplots
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=subplot_spacing, hspace=subplot_spacing)

    plt.show()

import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.ticker import MaxNLocator

def plot_distribution(dataframe, color_column=None, max_xticks=10, plot_width=10, subplot_hight=2, subplot_spacing=0.05):
    n_vars = dataframe.shape[1]
    
    if color_column is not None:
        unique_values = dataframe[color_column].unique()
        num_colors = len(unique_values)
    else:
        unique_values = [None]
        num_colors = 1
    colormap = plt.cm.get_cmap('viridis', len(unique_values))
    color_dict = {val: colormap(i) for i, val in enumerate(unique_values)}
    
    fig, axes = plt.subplots(n_vars, num_colors, figsize=(plot_width, subplot_hight * n_vars))
    
    # Kopieren des DataFrames zur Umwandlung von datetime.time in numerische Werte
    num_dataframe = dataframe.copy()
    for col in num_dataframe.columns.copy():
        if isinstance(num_dataframe[col].iloc[0], datetime.time):
            time_unit = determine_time_unit(num_dataframe[col])
            num_dataframe[col] = num_dataframe[col].apply(lambda t: time_to_units(t, time_unit))
            num_dataframe = num_dataframe.rename(columns={col: f'{col}_{time_unit}'})
    
    for i, unique_value in enumerate(unique_values):
        for j, column in enumerate(num_dataframe.columns):
            if len(unique_values) == 1:
                ax = axes[j]
            else:
                ax = axes[j, i]  # Vertauschte Indizes für das gewünschte Layout
            
            if color_column is not None:
                data = num_dataframe[num_dataframe[color_column] == unique_value][column]
                # ax.hist(data, bins=20, edgecolor='black', label=f'{color_column}: {unique_value}', color=color_dict[unique_value])  # Ändere die Farbe hier
                ax.hist(data, bins=20, edgecolor='black', color=color_dict[unique_value])  # Ändere die Farbe hier
                ax.set_xlabel(column)
                ax.xaxis.set_major_locator(MaxNLocator(max_xticks))
                if i == 0:  # Beschrifte nur die linken Achsen
                    ax.set_ylabel('Häufigkeit')
                else:
                    ax.set_yticklabels([])
                # ax.legend()
            else:
                ax.hist(num_dataframe[column], bins=20, edgecolor='black')
                ax.set_xlabel(column)
                ax.xaxis.set_major_locator(MaxNLocator(max_xticks))
                if i == 0:  # Beschrifte nur die linken Achsen
                    ax.set_ylabel('Häufigkeit')
                else:
                    ax.set_yticklabels([])
    
    for i, unique_value in enumerate(unique_values):
        if color_column is not None:
            axes[0, i].set_title(f'{color_column}: {unique_value}')
    
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=subplot_spacing, hspace=subplot_spacing)

    plt.tight_layout()
    plt.show()
