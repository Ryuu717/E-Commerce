# from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from wtforms import validators, ValidationError
# from wtforms.validators import DataRequired, URL
# from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo


class RegisterForm(FlaskForm):
    first_name = TextField("First Name",validators=[validators.Required(), Length(min=2, max=50)], render_kw={"placeholder": "ex) John"})
    last_name = TextField("Last Name",validators=[validators.Required(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Wick"})
    address = TextField("Address", render_kw={"placeholder": "ex) postal code, street, city, country"})
    phone = TextField("Phone",validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "ex) 012-3456-7890"})
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) abc@gmail.com"})
    card_number = TextField("Card Number", render_kw={"placeholder": "ex) 0000-0000-0000"})
    password = PasswordField("Password", validators=[validators.Required()], render_kw={"placeholder": "ex) abc123"})
    re_enter_password = PasswordField("Re-Enter password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    submit = SubmitField("Submit")

class RegisterGuestForm(FlaskForm):
    first_name = TextField("First Name",validators=[validators.Required(), Length(min=2, max=50)], render_kw={"placeholder": "ex) John"})
    last_name = TextField("Last Name",validators=[validators.Required(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Wick"})
    address = TextField("Address", render_kw={"placeholder": "ex) postal code, street, city, country"})
    phone = TextField("Phone",validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "ex) 012-3456-7890"})
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) abc@gmail.com"})
    card_number = TextField("Card Number", render_kw={"placeholder": "ex) 0000-0000-0000"})
    submit = SubmitField("Submit")



# # Without validation
# class RegisterForm(FlaskForm):
#     first_name = TextField("First Name")
#     last_name = TextField("Last Name")
#     address = TextField("Address")
#     phone = TextField("Phone")
#     email = TextField("Email")
#     card_number = TextField("Card Number")
#     password = PasswordField("Password")
#     re_enter_password = PasswordField("Re-Enter password")
#     submit = SubmitField("Submit")

class RegisteredForm(FlaskForm):
    first_name = TextField("First Name",validators=[validators.Required()])
    last_name = TextField("Last Name",validators=[validators.Required()])
    address = TextField("Address",validators=[validators.Required()])
    phone = TextField("Phone",validators=[DataRequired()])
    email = TextField("Email",validators=[DataRequired()])
    card_number = TextField("Card Number",validators=[DataRequired()])
    # password = PasswordField("Password", validators=[validators.Required()], render_kw={"placeholder": "ex) abc123"})
    # re_enter_password = PasswordField("Re-Enter password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    # submit = SubmitField("Submit")
