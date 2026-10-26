# Student Performance Analytics System

## Project Overview

A Python-based data analysis project that reads student records from a CSV file, processes and analyzes the data using **NumPy** and **Pandas**, and produces a comprehensive performance report including marks summaries, averages, grades, pass/fail status, subject-wise analysis, department-wise performance, and top performers.

---

## Project Structure

```
project1/
├── main.py            # Main program – runs all analysis and displays output
├── functions.py       # Reusable functions for calculations and processing
├── students.csv       # Student dataset (20 records)
├── README.md          # This file
└── Project_Documentation.md   # Full project documentation
```

---

## Dataset

The dataset (`students.csv`) contains **20 student records** with the following fields:

| Column       | Description                           |
|--------------|---------------------------------------|
| Student_ID   | Unique identifier (S001 – S020)       |
| Name         | Student full name                     |
| Department   | Academic department                   |
| Math         | Marks in Mathematics (out of 100)     |
| Science      | Marks in Science (out of 100)         |
| English      | Marks in English (out of 100)         |
| Computer     | Marks in Computer Science (out of 100)|
| History      | Marks in History (out of 100)         |
| Attendance   | Attendance percentage                 |

---

## How to Run

### Prerequisites

Make sure you have Python 3.8+ and the required libraries installed:

```bash
pip install numpy pandas
```

### Run the Project

```bash
python main.py
```

The program will display a full analytical report in the terminal.

---

## Features

- Load student data from CSV using **Pandas**
- Calculate total and average marks per student using **NumPy**
- Assign letter grades based on a defined grading scale
- Determine pass/fail based on subject marks and attendance
- Class-level summary statistics (highest, lowest, class average)
- Subject-wise performance analysis (mean, max, min, std deviation)
- Department-wise performance breakdown
- Top 5 performing students ranking
- Grade distribution with visual bar output
- Practical analytical insights (best student, best subject, etc.)

---

## Grading Scale

| Average Range | Grade |
|---------------|-------|
| 90 – 100      | A+    |
| 80 – 89       | A     |
| 70 – 79       | B     |
| 60 – 69       | C     |
| 50 – 59       | D     |
| Below 50      | F     |

## Pass Conditions

A student **PASSES** if:
1. Marks in **every subject** ≥ 40
2. **Attendance** ≥ 75%

---

## Technologies Used

- **Python 3.x**
- **NumPy** – Numerical calculations (mean, max, min, std, array operations)
- **Pandas** – DataFrame creation, loading CSV, filtering, grouping
- **os** – File path handling

---

## Author

Student – Python with AI | EWB Courses  
Submission Deadline: 15 October 2026  
GitHub: https://github.com/Kelly2858/Mini-Project
