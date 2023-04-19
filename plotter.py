import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import numpy as np
import parameters as pmts

def plot(api_response, coin_name, trendlines, support_extrema, resistance_extrema,doubles,double_support,double_resistence):
    df = pd.DataFrame(api_response)
    df.columns = ['timestamp','Open', 'High', 'Low', 'Close']
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)



    points_for_doubles = []
    stylek = []
    for i, j, yi, yj in doubles:
        points_for_doubles.append([(df.index[i]), yi, (df.index[j]), yj])
        if j >= pmts.fraction_old_data * len(api_response):
            stylek.append("dot")
        else:
            stylek.append("solid")

    if len(double_support) == 0:
        double_support.append(0)
    points_for_double_support = [np.nan] * len(df)
    for i in double_support:
        points_for_double_support[i] = df.iloc[i]['Low']
    points_for_double_resistance= [np.nan] * len(df)
    for i in double_resistence:
        points_for_double_resistance[i] = df.iloc[i]['High']

    # Create a candlestick trace
    candlestick = go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing=dict(line=dict(color='green')),
        decreasing=dict(line=dict(color='red'))
    )


    double_traces = []
    for points, style in zip(points_for_doubles, stylek):
        x1, y1, x2, y2 = points
        double_traces.append(go.Scatter(x=[x1, x2], y=[y1, y2], mode='lines', line=dict(color='black')))

    # Combine all traces into a list
    data = [candlestick] + double_traces

    # Define layout for the figure
    layout = go.Layout(
        title=coin_name,
        xaxis=dict(
            showgrid=False,
            type='category',
            tickmode='array',
            tickvals=[df.index[0]]
        ),
        yaxis=dict(title='Price')
    )

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Set x-axis limits to the range of available data
    fig.update_xaxes(range=[df.index[0], df.index[-1]])

    # Save the figure to a file
    pio.write_html(fig, file="plots/" + coin_name + ".html", auto_open=True)
