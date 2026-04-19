"""
hr_processes.py
Business logic for SAP HR H2R lifecycle processes.
Simulates SAP infotypes and personnel actions.
"""

import json, uuid, os
from datetime import datetime, date

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "employees.json")
PAYROLL_FILE = os.path.join(os.path.dirname(__file__), "data", "payroll.json")

# ─────────────────────────────────────────────────────────
# UTILITY — load / save JSON data store
# ─────────────────────────────────────────────────────────
def _load(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def _save(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)

def _load_list(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def _save_list(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)

# ─────────────────────────────────────────────────────────
# GENERATE EMPLOYEE ID (SAP-style: EMP + 6 digits)
# ─────────────────────────────────────────────────────────
def _generate_emp_id(db):
    existing = [int(k.replace("EMP", "")) for k in db.keys() if k.startswith("EMP")]
    next_num = max(existing, default=100000) + 1
    return f"EMP{next_num}"

# ─────────────────────────────────────────────────────────
# PA40 — HIRE EMPLOYEE
# ─────────────────────────────────────────────────────────
def hire_employee(data: dict) -> str:
    """
    Creates a new employee record.
    SAP Equivalent: PA40 (Personnel Actions) → Action Type: Hiring
    Infotypes created: IT0000 (Actions), IT0001 (Org Assignment),
                       IT0002 (Personal Data), IT0008 (Basic Pay)
    """
    db = _load(DATA_FILE)
    emp_id = _generate_emp_id(db)

    db[emp_id] = {
        "emp_id":          emp_id,
        "first_name":      data["first_name"],
        "last_name":       data["last_name"],
        "full_name":       f"{data['first_name']} {data['last_name']}",
        "email":           data["email"],
        "phone":           data["phone"],
        "gender":          data["gender"],
        "dob":             data["dob"],
        # IT0001 — Organisational Assignment
        "designation":     data["designation"],
        "department":      data["department"],
        "cost_center":     data["cost_center"],
        "employment_type": data["employment_type"],
        "location":        data["location"],
        "manager":         data.get("manager", ""),
        # IT0008 — Basic Pay
        "basic_salary":    data["basic_salary"],
        "hra_pct":         data.get("hra_pct", 0.40),
        "ta_fixed":        data.get("ta_fixed", 1600),
        # Dates & Status
        "hire_date":       data["hire_date"],
        "status":          "Active",
        "created_at":      str(datetime.now()),
        # Sub-records
        "leaves":          [],
        "trainings":       [],
        "actions_log":     [
            {
                "date":   data["hire_date"],
                "action": "Hiring",
                "detail": f"Joined as {data['designation']} in {data['department']}"
            }
        ]
    }
    _save(DATA_FILE, db)
    return emp_id

# ─────────────────────────────────────────────────────────
# READ
# ─────────────────────────────────────────────────────────
def get_all_employees() -> list:
    db = _load(DATA_FILE)
    return list(db.values())

def get_employee(emp_id: str) -> dict:
    db = _load(DATA_FILE)
    return db.get(emp_id)

# ─────────────────────────────────────────────────────────
# PA30 — UPDATE EMPLOYEE MASTER DATA
# ─────────────────────────────────────────────────────────
def update_employee(emp_id: str, updates: dict):
    """
    SAP Equivalent: PA30 (Maintain HR Master Data)
    Updates personal, organisational, or pay data.
    """
    db = _load(DATA_FILE)
    if emp_id not in db:
        return False
    db[emp_id].update(updates)
    db[emp_id]["updated_at"] = str(datetime.now())
    _save(DATA_FILE, db)
    return True

# ─────────────────────────────────────────────────────────
# PAYROLL PROCESSING
# ─────────────────────────────────────────────────────────
def process_payroll(emp_id: str, month: int, year: int) -> dict:
    """
    SAP Equivalent: PC00_M99_CALC (Payroll Driver)
    Calculates gross, deductions, and net pay.
    """
    db = _load(DATA_FILE)
    if emp_id not in db:
        return None
    emp = db[emp_id]

    basic      = emp["basic_salary"]
    hra        = basic * emp.get("hra_pct", 0.40)
    ta         = emp.get("ta_fixed", 1600)
    special_all= basic * 0.10
    gross      = basic + hra + ta + special_all

    # Statutory deductions
    pf         = basic * 0.12        # 12% of basic
    esi        = gross * 0.0075 if gross <= 21000 else 0  # ESI if gross ≤ 21k
    pt         = 200                  # Professional Tax (flat)
    tds        = max(0, (gross * 12 - 250000) / 12 * 0.05)  # simplified TDS

    total_deductions = pf + esi + pt + tds
    net_pay    = gross - total_deductions

    month_name = datetime(year, month, 1).strftime("%B")
    payslip = {
        "payslip_id":   str(uuid.uuid4())[:8].upper(),
        "emp_id":       emp_id,
        "emp_name":     emp["full_name"],
        "designation":  emp["designation"],
        "department":   emp["department"],
        "month":        month_name,
        "year":         year,
        "period":       f"{month_name} {year}",
        # Earnings
        "basic":        round(basic, 2),
        "hra":          round(hra, 2),
        "ta":           round(ta, 2),
        "special_all":  round(special_all, 2),
        "gross":        round(gross, 2),
        # Deductions
        "pf":           round(pf, 2),
        "esi":          round(esi, 2),
        "pt":           round(pt, 2),
        "tds":          round(tds, 2),
        "total_deductions": round(total_deductions, 2),
        # Net
        "net_pay":      round(net_pay, 2),
        "processed_on": str(datetime.now().date()),
    }

    # Save payroll history
    history = _load_list(PAYROLL_FILE)
    history.append(payslip)
    _save_list(PAYROLL_FILE, history)

    return payslip

def get_payroll_history(emp_id: str) -> list:
    history = _load_list(PAYROLL_FILE)
    return [p for p in history if p["emp_id"] == emp_id]

# ─────────────────────────────────────────────────────────
# TIME MANAGEMENT — LEAVE (IT2001)
# ─────────────────────────────────────────────────────────
def record_leave(emp_id: str, leave_type: str, start: str, end: str, reason: str):
    """
    SAP Equivalent: IT2001 (Absences)
    Records employee leave/absence.
    """
    db = _load(DATA_FILE)
    if emp_id not in db:
        return False
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt   = datetime.strptime(end, "%Y-%m-%d")
    days     = (end_dt - start_dt).days + 1

    leave = {
        "leave_id":   str(uuid.uuid4())[:8].upper(),
        "leave_type": leave_type,
        "start_date": start,
        "end_date":   end,
        "days":       days,
        "reason":     reason,
        "applied_on": str(date.today()),
        "status":     "Approved"
    }
    db[emp_id]["leaves"].append(leave)
    _save(DATA_FILE, db)
    return True

# ─────────────────────────────────────────────────────────
# TRAINING & DEVELOPMENT (LSO)
# ─────────────────────────────────────────────────────────
def add_training(emp_id: str, course: str, provider: str,
                  start: str, end: str, status: str):
    """
    SAP Equivalent: LSO (Learning Solution) / Training & Events
    Records employee training programs.
    """
    db = _load(DATA_FILE)
    if emp_id not in db:
        return False
    training = {
        "training_id": str(uuid.uuid4())[:8].upper(),
        "course":      course,
        "provider":    provider,
        "start_date":  start,
        "end_date":    end,
        "status":      status,
        "added_on":    str(date.today()),
    }
    db[emp_id]["trainings"].append(training)
    _save(DATA_FILE, db)
    return True

# ─────────────────────────────────────────────────────────
# PROMOTION / TRANSFER (PA40 — Promotion / Transfer Action)
# ─────────────────────────────────────────────────────────
def promote_employee(emp_id: str, updates: dict):
    """
    SAP Equivalent: PA40 → Action Type: Promotion / Transfer
    Updates org assignment and pay grade.
    """
    db = _load(DATA_FILE)
    if emp_id not in db:
        return False
    old_desig = db[emp_id]["designation"]
    old_dept  = db[emp_id]["department"]

    db[emp_id]["designation"]  = updates["designation"]
    db[emp_id]["department"]   = updates["department"]
    db[emp_id]["basic_salary"] = updates["basic_salary"]
    db[emp_id]["updated_at"]   = str(datetime.now())
    db[emp_id]["actions_log"].append({
        "date":   updates["effective_date"],
        "action": updates["action_type"],
        "detail": f"From: {old_desig} ({old_dept}) → To: {updates['designation']} ({updates['department']})"
    })
    _save(DATA_FILE, db)
    return True

# ─────────────────────────────────────────────────────────
# SEPARATION / RETIREMENT (PA40 — Leaving Action)
# ─────────────────────────────────────────────────────────
def terminate_employee(emp_id: str, reason: str, last_working_day: str):
    """
    SAP Equivalent: PA40 → Action Type: Leaving
    Infotype: IT0000 (Actions) — sets employment status to 0 (Withdrawn)
    """
    db = _load(DATA_FILE)
    if emp_id not in db:
        return False
    db[emp_id]["status"]           = "Inactive"
    db[emp_id]["separation_reason"] = reason
    db[emp_id]["last_working_day"]  = last_working_day
    db[emp_id]["separation_date"]   = str(date.today())
    db[emp_id]["actions_log"].append({
        "date":   last_working_day,
        "action": "Separation",
        "detail": f"Reason: {reason}. Last Working Day: {last_working_day}"
    })
    _save(DATA_FILE, db)
    return True

# ─────────────────────────────────────────────────────────
# DASHBOARD STATISTICS
# ─────────────────────────────────────────────────────────
def get_dashboard_stats() -> dict:
    employees = get_all_employees()
    active    = [e for e in employees if e.get("status") == "Active"]
    inactive  = [e for e in employees if e.get("status") != "Active"]
    dept_dist = {}
    for e in active:
        d = e.get("department", "Unknown")
        dept_dist[d] = dept_dist.get(d, 0) + 1

    total_payroll = sum(e.get("basic_salary", 0) * 1.6 for e in active)

    return {
        "total_employees": len(employees),
        "active":          len(active),
        "inactive":        len(inactive),
        "departments":     len(dept_dist),
        "total_payroll":   round(total_payroll, 2),
        "dept_distribution": dept_dist,
    }
