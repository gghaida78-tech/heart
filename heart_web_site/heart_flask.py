from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

# تحميل النموذج
with open("heart_model.pkl", "rb") as f:
    model = pickle.load(f)

USERNAME = "admin"
PASSWORD = "1234"

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("input_data"))
        else:
            error = "اسم المستخدم أو كلمة المرور خاطئة"
    return render_template("main.html", page="login", error=error)

@app.route("/input", methods=["GET", "POST"])
def input_data():
    if request.method == "POST":
        try:
            features = [
                int(request.form["age"]),
                int(request.form["sex"]),
                int(request.form["cp"]),
                int(request.form["trtbps"]),
                int(request.form["chol"]),
                int(request.form["fbs"]),
                int(request.form["restecg"]),
                int(request.form["thalachh"]),
                int(request.form["exng"]),
                float(request.form["oldpeak"]),
                int(request.form["slp"]),
                int(request.form["caa"]),
                int(request.form["thall"]),
            ]
            prediction = model.predict([features])[0]
            return render_template("main.html", page="result", prediction=prediction)
        except Exception as e:
            return f"حدث خطأ أثناء التنبؤ: {e}"
    return render_template("main.html", page="input")

if __name__ == "__main__":
    app.run(debug=True)
