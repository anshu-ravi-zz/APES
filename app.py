from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

app = Flask(__name__)


@app.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)


def create_plot():
    df = pd.read_csv("CHAT.csv",
                     sep=":",
                     encoding='latin-1',
                     names=["Name", "Comment"],
                     skipinitialspace=True,
                     comment='"')
    df1 = df.groupby("Name").count()
    df1.sort_values("Comment", ascending=False, inplace=True)
    fig = go.Figure(
        data=[go.Bar(x=df1.Comment, y=df1.index, orientation="h")]
    )
    fig.update_xaxes(title_text='No of comments')
    fig.update_yaxes(title_text='Students')
    fig['layout']['yaxis']['autorange'] = "reversed"

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == '__main__':
    app.run()
