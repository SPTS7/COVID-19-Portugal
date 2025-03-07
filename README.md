## Disclaimer

All of this information does not have any kind of scientific validity whatsoever.

# COVID-19 Data Analysis and Predictions

This Python project performs COVID-19 data analysis and generates predictions using logistic and Gompertz models. It fits these models to the COVID-19 data and produces various visualizations and forecasts. The project also exports the results to a CSV file.

![Prediction](prediction.png)

## Prerequisites

Before running the project, ensure you have the following Python libraries installed:

- `numpy`
- `pandas`
- `matplotlib`
- `scipy`
- `lmfit`
- `mpld3`
- `tqdm`

You can install these dependencies using `pip`:

```bash
pip install numpy pandas matplotlib scipy lmfit mpld3 tqdm
```

## File Structure

- `coronadata.xlsx`: Input file containing COVID-19 data.
- `prediction.pdf`: Output PDF containing the prediction visualizations.
- `prediction.png`: Output PNG image containing the prediction visualizations.
- `Previsoes.csv`: CSV file containing the predictions and analysis results.

## Functions

### 1. `generate_data(df)`

Generates data from the provided DataFrame containing COVID-19 data.

**Arguments:**

- `df`: The DataFrame containing the data, with columns "Dia Ano," "Suspeitos," and "Confirmados."

**Returns:**

- `x`: The day of the year.
- `ysuspeitos`: Suspected cases.
- `yconfirmados`: Confirmed cases.
- `dias`: Length of the data.

### 2. `fitlogistic(x, y, dias)`

Fits a logistic model to the data and returns the fit parameters and values.

**Arguments:**

- `x`: Day of the year.
- `y`: Confirmed cases.
- `dias`: Total number of days to predict.

**Returns:**

- Fit parameters (amplitude, center, sigma), fitted values, cumulative values, and the fit report.

### 3. `fitGompertz(x, y, dias)`

Fits a Gompertz model to the data and returns the fit parameters and values.

**Arguments:**

- `x`: Day of the year.
- `y`: Confirmed cases.
- `dias`: Total number of days to predict.

**Returns:**

- Fit parameters (amplitude, center, sigma), fitted values, cumulative values, and the fit report.

### 4. `convertdateconf(centerc)`

Converts the center of the logistic fit to a date for confirmed cases.

**Arguments:**

- `centerc`: The center of the logistic curve.

**Returns:**

- `diac`: Converted day of the year.
- `diamaxc`: Corresponding date.

### 5. `convertdatesusp(centers)`

Converts the center of the logistic fit to a date for suspected cases.

**Arguments:**

- `centers`: The center of the logistic curve for suspected cases.

**Returns:**

- `dias`: Converted day of the year.
- `diamaxs`: Corresponding date.

### 6. `datas(x)`

Converts the day of the year to actual date format.

**Arguments:**

- `x`: List of days of the year.

**Returns:**

- `date`: List of datetime objects.
- `data`: List of formatted date strings.

### 7. `plot(...)`

Plots the confirmed and suspected cases along with the fitted logistic and Gompertz models.

**Arguments:**

- `x`, `xconf`, `date`, `yconfirmados`, `outputconf`, `erfoutputconf`, `cumconf`, `erfcumconf`, `ysuspeitos`, `Diamaxconf`, `amplitudeconf`: Various data and fit results to visualize the analysis.

### 8. `export(...)`

Exports the predictions and analysis results to a CSV file.

**Arguments:**

- `x`, `out`, `erfout`, `cumu`, `erfcumu`, `dias`, `data`, `diaspassados`, `yconfirmados`: Data and analysis results to export.

### 9. `predictions(df, dias)`

Generates the predictions and visualizations.

**Arguments:**

- `df`: The DataFrame containing COVID-19 data.
- `dias`: Total number of days to predict.

## Running the Code

To run the code, simply execute the script. Ensure that the input data is available in an Excel file (`coronadata.xlsx`) in the same directory.

```bash
python your_script_name.py
```

The program will:

1. Load the data from the Excel file.
2. Fit both logistic and Gompertz models to the confirmed cases.
3. Generate predictions for the specified number of days.
4. Plot the data and fits.
5. Export the results to a CSV file (`Previsoes.csv`).
6. Save visualizations as PNG and PDF files (`prediction.png` and `prediction.pdf`).

## Results

The following files will be generated:

- `prediction.png`: A PNG image of the predictions and analysis.
- `prediction.pdf`: A PDF version of the same visualizations.
- `Previsoes.csv`: A CSV file with the predictions and analysis data.

## License

This project is licensed under the MIT License.
