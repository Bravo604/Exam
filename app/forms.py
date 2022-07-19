from flask_wtf import FlaskForm
import wtforms as wf


class UserForm(FlaskForm):
    username = wf.StringField('Пользователь', validators=[wf.validators.DataRequired()])
    password = wf.PasswordField('Пароль', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=8, max=64)
    ])
    submit = wf.SubmitField('OK')


class EmployeeForm(FlaskForm):
    fullname = wf.StringField('ФИО клиента', validators=[wf.validators.DataRequired()])
    phone = wf.StringField('Номер телефона', validators=[wf.validators.DataRequired()])
    short_info = wf.TextAreaField('Краткая информация', validators=[wf.validators.DataRequired()])
    experience = wf.IntegerField('Опыт работы', validators=[wf.validators.DataRequired()])
    preferred_position = wf.StringField('Предпочитаемая позиция')
    submit = wf.SubmitField('OK')

    def validate(self):
        if not super().validate():
            return False
        if " " not in self.fullname.data:
            self.fullname.errors.append("ФИО нужно писать раздельно")
            return False
        return True
