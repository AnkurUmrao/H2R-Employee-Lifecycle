"""
seed_data.py
Run this once to populate the system with sample employees for demo purposes.
Usage: python seed_data.py
"""
from hr_processes import hire_employee, process_payroll, record_leave, add_training

sample_employees = [
    {
        "first_name": "Arjun", "last_name": "Sharma",
        "email": "arjun.sharma@techcorp.in", "phone": "9876543210",
        "gender": "Male", "dob": "1990-05-14",
        "designation": "Senior Software Engineer", "department": "IT",
        "cost_center": "CC-IT-001", "employment_type": "Permanent",
        "hire_date": "2021-03-01", "basic_salary": 85000,
        "location": "Bengaluru", "manager": "",
    },
    {
        "first_name": "Priya", "last_name": "Menon",
        "email": "priya.menon@techcorp.in", "phone": "9823456781",
        "gender": "Female", "dob": "1993-08-22",
        "designation": "HR Manager", "department": "Human Resources",
        "cost_center": "CC-HR-001", "employment_type": "Permanent",
        "hire_date": "2020-07-15", "basic_salary": 72000,
        "location": "Mumbai", "manager": "",
    },
    {
        "first_name": "Rahul", "last_name": "Verma",
        "email": "rahul.verma@techcorp.in", "phone": "9911223344",
        "gender": "Male", "dob": "1988-11-03",
        "designation": "Finance Analyst", "department": "Finance",
        "cost_center": "CC-FIN-001", "employment_type": "Permanent",
        "hire_date": "2019-01-10", "basic_salary": 68000,
        "location": "Delhi", "manager": "",
    },
    {
        "first_name": "Sneha", "last_name": "Patel",
        "email": "sneha.patel@techcorp.in", "phone": "9745612380",
        "gender": "Female", "dob": "1995-02-17",
        "designation": "Marketing Executive", "department": "Marketing",
        "cost_center": "CC-MKT-001", "employment_type": "Contract",
        "hire_date": "2023-06-01", "basic_salary": 45000,
        "location": "Ahmedabad", "manager": "",
    },
    {
        "first_name": "Vikram", "last_name": "Nair",
        "email": "vikram.nair@techcorp.in", "phone": "9988776655",
        "gender": "Male", "dob": "1985-09-29",
        "designation": "Operations Manager", "department": "Operations",
        "cost_center": "CC-OPS-001", "employment_type": "Permanent",
        "hire_date": "2018-04-20", "basic_salary": 92000,
        "location": "Pune", "manager": "",
    },
]

if __name__ == "__main__":
    print("Seeding employee data...")
    emp_ids = []
    for emp in sample_employees:
        eid = hire_employee(emp)
        emp_ids.append(eid)
        print(f"  Created: {eid} — {emp['first_name']} {emp['last_name']}")

    # Process some payroll
    print("\nProcessing sample payroll...")
    for eid in emp_ids[:3]:
        p = process_payroll(eid, 3, 2026)
        print(f"  Payroll: {eid} → ₹{p['net_pay']:,.2f} net")

    # Add some leaves
    print("\nAdding leave records...")
    record_leave(emp_ids[0], "Annual Leave", "2026-02-10", "2026-02-14", "Family vacation")
    record_leave(emp_ids[1], "Sick Leave",   "2026-01-20", "2026-01-22", "Fever")

    # Add training
    print("\nAdding training records...")
    add_training(emp_ids[0], "SAP ABAP Fundamentals", "SAP SE", "2026-01-05", "2026-01-07", "Completed")
    add_training(emp_ids[2], "Advanced Excel & SAP FI", "NIIT", "2026-02-01", "2026-02-03", "Completed")

    print("\n✅ Seed data loaded successfully! Run 'python app.py' to start.")
