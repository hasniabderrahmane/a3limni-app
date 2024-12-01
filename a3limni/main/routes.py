from flask import Blueprint, render_template
from flask_login import login_required
from a3limni.models import Student, User

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        total_students = Student.query.count()
        active_students = Student.query.filter_by(is_active=True).count()
        total_courses = 0  # يمكن إضافة نموذج للمقررات لاحقاً
        recent_activities = []  # يمكن إضافة نموذج للنشاطات لاحقاً
        
        return render_template('home.html',
                             total_students=total_students,
                             active_students=active_students,
                             total_courses=total_courses,
                             recent_activities=recent_activities)
    return render_template('home.html')
