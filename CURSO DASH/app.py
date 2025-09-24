from ucimlrepo import fetch_ucirepo
import plotly.express as px
from dash import Dash, dcc, html

heart_disease = fetch_ucirepo(id=45)
dados = heart_disease.data.features

figura_histograma = px.histogram(dados, x='age', title='Histograma de idades')

dados["doenca"] = (heart_disease.data.targets > 0) * 1
figura_boxplot = px.box(dados, x='doenca', y='age', title='Boxplot de idades', color='doenca')

figura_boxplot_chol = px.box(dados, x='doenca', y='chol', color='doenca', title='Boxplot de Colesterol Sérico')

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Análise de dados do UCI Repository Heart Disease'),
    html.Div([
        html.H2('Histograma de idades'),
        dcc.Graph(figure=figura_histograma)
    ]),
    html.Div([
        html.H2('Boxplot de idades'),
        dcc.Graph(figure=figura_boxplot)
    ]),
    html.Div([
        html.H2('Boxplot de Colesterol Sérico'),
        dcc.Graph(figure=figura_boxplot_chol)
    ])
])

app.run_server(debug=True)
