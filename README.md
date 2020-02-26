# What happened after the All-Star break?

This repo contains all the necessary files for maintaining [this dashboard](https://all-star-break-dash.herokuapp.com/) which looks at the performance of 3 different MLB pitchers before and after the All-Star break. The dashboard is built using Python-based [Dash](https://plot.ly/dash/) by Plotly.

## Installation

The dashboard is deployed using [Heroku](https://dashboard.heroku.com/apps), so installation is not necessary. Simply use [this link](https://all-star-break-dash.herokuapp.com/) to access the dashboard.

If the dashboard is offline for any reason, you can run the dashboard locally by:

1. Clone this repo locally
2. Create a virtual env for this project using your preferred method
2. Using Terminal, navigate to the directory that contains the repo and run the following:
```bash
$ pip install -r requirements.txt
$ python app.py
```
3. Navigate to ```localhost:8050``` on your preferred browser to access the dashboard

Note: Having Python installed is a requirement for this option.

## Usage

Use [this link](https://all-star-break-dash.herokuapp.com/) to access the dashboard. You can use the dropdowns to explore the data for each pitcher.

## Support & Contributing
For help or if you want to build additional Dash components, please open an issue first to discuss what you would like to change.

Pull requests are welcome. Please make sure to include tests as appropriate.
