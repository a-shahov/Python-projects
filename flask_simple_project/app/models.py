from datetime import datetime
from sqlalchemy.orm import RelationshipProperty
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from hashlib import md5

# This is a direct translation of the association table from my diagram above. Note that I am not declaring this
# table as a model, like I did for the users and posts tables. Since this is an auxiliary table that has no data
# other than the foreign keys, I created it without an associated model class.
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    id: object = db.Column(db.Integer, primary_key=True)
    username: object = db.Column(db.String(64), index=True, unique=True)
    email: object = db.Column(db.String(128), index=True, unique=True)
    password_hash: object = db.Column(db.String(128))
    # the User class has a new posts field, that is initialized with db.relationship.This is not an actual database
    # field, but a high-level view of the relationship between users and posts, and for that reason it isn't in the
    # database diagram
    #
    # What does db.relationship() do? That function returns a new property that can do multiple
    # things. In this case we told it to point to the Post class and load multiple of those. How does it know that
    # this will return more than one post? Because SQLAlchemy guesses a useful default from your declaration. If
    # you would want to have a one-to-one relationship you can pass uselist=False to relationship().
    #
    # Since a user with no name or an email address with no post associated makes no sense, nullable=False tells
    # SQLAlchemy to create the column as NOT NULL. This is implied for primary key columns, but it’s a good idea to
    # specify it for all other columns to make it clear to other people working on your code that you did actually
    # want a nullable column and did not just forget to add it.
    #
    # So what do backref and lazy mean? backref is a simple way to also declare a new property on the Post class.
    # You can then also use my_post.author to get to the author at that post. lazy defines when SQLAlchemy will
    # load the data from the database:
    #
    # 'select' / True (which is the default, but explicit is better than implicit) means that SQLAlchemy will load
    # the data as necessary in one go using a standard select statement.
    #
    # 'joined' / False tells SQLAlchemy to load the relationship in the same query as the parent using a JOIN statement.
    #
    # 'subquery' works like 'joined' but instead SQLAlchemy will use a subquery.
    #
    # 'dynamic' is special and can be useful if you have many items and always want to apply additional SQL filters
    # to them. Instead of loading the items SQLAlchemy will return another query object which you can further refine
    # before loading the items. Note that this cannot be turned into a different loading strategy when querying so
    # it’s often a good idea to avoid using this in favor of lazy=True. A query object equivalent to a dynamic
    # user.posts relationship can be created using Post.query.with_parent(user) while still being able to use
    # lazy or eager loading on the relationship itself as necessary.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Let's examine all the arguments to the db.relationship() call one by one:
    #
    # 'User' is the right side entity of the relationship (the left side entity is the parent class). Since this is a
    # self-referential relationship, I have to use the same class on both sides.
    #
    # secondary configures the association table that is used for this relationship, which I defined right above this
    # class.
    #
    # primaryjoin indicates the condition that links the left side entity (the follower user) with the association
    # table. The join condition for the left side of the relationship is the user ID matching the follower_id field
    # of the association table. The value of this argument is followers.c.follower_id, which qreferences the
    # follower_id column of the association table.
    #
    # secondaryjoin indicates the condition that links the right side entity (the followed user)
    # with the association table. This condition is similar to the one for primaryjoin, with the only difference that
    # now I'm using followed_id, which is the other foreign key in the association table.
    #
    # backref defines how this relationship will be accessed from the right side entity. From the left side,
    # the relationship is named followed, so from the right side I am going to use the name followers to represent
    # all the left side users that are linked to the target user in the right side.
    #
    # The additional lazy argument indicates the execution mode for
    # this query. A mode of dynamic sets up the query to not run until specifically requested, which is also how I
    # set up the posts one-to-many relationship. lazy is similar to the parameter of the same name in the backref,
    # but this one applies to the left side query instead of the right side.
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),  # for parent
                               secondaryjoin=(followers.c.followed_id == id),  # for child
                               backref=db.backref('followers', lazy='dynamic'),  # for parent
                               lazy='dynamic'  # for child
                               )
    about_me: object = db.Column(db.String(140))
    last_seen: object = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


# Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that
# reason, the extension expects that the application will configure a user loader function, that can be called to
# load a user given the ID
@login.user_loader
def load_user(identifier):
    return User.query.get(int(identifier))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
