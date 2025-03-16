from flask import Flask, render_template, Response, request, redirect, session, jsonify, url_for
import cv2
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

camera = cv2.VideoCapture(0)

# Ensure models directory exists
MODEL_PATH = os.path.join("static", "models", "human_model.glb")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def detect_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    ret, frame = camera.read()

    if not ret:
        return False
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    return len(faces) > 0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["age"] = request.form["age"]
        session["gender"] = request.form["gender"]
        return redirect("/scanning")
    return render_template("index.html")

@app.route("/scanning", methods=["GET"])
def scanning():
    return render_template("scanning.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/check-face", methods=["GET"])
def check_face():
    if detect_face():
        return jsonify({"status": "done"})
    else:
        return jsonify({"status": "failed"})

@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html", name=session.get("name", "User"))

@app.route("/virtual_tryon")
def virtual_tryon():
    if not os.path.exists(MODEL_PATH):
        return "3D Model not found. Please check your static/models/ directory.", 404
    return render_template("virtual_tryon.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
