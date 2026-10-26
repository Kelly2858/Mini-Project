# Project Documentation

## Student Performance Analytics System

---

## 1. Project Title

**Student Performance Analytics System**

- **Course**: Python with AI – EWB Courses  
- **Submission Deadline**: 15 October 2026

---

## 2. Objective

The goal of this project is to build a Python-based analytics system that reads a student dataset, processes it programmatically, and generates a comprehensive performance report. The project demonstrates how real-world data analysis tasks can be solved using Python fundamentals — functions, loops, and conditions — alongside powerful libraries like **NumPy** (for numerical computation) and **Pandas** (for structured data handling).

**Problem it solves**: Manually reviewing student marks across multiple subjects is tedious and error-prone. This system automates the process, instantly producing totals, averages, grades, pass/fail results, subject rankings, and department-level insights.

---

## 3. Technologies Used

| Technology | Purpose                                                         |
|------------|-----------------------------------------------------------------|
| Python 3.x | Core programming language                                       |
| NumPy      | Array-based numerical calculations (mean, max, min, std, sum)  |
| Pandas     | CSV loading, DataFrame operations, filtering, sorting           |
| os module  | File path management                                            |

---

## 4. Dataset Description

**File**: `students.csv`  
**Records**: 20 students  
**Columns**: 9

| Column       | Type    | Description                                |
|--------------|---------|--------------------------------------------|
| Student_ID   | String  | Unique ID for each student (S001 – S020)   |
| Name         | String  | Full name of the student                   |
| Department   | String  | Academic department                        |
| Math         | Integer | Marks in Mathematics (0 – 100)             |
| Science      | Integer | Marks in Science (0 – 100)                 |
| English      | Integer | Marks in English (0 – 100)                 |
| Computer     | Integer | Marks in Computer Science (0 – 100)        |
| History      | Integer | Marks in History (0 – 100)                 |
| Attendance   | Integer | Attendance percentage (0 – 100)            |

The dataset covers 4 departments: **Computer Science, Electronics, Mechanical, Civil** with a realistic spread of marks — including strong performers, average students, and a few failing cases — to make the analytics meaningful.

---

## 5. Implementation

### Step 1 – Prepare the Dataset

Created `students.csv` manually with 20 diverse student records. Marks are spread across all ranges (38 – 99) to ensure all grade categories and pass/fail conditions are represented. Attendance values range from 55% to 99%.

### Step 2 – Read the Data (`main.py → load_data()`)

```python
df = pd.read_csv(filepath)
```

The `load_data()` function:
- Checks if the file exists using `os.path.exists()`
- Uses `pd.read_csv()` to load the dataset into a Pandas DataFrame
- Validates that all required columns are present
- Reports the number of records and columns loaded

### Step 3 – Process the Data (`functions.py → process_dataframe()`)

The `process_dataframe()` function adds four computed columns to the DataFrame:

#### Total Marks — `calculate_total(row)`
Uses a **loop** to sum marks across all 5 subjects:
```python
for subject in SUBJECTS:
    total += row[subject]
```

#### Average Marks — `calculate_average(row)`
Uses **NumPy** `np.mean()` on a NumPy array:
```python
marks_array = np.array([row[subject] for subject in SUBJECTS])
return round(float(np.mean(marks_array)), 2)
```

#### Grade Assignment — `assign_grade(average)`
Uses a predefined grading scale and a loop with conditions:
```python
GRADE_SCALE = [(90,"A+"), (80,"A"), (70,"B"), (60,"C"), (50,"D"), (0,"F")]
for threshold, grade in GRADE_SCALE:
    if average >= threshold:
        return grade
```

#### Pass / Fail — `determine_pass_fail(row)`
Two conditions must be met:
1. All subject marks ≥ 40 (checked via a loop)
2. Attendance ≥ 75%

### Step 4 – Perform Analysis

The following analysis functions are implemented in `functions.py`:

