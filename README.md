# dataset_utils

This repository contains a set of Python functions designed for the conversion of `datetime.time` objects into various time units, and for visualizing and analyzing time-based data within pandas DataFrames. It includes utilities for determining the most appropriate time unit for a given set of time data, and for generating scatterplot matrices and distribution plots with options for color coding based on categorical data.

## Features

1. **Time Conversion (`time_to_units`)**: Converts `datetime.time` objects into a specified time unit (seconds, minutes, hours, milliseconds, or microseconds).

2. **Determine Time Unit (`determine_time_unit`)**: Automatically determines the most appropriate time unit (seconds, minutes, hours, milliseconds, or microseconds) to represent a range of time values based on their variance.

3. **Scatterplot Matrix (`scatterplot_matrix`)**: Generates a matrix of scatter plots for each pair of numerical variables in a DataFrame. If a DataFrame column contains `datetime.time` objects, they are automatically converted into a numerical representation before plotting. This function supports color coding based on a categorical column.

4. **Distribution Plot (`plot_distribution`)**: Generates distribution plots (histograms) for each numerical variable in a DataFrame, with optional color coding based on a categorical column. Like the scatterplot matrix, `datetime.time` objects are automatically converted to numerical values based on the most suitable time unit.

## Usage

### Time Conversion

```python
import datetime
time_obj = datetime.time(12, 34, 56)
converted_time = time_to_units(time_obj, 'minutes')
print(converted_time)
```

### Determine Time Unit

```python
import pandas as pd
time_data = pd.Series([datetime.time(1, 0), datetime.time(2, 0)])
best_unit = determine_time_unit(time_data)
print(best_unit)
```

### Scatterplot Matrix

```python
import pandas as pd
dataframe = pd.DataFrame({
    'Time': [datetime.time(12, 34, 56), datetime.time(13, 14, 15)],
    'Value': [1, 2]
})
scatterplot_matrix(dataframe, color_column='Value')
```

### Distribution Plot

```python
plot_distribution(dataframe, color_column='Value')
```

## Installation

No specific installation steps are required apart from having Python and the necessary libraries (`pandas`, `matplotlib`, `numpy`) installed. Simply clone this module into your Python project and ensure the required libraries are installed.
