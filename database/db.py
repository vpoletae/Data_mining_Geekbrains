from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


class Database:

    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def _get_or_create(self, session, model, **data):
        db_data = session.query(model).filter(model.url == data["url"]).first()
        if not db_data:
            db_data = model(**data)
        return db_data

    def _get_or_create_comments(self, session, data: list) -> list:
        result = []
        if data:
            for comment in data:
                comment_author = self._get_or_create(
                    session,
                    models.Writer,
                    models.Writer.url,
                    comment["comment"]["user"]["url"],
                    name=comment["comment"]["user"]["full_name"],
                    url=comment["comment"]["user"]["url"],
                )
                db_comment = self.get_or_create(
                    session,
                    models.Comment,
                    models.Commet.id,
                    comment["comment"]["id"],
                    **comment["comment"],
                    author=comment_author,
                )

                result.append(db_comment)
                result.extend(
                    self._get_or_create_comments(session, comment["comment"]["children"])
                )
                
    def create_post(self, data):
        session = self.maker()
        writer = self._get_or_create(session, models.Writer, **data['writer_data'])
        tags = map(lambda tag_data: self._get_or_create(session, models.Tag, **tag_data),
                    data["tags_data"])
        comments = map(lambda comment_data: self._get_or_create(session, models.Comment, **comment_data),
                    data["comments_data"])          
        post = self._get_or_create(session, models.Post, **data["post_data"], writer=writer)
        post.tags.extend(tags)
        post.comments.extend(comments)

        session.add(post)

        try:
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
