import os
import json
import re
import pandas as pd
from acat import ACAT

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)
    
def read_outcomes(outcomes_file):
    outcomes_df = pd.read_excel(outcomes_file)
    outcomes = outcomes_df.iloc[:, 0].dropna().tolist()  
    return outcomes


def read_assignments(assignments_file, outcomes):
    assignments_df = pd.read_excel(assignments_file)
    assignments = {}    
    for outcome in outcomes:
        # Locate the row matching the outcome in the first column
        row_matches = assignments_df[assignments_df.iloc[:, 0] == outcome]
        if not row_matches.empty:
            # Select all non-empty assignment names from columns after the first
            assignment_names = row_matches.iloc[0, 1:].dropna().tolist()
            assignments[outcome] = assignment_names    
    return assignments



def read_grades(grades_file, required_columns):
    grades_df = pd.read_excel(grades_file)
    # Remove the unique Canvas identifiers (numbers in parentheses) from column names
    cleaned_columns = {
        col: re.sub(r"\s*\(.*?\)", "", col).strip()
        for col in grades_df.columns
    }
    grades_df.rename(columns=cleaned_columns, inplace=True)
    relevant_columns = ['SIS User ID'] + [col for col in required_columns if col in grades_df.columns]
    grades_df = grades_df[relevant_columns].set_index('SIS User ID')
    return grades_df.to_dict(orient='index')

def main():
    config = load_config("acat_config.json")
    course_outcomes_results = {}

    for course in config['courses']:
        course_name = course['course_name']
        semester = course['semester']
        outcomes = read_outcomes(course['outcomes_file'])

        print("Processing course:\n", course_name)
        print("Outcomes:\n", outcomes)

        for section_data in course['sections']:
            section = section_data['section']
            assignments_mapping = read_assignments(section_data['assignments_file'], outcomes)
            final_outcomes = {
                outcome: assignments_mapping.get(outcome, [])
                for outcome in outcomes
            }

            print("Final Outcomes:\n", final_outcomes)

            # Extract the unique list of all required assignments for this section
            required_columns = set(assignment for criteria in final_outcomes.values() for assignment in criteria)

            student_data = read_grades(section_data['grades_file'], required_columns=required_columns)

            acat = ACAT(course_name, semester, section, final_outcomes, student_data)
            student_outcomes = acat.compute_course_outcomes()
            acat.summarize_course_outcomes(student_outcomes)

            excel_output = os.path.join(
                config['output']['excel_folder'],
                f"{course_name}_{semester}_{section}_outcomes.xlsx"
            )

            db_output = os.path.join(
                config['output']['database_folder'],
                f"{course_name}_{semester}_{section}_outcomes.db"
            )

            os.makedirs(config['output']['excel_folder'], exist_ok=True)
            os.makedirs(config['output']['database_folder'], exist_ok=True)

            acat.save_to_excel(student_outcomes, excel_output)
            acat.save_to_sqlite(db_output, student_outcomes)


if __name__ == "__main__":
    main()