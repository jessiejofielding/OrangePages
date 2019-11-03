from orangepages.models.models import db, User, app

if app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite:////Users/jessie/OrangePages/test.sqlite':
    exit()

db.drop_all()
db.create_all()
db.session.commit()

sally = User('sstudent', 'Sally', 'Student', 'sstudent@princeton.edu')
john = User('jexample', 'John', 'Example', 'jexample@princeton.edu')
db.session.add(sally)
db.session.add(john)
db.session.commit()

users = User.query.all()
for user in users:
    print(user.firstname)
    print(user.lastname)
    print(user.uid)
