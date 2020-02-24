from datetime import datetime
import json
from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine

from forms import ContatoForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    from models import Post

    posts = Post.objects
    if request.method == 'POST':
        # Adicionei na lista de posts
        hoje = datetime.now()
        p = Post(
           content=request.values['content'],
           date=hoje.strftime("%d/%m/%Y %H:%M")
       )
        p.save()
    posts = Post.objects.all()
    return render_template('index.html', titulo="Microblog de PWEB1", posts=posts)


@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    form = ContatoForm(csrf_enabled=False)
    if form.validate_on_submit():
        return 'Formulário enviado com sucesso, por %s/%s' % (form.data['nome'], form.data['email'])
    return render_template('contato.html', titulo="Contato", form=form)


@app.route('/sobre/')
def sobre():
    return 'Este é o nosso primeiro projeto Flask!!!'


if __name__ == '__main__':
    app.run()
