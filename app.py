# app.py
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

data_file = "data.json"

@app.route("/", methods=["GET", "POST"])
def calculate_bmi():
    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        age = int(request.form["age"])
        gender = request.form["gender"]
        
        # Calculate BMI and get status
        bmi, status = calculate_bmi_value(weight, height)
        
        if bmi is None:
            return render_template("result.html", bmi_error=status)
        
        # Store data
        store_data(age, gender, height, weight, bmi, status)
        
        return render_template("result.html", bmi=bmi, status=status)
    
    # Retrieve old readings
    old_readings = retrieve_data()
    return render_template("index.html", old_readings=old_readings)

def calculate_bmi_value(weight, height):
    try:
        height_in_meters = height / 100
        bmi = weight / (height_in_meters ** 2)
        bmi = round(bmi, 2)

        if bmi < 18.5:
            status = "Underweight"
        elif 18.5 <= bmi < 24.9:
            status = "Normal Weight"
        elif 25 <= bmi < 29.9:
            status = "Overweight"
        else:
            status = "Obese"
        
        return bmi, status
    except ZeroDivisionError:
        return None, "Invalid input: Height cannot be zero"
    except ValueError:
        return None, "Invalid input: Please enter valid numeric values for weight and height"

def store_data(age, gender, height, weight, bmi, status):
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    data.append({
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "status": status
    })
    
    with open(data_file, "w") as file:
        json.dump(data, file)

def retrieve_data():
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []

@app.route("/show", methods=["GET"])
def show_data():
    # Retrieve and display old readings
    old_readings = retrieve_data()
    return render_template("show.html", old_readings=old_readings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

