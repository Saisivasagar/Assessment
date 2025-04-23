import os
import pandas as pd

# Function to extract outcomes for student 11 across all courses
def extract_student_outcomes_for_all_courses(base_dir: str = "/workspaces/scthumma-assessment/src/ACAT", student_id: int = 11) -> dict:
    courses_outcomes = {}

    # Absolute path to the assessment_results directory
    assessment_results_dir = os.path.join(base_dir, "assessment_results")
    
    # Check if the folder exists
    if not os.path.exists(assessment_results_dir):
        print(f"❌ Folder {assessment_results_dir} does not exist.")
        return courses_outcomes

    # Loop through all files in the assessment_results directory
    for file_name in os.listdir(assessment_results_dir):
        if file_name.endswith("_outcomes.xlsx"):  # Check for outcome files
            course_code = file_name.split("_")[0]  # Extract course code (e.g., "COMP-101")
            file_path = os.path.join(assessment_results_dir, file_name)

            try:
                # Read the Excel file
                df = pd.read_excel(file_path)

                # Filter for Student ID 11 (assuming Student ID is in the first column)
                student_row = df[df.iloc[:, 0] == student_id]

                if not student_row.empty:
                    # Extract the outcome-Likert scores into a dictionary (skip the first column)
                    outcome_dict = student_row.iloc[0, 1:].to_dict()  # Outcomes start from the second column
                    courses_outcomes[course_code] = outcome_dict
                else:
                    print(f"No data found for student {student_id} in course {course_code}")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    return courses_outcomes

# Example usage: Call the function to extract outcomes for student 11 across all courses
student_outcomes = extract_student_outcomes_for_all_courses()
print(student_outcomes)
