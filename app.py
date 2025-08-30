from flask import Flask, render_template, request, flash
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("placemennt_modal.pkl", "rb"))
app.secret_key = "secret122"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        gpa = request.form.get("GPA", "").strip()
        iq = request.form.get("IQ", "").strip()

        if gpa == '' or iq == '':
            flash("Enter the CGPA AND IQ FIRST")
            return render_template("index.html")
        
        gpa = float(gpa)
        iq = float(iq)

        if not (0 <= gpa <= 10) or not (50 <= iq <= 200):
            flash("You entered values out of range")
            return render_template("index.html")
        
        # Prepare input
        X = pd.DataFrame([[gpa, iq]], columns=["CGPA", "IQ"])

        # Prediction
        pred = model.predict(X)[0]
        result_label = "Placed" if int(pred) == 1 else "Not Placed"

        prob = None
        # If model supports probability prediction
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X)[0][int(pred)]
            prob = round(float(prob) * 100, 2)  # convert to percentage

        return render_template("index.html", result=result_label, prob=prob, cgpa=gpa, iq=iq)

    except Exception as e:
        flash(f"Error: {e}")
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
