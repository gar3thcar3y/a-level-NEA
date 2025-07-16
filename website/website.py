from flask import Flask, render_template, send_file
import pickle
from io import StringIO, BytesIO
from skimage.io import imsave
import PIL

app = Flask(__name__)

import mysql.connector

db = db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password1",
        database="register",
    )
mycursor = db.cursor()


@app.route("/")
def index():
    mycursor.execute(f"select name, present from people;")
    people = mycursor.fetchall()

    mycursor.execute(f"select * from currently_in;")
    currently_in = mycursor.fetchall()

    mycursor.execute(f"select * from times_in;")
    times_in = mycursor.fetchall()

    return render_template("index.html", people=people, currently_in=currently_in, times_in=times_in)



from io import BytesIO  # Import BytesIO from io module
import pickle

@app.route("/img/<name>")
def getimg(name):
    mycursor.execute(f"select picture from people where name = '{name}';")
    img_data = mycursor.fetchone()[0]
    img = pickle.loads(img_data)
    img_buffer = BytesIO()
    imsave(img_buffer, img, plugin='pil', format_str='png')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
