from userpage import db
# Base model that for other models to inherit from


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

# Model for poll topics


class Topics(Base):

    title = db.Column(db.String(500))

    def to_json(self):
        return {
            'title': self.title,
            'options':
                [{'name': option.option.name, 'vote_count': option.vote_count}
                    for option in self.options.all()]
        }
    # user friendly way to display the object

    def __repr__(self):
        return self.title

# Model for poll choices


class Options(Base):
    name = db.Column(db.String(200), unique=True)

# Polls model to connect topics and options together


class Polls(Base):

    # Columns declaration
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    vote_count = db.Column(db.Integer, default=0)

    # Relationship declaration (makes it easier for us to access the polls
    # model from the other models it's related to)
    topic = db.relationship('Topics', foreign_keys=[topic_id],
                            backref=db.backref('options', lazy='dynamic'))
    option = db.relationship('Options', foreign_keys=[option_id])

    def __repr__(self):
        # a user friendly way to view our objects in the terminal
        return self.option.name

# create the user model


class Users(Base):
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        # a user friendly way to view our objects in the terminal
        return self.username


db.create_all()
db.session.commit()
