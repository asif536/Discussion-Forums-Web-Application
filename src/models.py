import enum
from src import db
from datetime import datetime
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin

"""
    Blueprint of the database schema   

"""
def time_difference(time):
    difference= datetime.now()-time
    seconds_in_day = 24 * 60 * 60
    return divmod(difference.days * seconds_in_day + difference.seconds, 3600)[0]

class UserTypeEnum(enum.Enum):
    MODERATOR="moderator"
    CASUAL="casual"

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    picture=db.Column(db.Text,nullable=False)
    score=db.Column(db.Integer,default=0,nullable=False)
    post_count=db.Column(db.Integer,default=0,nullable=False)
    user_type=db.Column(db.Enum(UserTypeEnum),nullable=False)
    created_at=db.Column(db.DateTime(),nullable=False,default=datetime.now())
    modify_at=db.Column(db.DateTime(),nullable=False,default=datetime.now())
    deleted_at=db.Column(db.DateTime(),nullable=False,default=datetime.now())
    is_deleted=db.Column(db.Boolean,default=False)
    comment=db.relationship('Comment',backref='author',lazy=False)

    def __str__(self):
        return f"User('{self.name}')"
    
    def get_badge_level(self):
        if int(self.score)<10:
            return 0
        elif int(self.score)>=10 and int(self.score)<100:
            return 1
        elif int(self.score>=100) and int(self.score)<500:
            return 2
        elif int(self.score)>=500 and int(self.score)<1000:
            return 3
        else:
            return 4

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "badge":self.get_badge_level(),
            }
            

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

liked_by = db.Table('voted_by',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
                              nullable=False, primary_key=True),
                    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'),
                              nullable=False, primary_key=True),
                    )
                    
class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    content=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime(),nullable=False,default=datetime.now())
    modify_at=db.Column(db.DateTime(),nullable=False,default=datetime.now())
    deleted_at=db.Column(db.DateTime(),nullable=False,default=datetime.now())
    is_deleted=db.Column(db.Boolean,default=False)
    likes =db.Column(db.Integer,default=0)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment',
                              backref=db.backref('parent', remote_side=[id]),
                              lazy=False)
    liked_by = db.relationship('User', secondary=liked_by, lazy='subquery',
                               backref=db.backref('liked_on', lazy=True))

    def __repr__(self):
        return f"Message('{self.title}')"
    
    def get_json(self):
        return {
            "post_id": self.id,
            "author": self.author.get_json(),
            "title":self.title,
            "content": self.content,
            "time": time_difference(self.created_at),
            "upvotes": self.likes
        }

