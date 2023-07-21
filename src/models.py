import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum 
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er


Base = declarative_base()



class MediaType(enum.Enum):
    IMAGE = 'image'
    VIDEO = 'video'


# Tabla y Tabla intermedia para relacionar muchos a muchos

followers = Table('followers',
    Base.metadata,         
    Column('user_from_id', Integer, ForeignKey('user.userID'), primary_key=True),
    Column('user_ID', Integer, ForeignKey('user.userID'), primary_key=True)
)


class User(Base):
    __tablename__= 'user'
    userID = Column (Integer, primary_key = True)
    username = Column (String(50), nullable = False)
    firstname = Column (String(50), nullable = False)
    lastname = Column (String(50), nullable = False)
    email = Column (String(50), nullable = False, unique = True)
    followers = relationship ("Follower", secondary=followers, lazy="subquery", backref=backref("user", lazy=True))

class Follower(Base):
    __tablename__= 'follower'
    id = Column(Integer, primary_key = True )

# -----------------------------------------------


class Post(Base):
    __tablename__= 'post'
    postID = Column (Integer, primary_key = True, nullable=False)
    user_ID = Column (Integer, ForeignKey('user.userID'), nullable=False)


class Media(Base):
    __tablename__= 'media'
    mediaID = Column (Integer, primary_key = True)
    type = Column(Enum(MediaType), nullable=False)  
    url = Column (String(250), nullable=False)
    post_ID = Column (Integer, ForeignKey('post.postID'), nullable=False)   


class comments(Base):
    __tablename__= 'comments'
    commentID = Column (Integer, primary_key = True)
    author_ID = Column (Integer, ForeignKey('user.userID'))
    post_ID = Column (Integer, ForeignKey('post.postID'))

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e