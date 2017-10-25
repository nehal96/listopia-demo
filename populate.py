# -*- coding: utf-8 -*-

from helper import getBookInfo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Book, User

from helper import getGenreList
from flask import Flask, jsonify
from flask import session as login_session
import json

engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)



steve_jobs_info = getBookInfo('steve jobs')
Steve_Jobs = Book(googleID=steve_jobs_info['id'],
                  title=steve_jobs_info['title'],
                  subtitle=steve_jobs_info['subtitle'],
                  author=steve_jobs_info['authors'][0],
                  publisher=steve_jobs_info['publisher'],
                  publishDate=steve_jobs_info['publishDate'],
                  description=steve_jobs_info['description'],
                  ISBN_10=steve_jobs_info['ISBN_10'],
                  ISBN_13=steve_jobs_info['ISBN_13'],
                  pageCount=steve_jobs_info['pageCount'],
                  category=steve_jobs_info['categories'][0],
                  buyLinkGoogle=steve_jobs_info['buyLinkGoogle'],
                  imageLink=steve_jobs_info['imageLink'])


the_gene_info = getBookInfo('the gene')
american_kingpin_info = getBookInfo('american kingpin')

TheGene = Book(googleID=the_gene_info['id'],
               title=the_gene_info['title'],
               subtitle=the_gene_info['subtitle'],
               author=the_gene_info['authors'][0],
               publisher=the_gene_info['publisher'],
               publishDate=the_gene_info['publishDate'],
               description=the_gene_info['description'],
               ISBN_10=the_gene_info['ISBN_10'],
               ISBN_13=the_gene_info['ISBN_13'],
               pageCount=the_gene_info['pageCount'],
               category=the_gene_info['categories'][0],
               buyLinkGoogle=the_gene_info['buyLinkGoogle'],
               imageLink=the_gene_info['imageLink'])
session.add(TheGene)
session.commit()

AmericanKingpin = Book(googleID=american_kingpin_info['id'],
                       title=american_kingpin_info['title'],
                       subtitle=american_kingpin_info['subtitle'],
                       author=american_kingpin_info['authors'][0],
                       publisher=american_kingpin_info['publisher'],
                       publishDate=american_kingpin_info['publishDate'],
                       description=american_kingpin_info['description'],
                       ISBN_10=american_kingpin_info['ISBN_10'],
                       ISBN_13=american_kingpin_info['ISBN_13'],
                       pageCount=american_kingpin_info['pageCount'],
                       category=american_kingpin_info['categories'][0],
                       buyLinkGoogle=american_kingpin_info['buyLinkGoogle'],
                       imageLink=american_kingpin_info['imageLink'])
session.add(AmericanKingpin)
session.commit()

all_the_light_info = getBookInfo('all the light we cannot see')

AllTheLight = Book(googleID=all_the_light_info['id'],
                   title=all_the_light_info['title'],
                   subtitle=all_the_light_info['subtitle'],
                   author=all_the_light_info['authors'][0],
                   publisher=all_the_light_info['publisher'],
                   publishDate=all_the_light_info['publishDate'],
                   description=all_the_light_info['description'],
                   ISBN_10=all_the_light_info['ISBN_10'],
                   ISBN_13=all_the_light_info['ISBN_13'],
                   pageCount=all_the_light_info['pageCount'],
                   category=all_the_light_info['categories'][0],
                   buyLinkGoogle=all_the_light_info['buyLinkGoogle'],
                   imageLink=all_the_light_info['imageLink'])
session.add(AllTheLight)
session.commit()


shoe_dog_info = getBookInfo('shoe dog')
ShoeDog = Book(googleID=shoe_dog_info['id'],
               title=shoe_dog_info['title'],
               subtitle=shoe_dog_info['subtitle'],
               author=shoe_dog_info['authors'][0],
               publisher=shoe_dog_info['publisher'],
               publishDate=shoe_dog_info['publishDate'],
               description=shoe_dog_info['description'],
               ISBN_10=shoe_dog_info['ISBN_10'],
               ISBN_13=shoe_dog_info['ISBN_13'],
               pageCount=shoe_dog_info['pageCount'],
               category=shoe_dog_info['categories'][0],
               buyLinkGoogle=shoe_dog_info['buyLinkGoogle'],
               imageLink=shoe_dog_info['imageLink'])
session.add(ShoeDog)
session.commit()
