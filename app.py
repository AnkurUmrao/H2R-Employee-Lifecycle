from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json, os, uuid
from datetime import datetime, date
from hr_processes import (
    hire_employee, get_all_employees, get_employee, update_employee,
    terminate_employee, process_payroll, record_leave, add_training,
    promote_employee, get_dashboard_stats, get_payroll_history
)

app = Flask(__name__)
app.secret_key = "sap_hr_h2r_secret_2026"

@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    employees = get_all_employees()
    recent = sorted(employees, key=lambda e: e.get("hire_date",""), reverse=True)[:5]
    return render_template("dashboard.html", stats=stats, recent=recent)

@app.route("/hire", methods=["GET", "POST"])
def hire():
    if request.method == "POST":
        data = {
            "first_name":     request.form["first_name"],
            "last_name":      request.form["last_name"],
            "email":          request.form["email"],
            "phone":          request.form["phone"],
            "gender":         request.form["gender"],
            "dob":            request.form["dob"],
            "designation":    request.form["designation"],
            "department":     request.form["department"],
            "cost_center":    request.form["cost_center"],
            "employment_type":request.form["employment_type"],
            "hire_date":      request.form["hire_date"],
            "basic_salary":   float(request.form["basic_salary"]),
            "manager":        request.form.get("manager",""),
            "location":       request.form["location"],
            "hra_pct":        0.40,
            "ta_fixed":       1600,
        }
        emp_id = hire_employee(data)
        flash(f"✅ Employee hired successfully! Employee ID: {emp_id}", "success")
        return redirect(url_for("employee_detail", emp_id=emp_id))
    managers = [e for e in get_all_employees() if e.get("status") == "Active"]
    return render_template("hire.html", managers=managers)

@app.route("/employees")
def employee_list():
    dept_filter = request.args.get("dept", "")
    status_filter = request.args.get("status", "")
    employees = get_all_employees()
    if dept_filter:
        employees = [e for e in employees if e.get("department") == dept_filter]
    if status_filter:
        employees = [e for e in employees if e.get("status") == status_filter]
    departments = sorted(set(e.get("department","") for e in get_all_employees()))
    return render_template("employee_list.html", employees=employees,
                           departments=departments, dept_filter=dept_filter,
                           status_filter=status_filter)

@app.route("/employee/<emp_id>")
def employee_detail(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        flash("Employee not found.", "danger")
        return redirect(url_for("employee_list"))
    payroll_hist = get_payroll_history(emp_id)
    return render_template("employee_detail.html", emp=emp, payroll_hist=payroll_hist)

@app.route("/employee/<emp_id>/edit", methods=["GET", "POST"])
def edit_employee(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        flash("Employee not found.", "danger")
        return redirect(url_for("employee_list"))
    if request.method == "POST":
        updates = {
            "phone":       request.form["phone"],
            "email":       request.form["email"],
            "designation": request.form["designation"],
            "department":  request.form["department"],
            "location":    request.form["location"],
            "basic_salary":float(request.form["basic_salary"]),
        }
        update_employee(emp_id, updates)
        flash("✅ Employee record updated (PA30 — Maintain HR Master Data).", "success")
        return redirect(url_for("employee_detail", emp_id=emp_id))
    return render_template("edit_employee.html", emp=emp)

@app.route("/payroll", methods=["GET", "POST"])
def payroll():
    employees = [e for e in get_all_employees() if e.get("status") == "Active"]
    result = None
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        month  = request.form["month"]
        year   = request.form["year"]
        result = process_payroll(emp_id, int(month), int(year))
        if result:
            flash(f"✅ Payroll processed for {result['emp_name']} — Net Pay: ₹{result['net_pay']:,.2f}", "success")
    return render_template("payroll.html", employees=employees, result=result)

@app.route("/leave", methods=["GET", "POST"])
def leave():
    employees = [e for e in get_all_employees() if e.get("status") == "Active"]
    if request.method == "POST":
        emp_id     = request.form["emp_id"]
        leave_type = request.form["leave_type"]
        start_date = request.form["start_date"]
        end_date   = request.form["end_date"]
        reason     = request.form["reason"]
        record_leave(emp_id, leave_type, start_date, end_date, reason)
        flash("✅ Leave recorded successfully in Time Management (IT2001).", "success")
        return redirect(url_for("leave"))
    return render_template("leave.html", employees=employees)

@app.route("/training", methods=["GET", "POST"])
def training():
    employees = [e for e in get_all_employees() if e.get("status") == "Active"]
    if request.method == "POST":
        emp_id   = request.form["emp_id"]
        course   = request.form["course"]
        provider = request.form["provider"]
        start    = request.form["start_date"]
        end      = request.form["end_date"]
        status   = request.form["status"]
        add_training(emp_id, course, provider, start, end, status)
        flash("✅ Training record added (LSO — Learning Solution).", "success")
        return redirect(url_for("training"))
    return render_template("training.html", employees=employees)

@app.route("/promote/<emp_id>", methods=["GET", "POST"])
def promote(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        flash("Employee not found.", "danger")
        return redirect(url_for("employee_list"))
    if request.method == "POST":
        updates = {
            "designation":  request.form["designation"],
            "department":   request.form["department"],
            "basic_salary": float(request.form["basic_salary"]),
            "effective_date": request.form["effective_date"],
            "action_type":  request.form["action_type"],
        }
        promote_employee(emp_id, updates)
        flash(f"✅ {updates['action_type']} processed successfully (PA40 — Personnel Action).", "success")
        return redirect(url_for("employee_detail", emp_id=emp_id))
    return render_template("promote.html", emp=emp)

@app.route("/separate/<emp_id>", methods=["GET", "POST"])
def separate(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        flash("Employee not found.", "danger")
        return redirect(url_for("employee_list"))
    if request.method == "POST":
        reason          = request.form["reason"]
        last_working_day = request.form["last_working_day"]
        terminate_employee(emp_id, reason, last_working_day)
        flash(f"✅ Employee separation recorded. Status: Inactive.", "success")
        return redirect(url_for("employee_detail", emp_id=emp_id))
    return render_template("separate.html", emp=emp)

@app.route("/api/employee/<emp_id>")
def api_employee(emp_id):
    emp = get_employee(emp_id)
    return jsonify(emp or {})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
