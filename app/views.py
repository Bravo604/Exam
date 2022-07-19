from flask import request, render_template, url_for, redirect, flash
from . import models, forms, db, login_manager
from flask_login import login_user, logout_user, login_required, current_user


# Employee func
def index():
    employees = models.Employee.query.all()
    return render_template('index.html', employees=employees)


@login_required
def employee_create():
    form = forms.EmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = models.Employee(fullname=request.form.get('fullname'), phone=request.form.get('phone'),
                                       short_info=request.form.get('short_info'),
                                       experience=request.form.get('experience'),
                                       preferred_position=request.form.get('preferred_position'),
                                       user_id=current_user.id)
            db.session.add(employee)
            db.session.commit()
            flash('Вы успешно добавили работника', category='success')
            return redirect(url_for('index'))
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('employee_create.html', form=form)


def employee_detail(employee_id):
    employee = models.Employee.query.filter_by(id=employee_id).first()
    return render_template('employee_detail.html', employee=employee)


@login_required
def employee_update(employee_id):
    employee = models.Employee.query.filter_by(id=employee_id).first()
    if employee:
        if employee.user_id == current_user.id:
            form = forms.EmployeeForm(obj=employee)
            if request.method == 'POST':
                if form.validate_on_submit():
                    fullname = request.form.get('fullname')
                    phone = request.form.get('phone')
                    short_info = request.form.get('short_info')
                    experience = request.form.get('experience')
                    preferred_position = request.form.get('preferred_position')
                    employee.fullname = fullname
                    employee.phone = phone
                    employee.short_info = short_info
                    employee.experience = experience
                    employee.preferred_position = preferred_position
                    db.session.commit()
                    flash('Работник обновлен', category='succes')
                    return redirect(url_for('index'))
                if form.errors:
                    for errors in form.errors.values():
                        for error in errors:
                            flash(error, category='danger')

            return render_template('employee_update.html', employee=employee, form=form)
        else:
            flash('У вас недостаточно прав', category='danger')
            return redirect(url_for('index'))
    else:
        flash('Работник не найден', category='danger')
        return redirect(url_for('index'))


@login_required
def employee_delete(employee_id):
    employee = models.Employee.query.filter_by(id=employee_id).first()
    if employee:
        form = forms.EmployeeForm(obj=employee)
        if employee.user_id == current_user.id:
            if request.method == 'POST':
                db.session.delete(employee)
                db.session.commit()
                flash('Работник успешно удален', category='success')
                return redirect(url_for('index'))
            else:
                return render_template('employee_delete.html', employee=employee, form=form)
        else:
            flash('У вас нет права для удаления записи', category='danger')
            return redirect(url_for('index'))
    else:
        flash('Работник не найден', category='danger')
        return redirect(url_for('index'))


# USER fUNC
def register():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User(username=request.form.get('username'), password=request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались', category='success')
            return redirect(url_for('login'))
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('register.html', form=form)


def login():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Вы успешно вошли', category='success')
                return redirect(url_for('index'))
            else:
                flash('Неверный пароль или Логин', category='danger')

        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('login.html', form=form)


def logout():
    logout_user()
    flash('Вы успешно вошли', category='success')
    return redirect(url_for('index'))
