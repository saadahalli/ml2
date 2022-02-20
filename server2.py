from flask import Flask, render_template, request
import numpy as np


import json
import joblib

app = Flask(__name__)




gbc = joblib.load('gbc_SBA_Loann')




# Prediction Page
@app.route('/')
def predict():
    return render_template('predict.html')

# Result Page
@app.route('/SBA_Loan_Result', methods=["POST", "GET"])
def SBA_Loan_predict():
    if request.method == "POST":
        input = request.form
        Term = float(input['Term'])
        NewExist = float(input['NewExist'])
        if NewExist == 1:
            NewExistRes = 'Existing Business'
        else:
            NewExistRes = 'New Business'
        GrAppv = float(input['GrAppv'])
        SBA_Appv = float(input['SBA_Appv'])
        RevLineCr = float(input['RevLineCr'])
        if RevLineCr == 1:
            RevLineCrRes = 'Yes'
        else:
            RevLineCrRes = 'No'
        LowDoc = float(input['LowDoc'])
        if LowDoc == 1:
            LowDocRes = 'Yes'
        else:
            LowDocRes = 'No'
        NAICS = input['NAICS']
        NAICS_11 = 0
        NAICS_21 = 0
        NAICS_22 = 0
        NAICS_23 = 0
        NAICS_31_33 = 0
        NAICS_42 = 0
        NAICS_44_45 = 0
        NAICS_48_49 = 0
        NAICS_51 = 0
        NAICS_52 = 0
        NAICS_53 = 0
        NAICS_54 = 0
        NAICS_55 = 0
        NAICS_55 = 0
        NAICS_56 = 0
        NAICS_61 = 0
        NAICS_62 = 0
        NAICS_71 = 0
        NAICS_72 = 0
        NAICS_81 = 0
        NAICS_92 = 0
        if NAICS == '11':
            NAICS_11 += 1
            NAICSRes = 'Agriculture, forestry, fishing and hunting'
        elif NAICS == '21':
            NAICS_21 += 1
            NAICSRes = 'Mining, quarrying, and oil and gas extraction'
        elif NAICS == '22':
            NAICS_22 += 1
            NAICSRes = 'Utilities'
        elif NAICS == '23':
            NAICS_23 += 1
            NAICSRes = 'Construction'
        elif NAICS == '31-33':
            NAICS_31_33 += 1
            NAICSRes = 'Manufacturing'
        elif NAICS == '42':
            NAICS_42 += 1
            NAICSRes = 'Wholesale trade'
        elif NAICS == '44-45':
            NAICS_44_45 += 1
            NAICSRes = 'Retail trade'
        elif NAICS == '48-49':
            NAICS_48_49 += 1
            NAICSRes = 'Transportation and warehousing'
        elif NAICS == '51':
            NAICS_51 += 1
            NAICSRes = 'Information'
        elif NAICS == '52':
            NAICS_52 += 1
            NAICSRes = 'Finance and insurance'
        elif NAICS == '53':
            NAICS_53 += 1
            NAICSRes = 'Real estate and rental and leasing'
        elif NAICS == '54':
            NAICS_54 += 1
            NAICSRes = 'Professional, scientific, and technical services'
        elif NAICS == '55':
            NAICS_55 += 1
            NAICSRes = 'Management of companies and enterprises'
        elif NAICS == '56':
            NAICS_56 += 1
            NAICSRes = 'Administrative/support & waste management/remediation Service'
        elif NAICS == '61':
            NAICS_61 += 1
            NAICSRes = 'Educational services'
        elif NAICS == '62':
            NAICS_62 += 1
            NAICSRes = 'Health care and social assistance'
        elif NAICS == '71':
            NAICS_71 += 1
            NAICSRes = 'Arts, entertainment, and recreation'
        elif NAICS == '72':
            NAICS_72 += 1
            NAICSRes = 'Accommodation and food services'
        elif NAICS == '81':
            NAICS_81 += 1
            NAICSRes = 'Other services (except public administration)'
        elif NAICS == '92':
            NAICS_92 += 1
            NAICSRes = 'Public administration'

# Term, NewExist, GrAppv, SBA_Appv, RevLineCr, Lowdoc, NAICS_11
        pred = gbc.predict([[Term, NewExist, GrAppv, SBA_Appv, RevLineCr, LowDoc, NAICS_11, NAICS_21, NAICS_22,
        NAICS_23, NAICS_31_33, NAICS_42, NAICS_44_45, NAICS_48_49, NAICS_51, NAICS_52, NAICS_53, NAICS_54, NAICS_55,
        NAICS_56, NAICS_61, NAICS_62, NAICS_71, NAICS_72, NAICS_81, NAICS_92]])[0]
        
        pred_proba = gbc.predict_proba([[Term, NewExist, GrAppv, SBA_Appv, RevLineCr, LowDoc, NAICS_11, NAICS_21, NAICS_22,
        NAICS_23, NAICS_31_33, NAICS_42, NAICS_44_45, NAICS_48_49, NAICS_51, NAICS_52, NAICS_53, NAICS_54, NAICS_55,
        NAICS_56, NAICS_61, NAICS_62, NAICS_71, NAICS_72, NAICS_81, NAICS_92]])
        
        pred_and_proba = f"{round(np.max(pred_proba)*100,2)}% {'Approuvé' if pred == 1 else 'Refusé'}"

        return render_template('result.html',
        data=input, prediction=pred_and_proba, Term=input['Term'],
        NewExist=NewExistRes, GrAppv=input['GrAppv'],
        SBA_Appv=input['SBA_Appv'], RevLineCr=RevLineCrRes,
        LowDoc=LowDocRes, NAICS=NAICSRes)

if __name__ == '__main__':
    
    app.run(debug=True)