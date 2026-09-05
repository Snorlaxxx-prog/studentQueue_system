from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "studentqueue_secret_key"

admin = {
    "username": "ckcmadmin",
    "password": "1234",
    "name": "Dolfh"
}

reset_password = "gwapoko"


waiting_queue = []
completed_students = []

next_number = 1


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == admin["username"] and password == admin["password"]:
            session["admin_name"] = admin["name"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "admin_name" not in session:
        return redirect(url_for("login"))

    current_student = waiting_queue[0] if waiting_queue else None

    return render_template(
        "dashboard.html",
        admin_name=session["admin_name"],
        current_student=current_student
    )


@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    global next_number

    if "admin_name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        student_name = request.form["student_name"]

        student = {
            "number": next_number,
            "name": student_name
        }

        waiting_queue.append(student)
        next_number += 1

        return redirect(
            url_for(
                "ticket",
                number=student["number"],
                name=student["name"]
            )
        )

    return render_template("add_student.html")


@app.route("/ticket")
def ticket():
    if "admin_name" not in session:
        return redirect(url_for("login"))

    number = request.args.get("number")
    name = request.args.get("name")

    return render_template(
        "ticket.html",
        number=number,
        name=name
    )


@app.route("/waiting-queue")
def waiting_queue_page():
    if "admin_name" not in session:
        return redirect(url_for("login"))

    return render_template(
        "waiting_queue.html",
        students=waiting_queue
    )


@app.route("/mark-done")
def mark_done():
    if "admin_name" not in session:
        return redirect(url_for("login"))

    if waiting_queue:
        student = waiting_queue.pop(0)
        completed_students.append(student)

    return redirect(url_for("dashboard"))

@app.route("/reset-queue", methods=["GET", "POST"])
def reset_queue():
    global waiting_queue, next_number

    if "admin_name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form["password"]

        if password == reset_password:
            waiting_queue.clear()
            next_number = 1

            return redirect(url_for("dashboard"))

        return render_template(
            "reset_queue.html",
            error="Incorrect reset password"
        )

    return render_template("reset_queue.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)