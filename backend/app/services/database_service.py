from app.models.database import SQLiteDatabase


def create_tables(db: SQLiteDatabase):
    # Create tables
    db.execute_query('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        position TEXT,
        salary REAL,
        hire_date DATE
    )
    ''')

    db.execute_query('''
    CREATE TABLE departments (
        id INTEGER PRIMARY KEY,
        name TEXT,
        budget REAL
    )
    ''')

    db.execute_query('''
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY,
        name TEXT,
        start_date DATE,
        end_date DATE,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    ''')

    db.execute_query('''
    CREATE TABLE employee_projects (
        employee_id INTEGER,
        project_id INTEGER,
        role TEXT,
        PRIMARY KEY (employee_id, project_id),
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')


def insert_dummy_data(db: SQLiteDatabase):
    departments = [
        (1, 'Engineering', 1000000),
        (2, 'Marketing', 500000),
        (3, 'HR', 300000),
        (4, 'Sales', 750000)
    ]

    employees = [
        (1, 'John Doe', 'Engineering', 'Senior Developer', 95000, '2020-01-15'),
        (2, 'Jane Smith', 'Marketing', 'Marketing Manager', 85000, '2019-05-20'),
        (3, 'Bob Johnson', 'Engineering', 'Developer', 80000, '2021-03-10'),
        (4, 'Alice Williams', 'HR', 'HR Specialist', 70000, '2018-11-01'),
        (5, 'Charlie Brown', 'Marketing', 'Content Writer', 65000, '2022-02-15'),
        (6, 'Eva Davis', 'Sales', 'Sales Representative', 75000, '2020-09-01'),
        (7, 'Frank Miller', 'Engineering', 'QA Engineer', 85000, '2019-07-22'),
        (8, 'Grace Lee', 'Marketing', 'Graphic Designer', 70000, '2021-11-30')
    ]

    projects = [
        (1, 'Website Redesign', '2024-01-01', '2024-06-30', 1),
        (2, 'Mobile App Development', '2024-03-15', '2024-12-31', 1),
        (3, 'Data Analytics Platform', '2024-02-01', '2024-11-30', 1),
        (4, 'Summer Marketing Campaign', '2024-05-01', '2024-08-31', 2),
        (5, 'Employee Engagement Program', '2024-04-01', '2024-09-30', 3)
    ]

    employee_projects = [
        (1, 1, 'Project Lead'),
        (1, 2, 'Senior Developer'),
        (2, 4, 'Campaign Manager'),
        (3, 2, 'Developer'),
        (3, 3, 'Developer'),
        (4, 5, 'Program Coordinator'),
        (5, 4, 'Content Creator'),
        (6, 4, 'Sales Liaison'),
        (7, 1, 'QA Lead'),
        (7, 2, 'QA Engineer'),
        (8, 4, 'Design Lead')
    ]

    for dept in departments:
        db.execute_query('INSERT INTO departments VALUES (?,?,?)', dept)

    for emp in employees:
        db.execute_query('INSERT INTO employees VALUES (?,?,?,?,?,?)', emp)

    for proj in projects:
        db.execute_query('INSERT INTO projects VALUES (?,?,?,?,?)', proj)

    for emp_proj in employee_projects:
        db.execute_query('INSERT INTO employee_projects VALUES (?,?,?)', emp_proj)


def create_examples_database():
    sqlite_db = SQLiteDatabase(':memory:')
    create_tables(sqlite_db)
    insert_dummy_data(sqlite_db)
    return sqlite_db
