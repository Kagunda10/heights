from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func
from send_email import send_email

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kqapusvawdjagy:9cbd635d91ee6b6134c2fe4d6a98b4a56297e8a6d623514ac8279e7cb84c819f@ec2-184-73-250-50.compute-1.amazonaws.com:5432/d86ei5njc0m00u?sslmode=require'
db = SQLAlchemy(app)
# Models
class Data(db.Model):
	__tableanme__="data"
	id = db.Column(db.Integer, primary_key=True)
	email_ = db.Column(db.String(120), unique=True)
	height_ = db.Column(db.Integer)

	def __init__(self, email_, height_):
		self.email_ = email_
		self.height_ = height_

@app.route("/")
def index():
	return render_template("index.html")


# Form Values are being passed to this method
@app.route("/success", methods=['POST'])
def success():
	# Request Object has the following methods(form, args, cookies, files, method)
	if request.method=='POST':
		email=request.form['email_name']
		height = request.form['height_name']
		data = Data(email, height)
		
		# Remove duplicates
		if db.session.query(Data).filter(Data.email_ == email).count() == 0:
			db.session.add(data)
			db.session.commit()
			average_height = db.session.query(func.avg(Data.height_)).scalar()
			average_height = round(average_height, 1)
			count = db.session.query(Data.height_).count()
			send_email(email, height, average_height, count)
			return render_template("success.html")

	return render_template("index.html", text="The email is aleady in use!")

if __name__ == '__main__':
	app.debug=True
	app.run()