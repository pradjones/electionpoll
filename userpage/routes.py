''' Routes '''
from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from userpage import app
from userpage import db
from userpage.models import Topics, Options, Polls, Users

# flask-admin
from flask_admin import Admin
from admin import AdminView

admin = Admin(app, name='Dashboard', index_view=AdminView(
    Topics, db.session, url='/admin', endpoint='admin'))
admin.add_view(AdminView(Users, db.session))
admin.add_view(AdminView(Polls, db.session))
admin.add_view(AdminView(Options, db.session))


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/api/poll', methods=['GET', 'POST'])
def createpoll():
    if request.method == 'POST':
        i = 1
        poll = []
        while(('choiceTitle'+str(i)) in request.form):
            option = Options(name=request.form[('choiceTitle'+str(i))])
            newPoll = Polls(option=option)
            db.session.add(newPoll)
            poll.append(newPoll)
            i += 1
        newTopic = Topics(title=request.form['pollQuestion'], options=poll)
        db.session.add(newTopic)
        db.session.commit()
    return render_template('newPoll.html')


@app.route('/delete-poll', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        topic = Topics.query.filter(Topics.title == request.form['title']).first()
        options = topic.options.all()
        for option in options:
            poll = Polls.query.join(Options).filter(
                Options.name == str(option)).first()
            db.session.delete(poll)
        db.session.delete(topic)
        db.session.commit()
    all_topics = Topics.query.all()
    return render_template('delete.html', topics=all_topics)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        topics = Topics.query.join(Polls).all()
        return render_template('index.html', title='Polls OZ', topics=topics)
    else:
        optionName = request.form['Vote']
        print(optionName)
        Topic = Topics.query.join(Polls).join(Options).filter(
            Options.name.like(optionName)).first()
        option = Polls.query.join(Topics).join(Options).filter(Topics.title ==
            str(Topic)).filter(Options.name == optionName).first()
        print(option.vote_count)
        option.vote_count += 1
        db.session.commit()
        return render_template('results.html', title="Results")


@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html')


@app.route('/api/graphs')
def graphs():
    topic = [topic.to_json() for topic in Topics.query.all()]
    return render_template('graphs.html', data=topic)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        # get the user details from the form
        email = request.form['email']
        username = request.form['usr']
        password = request.form['pwd']
        # hash the password
        password = generate_password_hash(password)

        user = Users(email=email, username=username, password=password)

        db.session.add(user)
        db.session.commit()

        flash('Thanks for signing up please login')

        return redirect(url_for('login'))

    return render_template('signup.html')

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # search the database for the User
        user = Users.query.filter_by(username=username).first()
        print(user)
        if user:
            password_hash = user.password
            print(password_hash)
            if check_password_hash(password_hash, password):
                # The hash matches the password in the database log the user in
                session['user'] = username
                flash('Login was succesfull')
                print("success")
        else:
            # user wasn't found in the database
            flash('Username or password is incorrect please try again', 'error')
            print('fail')

    return render_template('login.html') or redirect(url_for('home'))


# logout
@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')

        flash('We hope to see you again!')

    return redirect(url_for('home'))
