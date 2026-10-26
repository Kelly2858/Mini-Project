# =============================================================================
# functions.py
# Student Performance Analytics System
# Reusable functions for data processing and analysis
# =============================================================================

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUBJECTS = ["Math", "Science", "English", "Computer", "History"]
PASS_MARK = 40          # Minimum marks required per subject to pass
PASS_ATTENDANCE = 75    # Minimum attendance % required

GRADE_SCALE = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),
]


# ---------------------------------------------------------------------------
# Calculation functions
# ---------------------------------------------------------------------------

def calculate_total(row):
    """Return the sum of all subject marks for a given student row."""
    total = 0
    for subject in SUBJECTS:
        total += row[subject]
    return total


def calculate_average(row):
    """Return the average marks across all subjects (rounded to 2 decimal places)."""
    marks = [row[subject] for subject in SUBJECTS]
    marks_array = np.array(marks)
    return round(float(np.mean(marks_array)), 2)


def assign_grade(average):
    """
    Assign a letter grade based on the student's average marks.

    Grading Scale:
        90 – 100  →  A+
        80 – 89   →  A
        70 – 79   →  B
        60 – 69   →  C
        50 – 59   →  D
        Below 50  →  F
    """
    for threshold, grade in GRADE_SCALE:
        if average >= threshold:
            return grade
    return "F"


def determine_pass_fail(row):
    """
    Determine whether a student passes or fails.

    Conditions for PASS:
        1. Marks in every subject must be >= PASS_MARK (40).
        2. Attendance must be >= PASS_ATTENDANCE (75%).

    Returns 'Pass' or 'Fail'.
    """
    # Check each subject separately using a loop
    for subject in SUBJECTS:
        if row[subject] < PASS_MARK:
            return "Fail"

    # Check attendance requirement
    if row["Attendance"] < PASS_ATTENDANCE:
        return "Fail"

    return "Pass"


# ---------------------------------------------------------------------------
# DataFrame processing function
# ---------------------------------------------------------------------------

def process_dataframe(df):
    """
    Add computed columns to the DataFrame:
        - Total      : Sum of all subject marks
        - Average    : Mean of all subject marks
        - Grade      : Letter grade based on average
        - Result     : Pass / Fail status

    Returns the enriched DataFrame.
    """
    df = df.copy()

    df["Total"]   = df.apply(calculate_total, axis=1)
    df["Average"] = df.apply(calculate_average, axis=1)
    df["Grade"]   = df["Average"].apply(assign_grade)
    df["Result"]  = df.apply(determine_pass_fail, axis=1)

    return df


# ---------------------------------------------------------------------------
# Summary statistics functions
# ---------------------------------------------------------------------------

def get_class_summary(df):
    """
    Return a dictionary of overall class statistics using NumPy:
        - highest_average  : Best average in the class
        - lowest_average   : Lowest average in the class
        - class_average    : Mean of all student averages
        - total_students   : Number of students
        - pass_count       : Number of students who passed
        - fail_count       : Number of students who failed
        - pass_percentage  : Percentage of students who passed
    """
    averages = np.array(df["Average"].tolist())

    pass_count = int((df["Result"] == "Pass").sum())
    fail_count = int((df["Result"] == "Fail").sum())
    total      = len(df)

    return {
        "highest_average": round(float(np.max(averages)), 2),
        "lowest_average":  round(float(np.min(averages)), 2),
        "class_average":   round(float(np.mean(averages)), 2),
        "total_students":  total,
        "pass_count":      pass_count,
        "fail_count":      fail_count,
        "pass_percentage": round((pass_count / total) * 100, 2),
    }


def get_subject_analysis(df):
    """
    Return a Pandas DataFrame with per-subject statistics:
        - Mean, Max, Min, Std deviation (via NumPy)
        - Number of students who scored below PASS_MARK in that subject

    Sorted by Mean in descending order.
    """
    rows = []
    for subject in SUBJECTS:
        marks = np.array(df[subject].tolist())
        rows.append({
            "Subject":          subject,
            "Mean":             round(float(np.mean(marks)), 2),
            "Highest":          int(np.max(marks)),
            "Lowest":           int(np.min(marks)),
            "Std Dev":          round(float(np.std(marks)), 2),
            "Below Pass Mark":  int(np.sum(marks < PASS_MARK)),
        })

    subject_df = pd.DataFrame(rows)
    return subject_df.sort_values("Mean", ascending=False).reset_index(drop=True)


def get_top_performers(df, n=5):
    """
    Return the top-N performing students sorted by Average marks (descending).
    Default is top 5.
    """
    top = df.nlargest(n, "Average")[
        ["Student_ID", "Name", "Department", "Average", "Grade", "Result"]
    ].reset_index(drop=True)
    top.index = top.index + 1   # Start ranking from 1
    return top


def get_department_analysis(df):
    """
    Return a Pandas DataFrame with per-department performance summary:
        - Number of students
        - Average marks (Mean)
        - Highest and lowest averages in the department
        - Pass count and pass rate
    """
    rows = []
    departments = df["Department"].unique()

    for dept in sorted(departments):
        dept_df = df[df["Department"] == dept]
        averages = np.array(dept_df["Average"].tolist())
        pass_count = int((dept_df["Result"] == "Pass").sum())

        rows.append({
            "Department":      dept,
            "Students":        len(dept_df),
            "Avg Marks":       round(float(np.mean(averages)), 2),
            "Highest Avg":     round(float(np.max(averages)), 2),
            "Lowest Avg":      round(float(np.min(averages)), 2),
            "Pass Count":      pass_count,
            "Pass Rate (%)":   round((pass_count / len(dept_df)) * 100, 2),
        })

    return pd.DataFrame(rows)


def get_grade_distribution(df):
    """
    Return a dictionary mapping each grade letter to the count of students
    who received it.
    """
    all_grades = ["A+", "A", "B", "C", "D", "F"]
    grade_counts = df["Grade"].value_counts()
    distribution = {}
    for grade in all_grades:
        distribution[grade] = int(grade_counts.get(grade, 0))
    return distribution


def find_student_by_id(df, student_id):
    """Look up a single student record by Student_ID. Returns a Series or None."""
    result = df[df["Student_ID"] == student_id]
    if result.empty:
        return None
    return result.iloc[0]
