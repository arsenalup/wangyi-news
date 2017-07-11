from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy

from forms import NewsForm

app = Flask(__name__)

db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(300), )
    author = db.Column(db.String(20), )
    view_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<News %r>' % (self.title)


@app.route('/')
def index():
    """首页"""
    news_list = News.query.filter_by(is_valid=True)
    return render_template('index.html', news_list=news_list)


@app.route('/cat/<name>/')
def cat(name):
    """类别"""
    news_list = News.query.filter(News.is_valid==True ).filter(News.type == name)
    return render_template('cat.html', name=name, news_list=news_list)


@app.route('/detail/<int:pk>/')
def detail(pk):
    """详情页"""
    new_obj = News.query.get(pk)
    return render_template('detail.html', new_obj=new_obj)


@app.route('/admin/')
@app.route('/admin/<int:page>/')
def admin(page=None):
    """新闻管理首页"""
    if page is None:
        page = 1
    page_data = News.query.filter_by().paginate(page=page, per_page=4)
    return render_template('admin/index.html', page_data=page_data)


@app.route('/admin/update/<int:pk>/', methods=('GET', 'POST'))
def update(pk):
    news_obj = News.query.get(pk)
    if not news_obj:
        return redirect(url_for('admin'))
    form = NewsForm(obj=news_obj)
    news_obj.title = form.title.data
    news_obj.content = form.content.data
    news_obj.type = form.type.data
    news_obj.author = form.author.data
    news_obj.is_valid = form.is_valid.data
    news_obj.image = form.image.data

    db.session.add(news_obj)
    db.session.commit()
    flash('修改成功')
    return render_template('/admin/update.html', pk=pk, form=form)


@app.route('/admin/delete/<int:pk>/', methods=('POST',))
def delete(pk):
    if request.method == 'POST':
        news_obj = News.query.get(pk)
        if news_obj is None:
            return 'no'
        news_obj.is_valid = False
        db.session.add(news_obj)
        db.session.commit()
        return 'yes'
    return 'no'


@app.route('/admin/add/', methods=('GET', 'POST'))
def add():
    form = NewsForm()
    if form.validate_on_submit():
        n1 = News(
            title = form.title.data,
            content = form.content.data,
            image = form.image.data,
            type = form.type.data,
            author = form.author.data,
            created_at=datetime.now(),
        )
        db.session.add(n1)
        db.session.commit()
        flash('新增成功')
        return redirect(url_for('admin'))
    return render_template('admin/add.html', form=form)


app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:cky1993717@localhost:3306/net_news?charset=utf8'
app.config['SECRET_KEY'] = 'a random string'
if __name__ == '__main__':
    app.run(debug=True)

