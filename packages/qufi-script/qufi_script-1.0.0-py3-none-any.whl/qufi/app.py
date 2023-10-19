from flask import session, Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired

from qufi import QubeFidel

app = Flask(__name__)
app.config["SECRET_KEY"] = "testing"


class Form(FlaskForm):
    inputer = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Convert")
    output = TextAreaField(id="output")


@app.route('/', methods=["GET", "POST"])
def index():
    form = Form()
    qufi = QubeFidel()
    if form.validate_on_submit():
        session['text'] = form.inputer.data
        form.inputer.data = ""
        return redirect('/')

    return render_template("app.html", form=form, text=qufi.convert(session.get('text') or ""))


if __name__ == "__main__":
    app.run(debug=True)