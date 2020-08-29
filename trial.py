import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go

df = pd.read_csv("CHAT.csv",
                 sep=":",
                 encoding='latin-1',
                 names=["Name", "Comment"],
                 skipinitialspace=True,
                 comment='"')
df1 = df.groupby("Name").count().reset_index()
print(df1.Comment)
# df1.sort_values("Comment", ascending=False, inplace=True)
# fig = go.Figure(
#     data=[go.Bar(x=df1.Comment, y=df1.index, orientation="h")],
# )
# fig.update_xaxes(title_text='No of comments')
# fig.update_yaxes(title_text='Students')
# fig['layout']['yaxis']['autorange'] = "reversed"
#
# fig.show()
