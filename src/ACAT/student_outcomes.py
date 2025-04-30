import os
import pandas as pd
 
def extract_student_outcomes_for_all_courses(student_id: int = 11) -> dict:
    courses_outcomes = {}
 
    # Dynamically get the base directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assessment_results_dir = os.path.join(base_dir, "assessment_results")
 
    if not os.path.exists(assessment_results_dir):
        print(f"❌ Folder {assessment_results_dir} does not exist.")
        return courses_outcomes
 
    for file_name in os.listdir(assessment_results_dir):
        if file_name.endswith("_outcomes.xlsx"):
            course_code = file_name.split("_")[0]
            file_path = os.path.join(assessment_results_dir, file_name)
 
            try:
                df = pd.read_excel(file_path)
                student_row = df[df.iloc[:, 0] == student_id]
 
                if not student_row.empty:
                    outcome_dict = student_row.iloc[0, 1:].to_dict()
                    courses_outcomes[course_code] = outcome_dict
                else:
                    print(f"No data found for student {student_id} in course {course_code}")
 
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
 
    return courses_outcomes
 
# Optional: Test
if __name__ == "__main__":
    student_outcomes = extract_student_outcomes_for_all_courses()
    print(student_outcomes)