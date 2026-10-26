# =============================================================================
# main.py
# Student Performance Analytics System
# Main program - loads data, processes it, and displays full analysis
# =============================================================================

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import os

from functions import (
    process_dataframe,
    get_class_summary,
    get_subject_analysis,
    get_top_performers,
    get_department_analysis,
    get_grade_distribution,
    SUBJECTS,
    PASS_MARK,
    PASS_ATTENDANCE,
)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

LINE  = "=" * 72
DLINE = "-" * 72


def section(title):
    """Print a formatted section header."""
    print(f"\n{LINE}")
    print(f"  {title}")
    print(LINE)


def subsection(title):
    """Print a lighter sub-section separator."""
    print(f"\n{DLINE}")
    print(f"  {title}")
    print(DLINE)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(filepath):
    """
    Load the CSV dataset into a Pandas DataFrame.
    Validates that the file exists and required columns are present.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    df = pd.read_csv(filepath)

    required_columns = ["Student_ID", "Name", "Department",
                        "Math", "Science", "English", "Computer", "History",
                        "Attendance"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    print(f"  Dataset loaded successfully  ->  {len(df)} records, "
          f"{len(df.columns)} columns")
    return df


# ---------------------------------------------------------------------------
# Output sections
# ---------------------------------------------------------------------------

def display_raw_data(df):
    """Show a preview of the raw dataset."""
    section("RAW DATASET PREVIEW  (first 5 rows)")
    print(df.head().to_string(index=False))
    print(f"\n  Total rows : {len(df)}")
    print(f"  Columns    : {list(df.columns)}")


def display_processed_data(df):
    """Show the full processed table with computed columns."""
    section("FULL STUDENT REPORT  (with Total, Average, Grade, Result)")
    cols = ["Student_ID", "Name", "Department",
            *SUBJECTS, "Attendance", "Total", "Average", "Grade", "Result"]
    print(df[cols].to_string(index=False))


def display_class_summary(summary):
    """Print overall class statistics."""
    section("CLASS PERFORMANCE SUMMARY")
    print(f"  Total Students      : {summary['total_students']}")
    print(f"  Highest Average     : {summary['highest_average']}")
    print(f"  Lowest Average      : {summary['lowest_average']}")
    print(f"  Class Average       : {summary['class_average']}")
    print(f"  Students Passed     : {summary['pass_count']}")
    print(f"  Students Failed     : {summary['fail_count']}")
    print(f"  Pass Percentage     : {summary['pass_percentage']}%")


def display_pass_fail(df):
    """Show the list of passed and failed students."""
    section("PASS / FAIL BREAKDOWN")

    passed = df[df["Result"] == "Pass"][["Student_ID", "Name", "Department", "Average", "Grade"]]
    failed = df[df["Result"] == "Fail"][["Student_ID", "Name", "Department", "Average", "Grade"]]

    subsection(f"PASSED STUDENTS  ({len(passed)})")
    if len(passed) > 0:
        print(passed.to_string(index=False))
    else:
        print("  None")

    subsection(f"FAILED STUDENTS  ({len(failed)})")
    if len(failed) > 0:
        print(failed.to_string(index=False))
    else:
        print("  None")


def display_grade_distribution(distribution):
    """Display a grade-wise breakdown with a simple bar chart."""
    section("GRADE DISTRIBUTION")

    print(f"  {'Grade':<8} {'Count':<8} {'Bar'}")
    print(f"  {'------':<8} {'-----':<8} {'------------------------------'}")

    for grade, count in distribution.items():
        bar = "#" * count
        print(f"  {grade:<8} {count:<8} {bar}")


def display_subject_analysis(subject_df):
    """Print subject-wise performance statistics."""
    section("SUBJECT-WISE PERFORMANCE ANALYSIS")
    print(subject_df.to_string(index=False))

    best_subject = subject_df.iloc[0]["Subject"]
    print(f"\n  [BEST] Best performing subject  : {best_subject} "
          f"(Mean = {subject_df.iloc[0]['Mean']})")
    print(f"  [LOW]  Most difficult subject   : {subject_df.iloc[-1]['Subject']} "
          f"(Mean = {subject_df.iloc[-1]['Mean']})")


def display_top_performers(top_df):
    """Display the top 5 students."""
    section("TOP 5 PERFORMING STUDENTS")
    print(top_df.to_string())


def display_department_analysis(dept_df):
    """Print department-wise performance summary."""
    section("DEPARTMENT-WISE PERFORMANCE")
    print(dept_df.to_string(index=False))

    # Find best department using NumPy argmax
    avg_marks = np.array(dept_df["Avg Marks"].tolist())
    best_idx  = int(np.argmax(avg_marks))
    print(f"\n  [BEST] Best performing department : "
          f"{dept_df.iloc[best_idx]['Department']} "
          f"(Avg = {dept_df.iloc[best_idx]['Avg Marks']})")


def display_practical_insights(df, summary):
    """Answer practical analytical questions from the dataset."""
    section("PRACTICAL INSIGHTS  (Key Questions Answered)")

    # Q1 - Highest average student
    top_student = df.loc[df["Average"].idxmax()]
    print(f"  Q1. Student with highest average  : {top_student['Name']} "
          f"({top_student['Average']})")

    # Q2 - Lowest average student
    low_student = df.loc[df["Average"].idxmin()]
    print(f"  Q2. Student with lowest average   : {low_student['Name']} "
          f"({low_student['Average']})")

    # Q3 - Overall class average
    print(f"  Q3. Overall class average         : {summary['class_average']}")

    # Q4 - How many passed?
    print(f"  Q4. Students who passed           : {summary['pass_count']} "
          f"out of {summary['total_students']}")

    # Q5 - Best subject (computed from NumPy means across all students)
    subject_means = {}
    for subject in SUBJECTS:
        marks = np.array(df[subject].tolist())
        subject_means[subject] = round(float(np.mean(marks)), 2)

    best_subject = max(subject_means, key=subject_means.get)
    print(f"  Q5. Subject with best class avg   : {best_subject} "
          f"(Mean = {subject_means[best_subject]})")

    # Q6 - Subject with lowest class average
    worst_subject = min(subject_means, key=subject_means.get)
    print(f"  Q6. Subject with lowest class avg : {worst_subject} "
          f"(Mean = {subject_means[worst_subject]})")

    # Q7 - Attendance analysis
    attendance = np.array(df["Attendance"].tolist())
    low_att_count = int(np.sum(attendance < PASS_ATTENDANCE))
    print(f"  Q7. Students with low attendance  : {low_att_count} "
          f"(below {PASS_ATTENDANCE}%)")

    # Q8 - Students with A+ grade (average >= 90)
    excellent = df[df["Average"] >= 90]
    print(f"  Q8. Students with A+ grade (>=90) : {len(excellent)}")
    for _, row in excellent.iterrows():
        print(f"       -> {row['Name']} ({row['Average']})")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    print()
    print(LINE)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("       Python with AI  |  EWB Courses")
    print(LINE)

    # -- Step 1: Load Data --------------------------------------------------
    section("STEP 1 - LOADING DATASET")
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")
    df_raw = load_data(dataset_path)

    # -- Step 2: Preview Raw Data -------------------------------------------
    display_raw_data(df_raw)

    # -- Step 3: Process Data -----------------------------------------------
    section("STEP 2 - PROCESSING DATA")
    print(f"  Calculating totals, averages, grades and pass/fail status...")
    print(f"  Pass condition : Each subject >= {PASS_MARK} marks  "
          f"AND  Attendance >= {PASS_ATTENDANCE}%")

    df = process_dataframe(df_raw)
    print(f"  Processing complete.")

    # -- Step 4: Display Full Report ----------------------------------------
    display_processed_data(df)

    # -- Step 5: Summary Statistics -----------------------------------------
    summary = get_class_summary(df)
    display_class_summary(summary)

    # -- Step 6: Pass / Fail Lists ------------------------------------------
    display_pass_fail(df)

    # -- Step 7: Grade Distribution -----------------------------------------
    distribution = get_grade_distribution(df)
    display_grade_distribution(distribution)

    # -- Step 8: Subject-wise Analysis --------------------------------------
    subject_df = get_subject_analysis(df)
    display_subject_analysis(subject_df)

    # -- Step 9: Top Performers ---------------------------------------------
    top_df = get_top_performers(df, n=5)
    display_top_performers(top_df)

    # -- Step 10: Department Analysis ---------------------------------------
    dept_df = get_department_analysis(df)
    display_department_analysis(dept_df)

    # -- Step 11: Practical Insights ----------------------------------------
    display_practical_insights(df, summary)

    # -- Done ---------------------------------------------------------------
    print(f"\n{LINE}")
    print("  Analysis complete. Thank you!")
    print(LINE)
    print()


if __name__ == "__main__":
    main()
