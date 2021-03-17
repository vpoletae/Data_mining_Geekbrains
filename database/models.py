from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, \
                        ForeignKey, Table

Base = declarative_base()

class IdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)

class NameMixin:
    name = Column(String, nullable=False)

class UrlMixin:
    url = Column(String, nullable=False, unique=True)

tag_post = Table("tag_post",
                 Base.metadata,
                 Column('post_id', Integer, ForeignKey("post.id")),
                 Column('tag_id', Integer, ForeignKey("tag.id")),
                 )

comment_post = Table("comment_post",
                 Base.metadata,
                 Column('post_id', Integer, ForeignKey("post.id")),
                 Column('comment_id', Integer, ForeignKey("comment.id")),
                 )

class Post(Base, UrlMixin):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("writer.id"))
    img = Column(String, nullable=False, unique=True)
    pub_date = Column(DateTime, nullable=False)
    author = relationship("Writer")
    tags = relationship("Tag", secondary=tag_post)
    comments = relationship("Comment", secondary=comment_post)


class Writer(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__ = 'writer'
    posts = relationship("Post")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_author = Column(String, nullable=False)
    comment_text = Column(String, nullable=False)
    posts = relationship("Post", secondary=comment_post)

class Tag(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__ = 'tag'
    posts = relationship("Post", secondary=tag_post)
