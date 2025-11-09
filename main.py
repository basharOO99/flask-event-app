from flask import Flask, redirect, render_template, url_for, flash, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import EventForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skills.db'
app.config['SECRET_KEY'] = 'lolo'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ===== تعريف جدول Event مع حقل location =====
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)  # الحقل الجديد
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)  # تاريخ الإنشاء

    def __repr__(self):
        return f"Event('{self.name}', '{self.date_posted}')"


# ===== الصفحة الرئيسية =====
@app.route('/')
@app.route('/home')
def home():
    events = Event.query.order_by(Event.date_posted.desc()).all()
    return render_template('home.html', events=events)


# ===== صفحة تفاصيل الحدث =====
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)


# ===== إنشاء حدث جديد =====
@app.route('/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            date_posted=form.date.data or datetime.utcnow()
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', form=form)


# ===== تحديث حدث =====
@app.route('/update/<int:event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)  # pre-populate form with event data
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.location = form.location.data
        event.date_posted = form.date.data or event.date_posted
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    return render_template('create_event.html', form=form, title="Update Event")


# ===== حذف حدث =====
@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ينشئ الجداول إذا لم تكن موجودة
    app.run(debug=True, host='0.0.0.0', port=9000)
