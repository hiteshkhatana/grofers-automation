import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from grofers import create
from grofers import func

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order',methods=['POST'])
def order():
    '''
    For rendering results on HTML GUI
    '''
    #int_features = [int(x) for x in request.form.values()]
    #final_features = [np.array(int_features)]
    #prediction = model.predict(final_features)

    #output = round(prediction[0], 2)
    data = create()

    all_p = func(data)

    return render_template('index.html', ordered_list='Employee Salary should be $ {}'.format(all_p))


if __name__ == "__main__":
    app.run(debug=True)