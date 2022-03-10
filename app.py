from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        bed = int(request.form['bed'])
        bath=float(request.form['bath'])
        car=int(request.form['car'])

        Suburb=request.form['Suburb']
        if(Suburb=='North Ryde'):
                North_Ryde=1
                Macquarie_Park=0
                East_Ryde=0
        elif(Suburb=='Macquarie Park'):
                North_Ryde=0
                Macquarie_Park=1
                East_Ryde=0
        else:
                North_Ryde=0
                Macquarie_Park=0
                East_Ryde=1
        propType=request.form['propType']
        if(propType=='Duplex/Semi-detached'):
            duplex=1
            house=0
            townhouse=0
            villa=0
        elif(propType=='House'):
            duplex=0
            house=1
            townhouse=0
            villa=0	
        elif(propType=='Townhouse'):
            duplex=0
            house=0
            townhouse=1
            villa=0	
        else:
            duplex=0
            house=0
            townhouse=0
            villa=1	
        prediction=model.predict([[bed,bath,car,East_Ryde,Macquarie_Park,North_Ryde,duplex,house,townhouse,villa]])
        
        output=int(prediction[0]/1000)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this house")
        else:
            return render_template('index.html',prediction_text="You Can Sell your "+propType+" at "+Suburb+" with "+str(bed)+" bedroom(s), "+str(int(bath))+" bathroom(s) "+str(car)+" and car parking space(s) at AUD ${}K".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

