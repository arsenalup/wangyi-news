from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField(label='新闻标题', validators=[DataRequired("请输入标题")], description='请输入标题',
                        render_kw={'required':'required', 'class':'form-control'})
    content = TextAreaField(label='新闻内容', validators=[DataRequired("请输入内容")], description='请输入内容',
                        render_kw={'required':'required', 'class':'form-control'})
    image = StringField(label='新闻图片', validators=[DataRequired("请输入标题")], description='请输入图片地址',
                        render_kw={'required':'required', 'class':'form-control'})
    type = SelectField('新闻类型',
                        choices=[('推荐', '推荐'), ('百家', '百家'), ('本地', '本地'), ('图片', '图片')],
                        description='请输入标题')
    author = StringField(label='新闻作者', description='请输入作者',
                        render_kw={'required': 'required', 'class': 'form-control'})
    is_valid = BooleanField('新闻是否显示', validators=[DataRequired('显示')], default=True)
    submit = SubmitField('提交')