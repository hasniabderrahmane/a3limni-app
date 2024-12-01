const express = require('express');
const router = express.Router();
const { ensureAuthenticated } = require('../config/auth');
const Student = require('../models/Student');

// عرض قائمة الطلاب
router.get('/', ensureAuthenticated, async (req, res) => {
    try {
        const students = await Student.find().sort({ createdAt: -1 });
        res.render('students/index', { students });
    } catch (err) {
        req.flash('error_msg', 'حدث خطأ في جلب بيانات الطلاب');
        res.redirect('/');
    }
});

// صفحة إضافة طالب جديد
router.get('/add', ensureAuthenticated, (req, res) => {
    res.render('students/add');
});

// إضافة طالب جديد
router.post('/add', ensureAuthenticated, async (req, res) => {
    const {
        studentId,
        firstName,
        lastName,
        email,
        phone,
        dateOfBirth,
        major,
        entryYear
    } = req.body;

    try {
        const newStudent = new Student({
            studentId,
            firstName,
            lastName,
            email,
            phone,
            dateOfBirth,
            major,
            entryYear
        });

        await newStudent.save();
        req.flash('success_msg', 'تم إضافة الطالب بنجاح');
        res.redirect('/students');
    } catch (err) {
        req.flash('error_msg', 'حدث خطأ في إضافة الطالب');
        res.redirect('/students/add');
    }
});

// عرض تفاصيل طالب
router.get('/:id', ensureAuthenticated, async (req, res) => {
    try {
        const student = await Student.findById(req.params.id);
        if (!student) {
            req.flash('error_msg', 'الطالب غير موجود');
            return res.redirect('/students');
        }
        res.render('students/view', { student });
    } catch (err) {
        req.flash('error_msg', 'حدث خطأ في عرض بيانات الطالب');
        res.redirect('/students');
    }
});

// صفحة تعديل بيانات طالب
router.get('/edit/:id', ensureAuthenticated, async (req, res) => {
    try {
        const student = await Student.findById(req.params.id);
        if (!student) {
            req.flash('error_msg', 'الطالب غير موجود');
            return res.redirect('/students');
        }
        res.render('students/edit', { student });
    } catch (err) {
        req.flash('error_msg', 'حدث خطأ في تحميل بيانات الطالب');
        res.redirect('/students');
    }
});

// تحديث بيانات طالب
router.post('/edit/:id', ensureAuthenticated, async (req, res) => {
    try {
        await Student.findByIdAndUpdate(req.params.id, req.body);
        req.flash('success_msg', 'تم تحديث بيانات الطالب بنجاح');
        res.redirect('/students');
    } catch (err) {
        req.flash('error_msg', 'حدث خطأ في تحديث بيانات الطالب');
        res.redirect(`/students/edit/${req.params.id}`);
    }
});

// حذف طالب
router.delete('/:id', ensureAuthenticated, async (req, res) => {
    try {
        await Student.findByIdAndDelete(req.params.id);
        req.flash('success_msg', 'تم حذف الطالب بنجاح');
        res.redirect('/students');
    } catch (err) {
        req.flash('error_msg', 'حدث خطأ في حذف الطالب');
        res.redirect('/students');
    }
});

module.exports = router;
