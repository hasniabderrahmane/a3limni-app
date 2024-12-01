from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class StudentForm(FlaskForm):
    student_id = StringField('الرقم الجامعي',
                           validators=[DataRequired(), Length(min=5, max=20)])
    first_name = StringField('الاسم الأول',
                           validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('الاسم الأخير',
                          validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('البريد الإلكتروني',
                       validators=[DataRequired(), Email()])
    phone = StringField('رقم الهاتف',
                       validators=[Length(max=20)])
    date_of_birth = DateField('تاريخ الميلاد',
                             validators=[DataRequired()])
    major = StringField('التخصص',
                       validators=[DataRequired(), Length(max=100)])
    entry_year = IntegerField('سنة الدخول',
                             validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    gpa = FloatField('المعدل التراكمي',
                     validators=[NumberRange(min=0, max=4)])
    submit = SubmitField('حفظ')
