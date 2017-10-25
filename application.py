# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, url_for, request, redirect, jsonify
from flask import make_response, flash
from flask import session as login_session

from datetime import datetime
import os
import http.server
import httplib2
import json
import ast
import requests
import threading
from socketserver import ThreadingMixIn
import random, string

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from models import Base, Book, User
from helper import getBookInfo, chunkify, getGenreList


engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/landingpage')
def showLandingPage():
    return render_template('landingpage.html')


@app.route('/books')
def showBookshelf():
    books = session.query(Book).all()
    book_chunks = chunkify(books, 4)
    genres = getGenreList(books)
    return render_template('bookshelf.html', book_chunks=book_chunks,
                                genres=genres)


@app.route('/book/<title>/<int:id>/')
def showBook(title, id):
    book = session.query(Book).filter_by(id=id).one()
    publish_date = book.publishDate
    try:
        publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
        publish_date = publish_date.strftime("%d %b %Y")
    except (ValueError, TypeError):
        publish_date = book.publishDate

    return render_template('showBook.html', book=book, publishDate=publish_date)


@app.route('/books/<genre>/')
def showGenre(genre):
    genre_format = genre.replace('+', ' ').title()
    books_by_genre = session.query(Book).filter_by(category=genre_format).all()
    book_chunks = chunkify(books_by_genre, 4)

    return render_template('showGenre.html', genre=genre_format,
                    book_chunks=book_chunks)


@app.route('/book/add/', methods=['GET', 'POST'])
def addBook():
    if request.method == 'POST':
        if request.form['search']:
            search_query = request.form['search']
            book_info = getBookInfo(search_query)
            if book_info is not None:
                return redirect(url_for('showSearchedBook', book_info=book_info))
            else:
                return render_template('nomatches.html',
                            search_query=search_query)
        else:
            return render_template('addBook.html')
    else:
        return render_template('addBook.html')


@app.route('/book/add/show')
def showSearchedBook():
    book_info = request.args.get('book_info')
    book_info = ast.literal_eval(book_info)
    response = make_response(render_template('showSearchedBook.html',
                    book_info=book_info))

    return response


@app.route('/book/add/confirm/', methods=['POST'])
def confirmBook():
    if request.method == 'POST':
        if request.form['confirmation']:
            book_info = request.args.get('book_info')
            book_info = ast.literal_eval(book_info)
            newBook = Book(googleID=book_info['id'],
                           title=book_info['title'],
                           subtitle=book_info['subtitle'],
                           author=book_info['authors'][0],
                           publisher=book_info['publisher'],
                           publishDate=book_info['publishDate'],
                           description=book_info['description'],
                           ISBN_10=book_info['ISBN_10'],
                           ISBN_13=book_info['ISBN_13'],
                           pageCount=book_info['pageCount'],
                           category=book_info['categories'][0],
                           buyLinkGoogle=book_info['buyLinkGoogle'],
                           imageLink=book_info['imageLink'])
            session.add(newBook)
            session.commit()
            return redirect(url_for('showBookshelf'))

@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
def editBook(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    publish_date = book.publishDate
    try:
        publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
        publish_date = publish_date.strftime("%d %b %Y")
    except (ValueError, TypeError):
        publish_date = book.publishDate
    if request.method == 'POST':
        if request.form['description']:
            book.description = request.form['description']
        if request.form['imageurl']:
            book.imageLink = request.form['imageurl']
        session.add(book)
        session.commit()
        return render_template('showBook.html', book=book,
                        publishDate=publish_date)
    else:
        return render_template('editBook.html', book=book)


@app.route('/book/delete/<int:book_id>', methods=['POST'])
def deleteBook(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        return redirect(url_for('showBookshelf'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000)) # Use PORT if it's there
    server_address = ('', port)
    httpd = ThreadHTTPServer(server_address, Shortener)
    httpd.serve_forever()
