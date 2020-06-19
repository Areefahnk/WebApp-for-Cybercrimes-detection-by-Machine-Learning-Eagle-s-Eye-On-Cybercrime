import os
import PhishingDetection
import pickle
from flask import Flask
import numpy as np
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
model=pickle.load(open('model.pkl','rb'))

UPLOAD_FOLDER = '/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/result')
def result():
    urlname = request.args['name']
    result = PhishingDetection.getResult(urlname)
    return result


# @app.route('/upload')
# def upload():
# 	return 'yes'

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
            return "false"
        file = request.files['file']
        if file.filename == '':
            flash('no select file')
            return 'false'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            contents = file.read()
            with open("files/URL.txt", "wb") as f:
                f.write(contents)
            file.save = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return render_template("getInput.html")
            return render_template("cyberDetect.html")
    #return render_template("getInput.html")
    return render_template("cyberDetect.html")
@app.route('/botdetect/', methods=['POST','GET'])
def botnet():
    return render_template('botdetect.html')

@app.route('/getInput/', methods=['POST','GET'])
def pish():
    return render_template('getInput.html')


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_f = [(x) for x in request.form.values()]
    #print(int_f)
    bag_of_words = ["bot", "b0t", "cannabis", "tweet me", "mishear", "follow me", "updates every", "gorilla", "yes_ofc",
                    "forget", "expos", "kill", "clit", "bbb", "butt", "fuck", "XXX", "sex", "truthe", "fake", "anony",
                    "free", "virus", "funky", "RNA",
                    "kuck", "jargon", "nerd", "swag", "jack", "bang", "bonsai", "chick", "prison", "paper", "pokem",
                    "xx", "freak", "ffd"
        , "dunia", "clone", "genie", "bbb", "ffd", "onlyman", "emoji", "joke", "troll", "droop", "free", "every", "wow",
                    "cheese", "bio", "magic"
        , "wizard", "face"]
    x = int_f[0]
    #print(x)
    exist = False
    for word in bag_of_words:
        # print(word)
        if (word in x):
            # print(word)
            print(x)
            print('banned words "{}" found in str'.format(word))
            int_f[0] = 1
            print(int_f[0])
            exist = True

            break

    if (not exist):
        int_f[0] = 0
        print(int_f[0])
        print('Banned words not found in str')
    # for word in bag_of_words:
    # if (word in x):
    print(int_f)
    # print(type(int_f[0]))

    ####################
    x = int_f[1]
    print(x)
    exist = False
    for word in bag_of_words:
        # print(word)
        if (word in x):
            # print(word)
            print(x)
            print('banned words "{}" found in str'.format(word))
            int_f[1] = 1
            print(int_f[1])
            exist = True

            break

    if (not exist):
        int_f[1] = 0
        print(int_f[1])
        print('Banned words not found in str')

    ###################################################
    x = int_f[2]
    print(x)
    exist = False
    for word in bag_of_words:
        # print(word)
        if (word in x):
            # print(word)
            print(x)
            print('banned words "{}" found in str'.format(word))
            int_f[2] = 1
            print(int_f[2])
            exist = True

            break

    if (not exist):
        int_f[2] = 0
        print(int_f[2])
        print('Banned words not found in str')
    #########################################################################################
    x = int_f[3]
    print(x)
    exist = False
    for word in bag_of_words:
        # print(word)
        if (word in x):
            # print(word)
            print(x)
            print('banned words "{}" found in str'.format(word))
            int_f[3] = 1
            print(int_f[0])
            exist = True

            break

    if (not exist):
        int_f[3] = 0
        print(int_f[3])
        print('Banned words not found in str')
    ######################################
    int_f[4] = int(int_f[4])
    int_f[5] = int(int_f[5])
    int_f[6] = int(int_f[6])
    int_f[7] = int(int_f[7])
    int_f[8] = int(int_f[8])
    print(int_f)
    final = [np.array(int_f)]
    print(int_f)
    print(final)
    prediction = model.predict_proba(final)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)
    print(output)
    if output>str(0.5):
        return render_template('botdetect.html',pred='TwitterBot Detected\nProbability of being bot is {}'.format(output),bhai="Danger! It is a twitterbot")
    else:
        return render_template('botdetect.html',pred='Not a TwitterBot.\n Probability of being bot is {}'.format(output),bhai="It is not a twitterbot!")



if __name__ == '__main__':
    app.run(debug=True)
