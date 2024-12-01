from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required
from a3limni import db
from a3limni.models import Student
from a3limni.students.forms import StudentForm
import pandas as pd
from datetime import datetime

students = Blueprint('students', __name__)

@students.route("/students")
@login_required
def list_students():
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('students/list.html',
                         students=pagination.items,
                         page=page,
                         pages=pagination.pages)

@students.route("/students/add", methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            student_id=form.student_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            date_of_birth=form.date_of_birth.data,
            major=form.major.data,
            entry_year=form.entry_year.data
        )
        db.session.add(student)
        db.session.commit()
        flash('تم إضافة الطالب بنجاح!', 'success')
        return redirect(url_for('students.list_students'))
    return render_template('students/add.html', form=form, title='إضافة طالب جديد')

@students.route("/students/edit/<int:student_id>", methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.student_id = form.student_id.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.date_of_birth = form.date_of_birth.data
        student.major = form.major.data
        student.entry_year = form.entry_year.data
        db.session.commit()
        flash('تم تحديث بيانات الطالب بنجاح!', 'success')
        return redirect(url_for('students.list_students'))
    return render_template('students/edit.html', form=form, student=student, title='تعديل بيانات الطالب')

@students.route("/students/delete/<int:student_id>")
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('تم حذف الطالب بنجاح!', 'success')
    return redirect(url_for('students.list_students'))

@students.route("/students/view/<int:student_id>")
@login_required
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('students/view.html', student=student, title='عرض بيانات الطالب')

@students.route("/students/export")
@login_required
def export_excel():
    students = Student.query.all()
    data = []
    for student in students:
        data.append({
            'الرقم الجامعي': student.student_id,
            'الاسم الأول': student.first_name,
            'الاسم الأخير': student.last_name,
            'البريد الإلكتروني': student.email,
            'الهاتف': student.phone,
            'تاريخ الميلاد': student.date_of_birth,
            'التخصص': student.major,
            'سنة الدخول': student.entry_year,
            'المعدل التراكمي': student.gpa
        })
    
    df = pd.DataFrame(data)
    filename = f'students_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    df.to_excel(f'a3limni/static/exports/{filename}', index=False)
    
    return redirect(url_for('static', filename=f'exports/{filename}'))
