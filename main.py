from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Teacher.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subj = db.Column(db.String(150), nullable=True)
    day = db.Column(db.String(150), nullable=True)
    time = db.Column(db.String(150), nullable=True)
    weektype = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Article %r>" % self.id


class Subj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Subj %r>" % self.id


class TeachName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Teacher %r>" % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-teacher', methods=['POST', 'GET'])
def create_teacher():
    if request.method == "POST":
        name = request.form['name']
        subj = request.form['subj']
        day = request.form['day']
        time = request.form['time']
        weektype = request.form['subjType']

        teacher = Teacher(name=name, subj=subj, day=day, time=time, weektype=weektype)
        try:
            db.session.add(teacher)
            db.session.commit()
            return redirect('/create-teacher')
        except:
            return "Произошла ошибка"
    else:
        subjects = Subj.query.order_by(Subj.s_name).all()
        teachers = TeachName.query.order_by(TeachName.t_name).all()
        return render_template("create-teacher.html", subjects=subjects, teachers=teachers)

@app.route('/teacher')
def teachers():
    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template("teacher.html", teachers=teachers)


@app.route('/teacher/<int:id>')
def teacher_detail(id):
    teacher = Teacher.query.get(id)
    return render_template("teacher_detail.html", teacher=teacher)


@app.route('/teacher/<int:id>/del')
def teacher_delete(id):
    teacher = Teacher.query.get_or_404(id)

    try:
        db.session.delete(teacher)
        db.session.commit()
        return redirect('/teacher')
    except:
        return "Произошла ошибка"


@app.route('/teacher/<int:id>/up', methods=['POST', 'GET'])
def teacher_update(id):
    teacher = Teacher.query.get(id)
    if request.method == "POST":
        teacher.name = request.form['name']
        teacher.subj = request.form['subj']
        teacher.day = request.form['day']
        teacher.time = request.form['time']
        teacher.weektype = request.form['subjType']


        try:
            db.session.commit()
            return redirect('/teacher')
        except:
            return "Произошла ошибка"
    else:

       subjects = Subj.query.order_by(Subj.s_name).all()
       teachers = TeachName.query.order_by(TeachName.t_name).all()
       return render_template("teacher_up.html", subjects=subjects, teachers=teachers, teacher=teacher)


@app.route('/Subject', methods=['POST', 'GET'])
def Subject():
    if request.method == "POST":
        s_name = request.form['subj']

        if(s_name == ""):
            return "Произошла ошибка"

        subject = Subj(s_name = s_name)
        try:
            db.session.add(subject)
            db.session.commit()
            return redirect('/Subject')
        except:
            return "Произошла ошибка"
    else:
        subjects = Subj.query.order_by(Subj.s_name).all()
        return render_template("subj.html", subjects=subjects)


@app.route('/subject/<int:id>')
def subject_detail(id):
    subject = Subj.query.get(id)
    return render_template("subject_detail.html", subject=subject)


@app.route('/subject/<int:id>/del')
def subject_delete(id):
    subject = Subj.query.get_or_404(id)

    try:
        db.session.delete(subject)
        db.session.commit()
        return redirect('/Subject')
    except:
        return "Произошла ошибка"


@app.route('/TeachName', methods=['POST', 'GET'])
def Teachname():
    if request.method == "POST":
        t_name = request.form['t_name']

        if (t_name == ""):
            return "Произошла ошибка"

        teacher = TeachName(t_name = t_name)
        try:
            db.session.add(teacher)
            db.session.commit()
            return redirect('/TeachName')
        except:
            return "Произошла ошибка"
    else:
        teachers = TeachName.query.order_by(TeachName.t_name).all()
        return render_template("TeachName.html", teachers=teachers)


@app.route('/TeachName/<int:id>')
def TeachName_detail(id):
    teachName = TeachName.query.get(id)
    return render_template("TeachName_detail.html", teachName=teachName)


@app.route('/TeachName/<int:id>/del')
def TeachName_delete(id):
    teachName = TeachName.query.get_or_404(id)

    try:
        db.session.delete(teachName)
        db.session.commit()
        return redirect('/TeachName')
    except:
        return "Произошла ошибка"


@app.route('/Schedule')
def Schedule():
    teachers = Teacher.query.all()
    return render_template("schedule.html", teachers=teachers)


if __name__ == "__main__":
    app.run(debug = True)
