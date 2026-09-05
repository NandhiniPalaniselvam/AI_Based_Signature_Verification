import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.utils import secure_filename

# ==================================================
# Flask App
# ==================================================

app = Flask(__name__)
app.secret_key = "signature123"

# ==================================================
# Upload Folder
# ==================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================================================
# MySQL Database Connection
# ==================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="signature_db"
    )

# ==================================================
# Home
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==================================================
# Login Page
# ==================================================

@app.route("/login")
def login():
    return render_template("login.html")


# ==================================================
# Register Page
# ==================================================

@app.route("/register")
def register():
    return render_template("register.html")


# ==================================================
# Register User
# ==================================================

@app.route("/register_user", methods=["POST"])
def register_user():

    fullname = request.form.get("fullname")
    username = request.form.get("username")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    try:

        cursor.execute(
            """
            INSERT INTO users
            (fullname, username, email, phone, password)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                fullname,
                username,
                email,
                phone,
                password
            )
        )

        conn.commit()

        return """
        <script>
        alert("Registration Successful");
        window.location="/login";
        </script>
        """

    except mysql.connector.IntegrityError:

        return """
        <script>
        alert("Email or Username already exists");
        window.location="/register";
        </script>
        """

    finally:

        cursor.close()
        conn.close()


# ==================================================
# Login User
# ==================================================

@app.route("/login_user", methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db_connection()

    # IMPORTANT:
    # buffered=True fixes "Unread result found"
    cursor = conn.cursor(
        dictionary=True,
        buffered=True
    )

    try:

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if user is None:

            return """
            <script>
            alert("Email not found");
            window.location="/login";
            </script>
            """

        if user["password"] == password:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/dashboard")

        else:

            return """
            <script>
            alert("Invalid Password");
            window.location="/login";
            </script>
            """

    finally:

        cursor.close()
        conn.close()


# ==================================================
# Dashboard
# ==================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# ==================================================
# Verify Page
# ==================================================

@app.route("/verify")
def verify():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("verify.html")


# ==================================================
# Verify Signature Upload
# ==================================================

@app.route("/verify_signature", methods=["POST"])
def verify_signature():

    if "user_id" not in session:
        return redirect("/login")

    reference = request.files.get("reference_signature")
    verify = request.files.get("verify_signature")

    if not reference or not verify:
        return "Please upload both signatures."

    reference_filename = secure_filename(
        reference.filename
    )

    verify_filename = secure_filename(
        verify.filename
    )

    reference_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "reference_" + reference_filename
    )

    verify_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "original_" + verify_filename
    )

    reference.save(reference_path)
    verify.save(verify_path)

    # ==================================================
    # Demo Result
    # ==================================================

    result = "Genuine"
    similarity = 92.50

    # ==================================================
    # Save Verification History
    # ==================================================

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    try:

        cursor.execute(
            """
            INSERT INTO verification_history
            (user_id, reference_image, original_image, result, similarity)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                reference_filename,
                verify_filename,
                result,
                similarity
            )
        )

        conn.commit()

    finally:

        cursor.close()
        conn.close()

    return redirect("/history")


# ==================================================
# Result
# ==================================================

@app.route("/result")
def result():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("result.html")


# ==================================================
# History
# ==================================================

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True,
        buffered=True
    )

    try:

        cursor.execute(
            """
            SELECT *
            FROM verification_history
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (session["user_id"],)
        )

        history_data = cursor.fetchall()

    finally:

        cursor.close()
        conn.close()

    return render_template(
        "history.html",
        history=history_data
    )


# ==================================================
# About
# ==================================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==================================================
# Contact
# ==================================================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ==================================================
# Logout
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==================================================
# Run Flask
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)