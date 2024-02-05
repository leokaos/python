from flask import Flask, request, jsonify
from flask import request
from textblob import TextBlob
from flask_basicauth import BasicAuth
import pickle

model = pickle.load(open('modelo_casa.sav', 'rb'))
colunas = ['tamanho', 'ano', 'garagem']

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'leo'
app.config['BASIC_AUTH_PASSWORD'] = 'leo12345'

basic_auth = BasicAuth(app)


@app.route('/')
def home():
    return 'Minha primeira API'


@app.route('/sentimento')
@basic_auth.required
def sentimento():

    tb = TextBlob(request.args.get('frase'))
    tb_en = tb.translate(to='en', from_lang='pt')

    return str(tb_en.sentiment.polarity)


@app.route('/cotacao', methods=['POST'])
@basic_auth.required
def casas():

    payload = request.get_json()

    variaveis = [payload[col] for col in colunas]

    result = model.predict([variaveis])

    return jsonify(preco=result[0])


app.run(debug=True)
