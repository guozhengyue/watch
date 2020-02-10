from flask import Flask,render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request,redirect,flash
import click
import os
# import sys

app = Flask(__name__)

app.config['SECRET_KEY']='dev'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(app.root_path,'data.db')

db=SQLAlchemy(app)



class User(db.Model):	#	表名将会是	user（自动生成，小写处理)
        id=db.Column(db.Integer,primary_key=True) #	主键
        name    =   db.Column(db.String(20))    #	名字



class Movie(db.Model):		#	表名将会是	movie
        id	=	db.Column(db.Integer,primary_key=True)      #	主键
        title   =   db.Column(db.String(60))    #	电影标题
        year    =   db.Column(db.String(4))     #	电影年份

@app.cli.command()
def forge():
    # db.drop_all()   
    db.create_all()

    name	=	'Grey	Li'
    movies	=[{'title':	'My	Neighbor	Totoro',	'year':	'1988'},				
    {'title':	'Dead	Poets	Society',	'year':	'1989'},				
    {'title':	'A	Perfect	World',	'year':	'1993'},				
    {'title':	'Leon',	'year':	'1994'},				
    {'title':	'Mahjong',	'year':	'1996'},				
    {'title':	'Swallowtail	Butterfly',	'year':	'1996'},				
    {'title':	'King	of	Comedy',	'year':	'1999'},				
    {'title':	'Devils	on	the	Doorstep',	'year':	'1999'},				
    {'title':	'WALL-E',	'year':	'2008'},				
    {'title':	'The	Pork	of	Music',	'year':	'2012'},]
    user=User(name=name)
    db.session.add(user)
    for m in movies:
        movie=Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done')
# @app.route('/')
# def	  hello():				
#     return	u'欢迎来到我的	Watchlist！'
@app.context_processor
def     inject_user():
        user=User.query.first()
        return dict(user=user)


@app.route('/',methods=['GET','POST'])
def	   index():
        if request.method=='POST':
            title=request.form.get('title')
            year=request.form.get('year')
            if not title or not year or len(year)>4 or len(title)>60:
                flash('Invalid input')
                return redirect(url_for('index'))
            movie=Movie(title=title,year=year)
            db.session.add(movie)
            db.session.commit()
            flash('Item created.')
            return redirect(url_for('index'))

        # user=User.query.first()
        movies=Movie.query.all()
        return	render_template('index.html',movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@app.errorhandler(404)
def     page_not_found(e):
        user    =	User.query.first()
        return	render_template('404.html'),404		#	返回模 板和状态码

# @app.route('/user/<name>') 
# def	  user_page(name):				
#     return	'User:	%s'	%name

# @app.route('/test') 
# def	  test_url_for():				#	下面是一些调用示例（请在命令行窗口查看输出的	URL）：				
#         print(url_for('hello'))		#	输出：/				
#         #	注意下面两个调用是如何生成包含	URL	变量的	URL	的				
#         print(url_for('user_page',	name='greyli'))		#	输出：/user/gre yli				
#         print(url_for('user_page',	name='peter'))		#	输出：/user/peter
#         print(url_for('test_url_for'))		#	输出：/test				
#         #	下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到	URL	后面。				
#         print(url_for('test_url_for',num=2))		#	输出：/test?num=2				
#         return	'Test	page'

if __name__ == '__main__':
    app.run()