from flask import Flask, jsonify, request
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/add', methods=['GET'])
def add_database():
    db.create_all()
    return jsonify({"Hello": "World"})


@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(reversed(all_articles))
    return jsonify(results)


@app.route('/add', methods=['POST'])
def add_articles():
    title = request.json['title']
    # loadings = request.json['loadings']
    # tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    # model = TFGPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)
    #
    # input_id = tokenizer.encode(title, return_tensors='tf')
    #
    # output = model.generate(input_id, max_length=100,
    #                         num_beams=5, no_repeat_ngram_size=2,
    #                         early_stopping=True)
    #
    # body = tokenizer.decode(output[0], skip_special_tokens=True,
    #                         clean_up_tokenization_spaces=True)
    # body = request.json['body']
    body = 'Hello test'

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


@app.route('/update/<id>', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/delete/<id>', methods=['DELETE'])
def article_delete(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=False)
