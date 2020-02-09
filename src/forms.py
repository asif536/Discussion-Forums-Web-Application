from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField,StringField

class PostForm(FlaskForm):
    title= StringField('Title',validators=[DataRequired()])
    content = PageDownField(validators=[DataRequired()],render_kw={"placeholder": "Enter the Content"})
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = PageDownField("Enter the Content",validators=[DataRequired()],render_kw={"placeholder": "Enter the Comment"})
    submit = SubmitField('Post')