| Function                    | What it computes                                          |
|-----------------------------|-----------------------------------------------------------|
| `get_class_summary(df)`     | Highest, lowest, class average; pass/fail count & rate   |
| `get_subject_analysis(df)`  | Per-subject mean, max, min, std deviation (via NumPy)    |
| `get_top_performers(df, n)` | Top-N students by average using `df.nlargest()`          |
| `get_department_analysis(df)`| Per-department stats and pass rates                      |
| `get_grade_distribution(df)`| Count of students per grade letter                       |

All numerical statistics use **NumPy arrays** (`np.mean`, `np.max`, `np.min`, `np.std`, `np.sum`, `np.argmax`) to ensure efficient computation.

### Step 5 – Final Output (`main.py`)

The `main()` function orchestrates the full analysis in 11 sections:

1. Dataset loading confirmation
2. Raw data preview
3. Processing log
4. Full student report (all columns)
5. Class summary statistics
6. Pass / Fail breakdown
7. Grade distribution with ASCII bar chart
8. Subject-wise performance analysis
9. Top 5 performers ranking
10. Department-wise analysis
11. Practical insights (8 key questions answered)

---

## 6. Key Features

- ✅ CSV dataset with 20 realistic student records
- ✅ Pandas DataFrame for structured data handling
- ✅ NumPy for all numerical computations
- ✅ Reusable functions organized in `functions.py`
- ✅ Loops used for subject iteration and grade assignment
- ✅ Total and average marks per student
- ✅ Letter grade assignment (A+ to F)
- ✅ Pass/fail determination with dual conditions
- ✅ Class-level statistics (highest, lowest, class average)
- ✅ Subject-wise analysis (mean, max, min, std)
- ✅ Department-wise performance breakdown
- ✅ Top 5 performers ranking
- ✅ Grade distribution with visual bar chart
- ✅ 8 practical insight questions answered programmatically

---

## 7. Output / Screenshots

The program produces formatted terminal output organized into sections, for example:

```
========================================================================
  CLASS PERFORMANCE SUMMARY
========================================================================
  Total Students      : 20
  Highest Average     : 95.8
  Lowest Average      : 42.0
  Class Average       : 73.4
  Students Passed     : 16
  Students Failed     : 4
  Pass Percentage     : 80.0%
```

```
========================================================================
  GRADE DISTRIBUTION
========================================================================
  Grade    Count    Bar
  ------   -----    ------------------------------
  A+       3        ███
  A        5        █████
  B        4        ████
  C        4        ████
  D        2        ██
  F        2        ██
```

---

## 8. Final Outcome

The project successfully:
- Loaded and validated a 20-record student dataset using Pandas
- Computed all performance metrics (total, average, grade, pass/fail)
- Performed multi-dimensional analysis (class, subject, department, individual)
- Answered 8 practical analytical questions from the data
- Produced clear, readable terminal output that requires no code inspection to understand

The system is modular, with `functions.py` containing all logic and `main.py` handling only orchestration and display — making it easy to extend or reuse individual components.

---

## 9. Challenges & Learning

| Challenge | How it was resolved | What was learned |
|-----------|---------------------|------------------|
| Combining `apply()` with custom functions | Used `df.apply(func, axis=1)` to pass each row to a function | How Pandas applies row-wise operations |
| Using NumPy inside Pandas workflows | Converted DataFrame columns to NumPy arrays with `np.array()` | Integration between Pandas and NumPy |
| Multi-condition pass/fail logic | Used a loop for subject checks, then a separate attendance check | Breaking complex conditions into readable steps |
| Formatting terminal output neatly | Used f-strings with fixed-width formatting | Python string formatting best practices |
| Department grouping without `groupby` | Iterated over `unique()` department values manually | Manual aggregation using loops and NumPy |

---

## 10. GitHub Repository

> https://github.com/Kelly2858/Mini-Project
