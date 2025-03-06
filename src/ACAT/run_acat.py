import os
import json
import pandas as pd
from acat import ACAT

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)
    
def read_outcomes(outcomes_file):
    outcomes_df = pd.read_excel(outcomes_file)
    outcomes = {}
    for _, row in outcomes_df.iterrows():
        outcome = row.iloc[0]
        criteria = [col for col in outcomes_df.columns[1:] if pd.notnull(row[col])]
        outcomes[outcome] = criteria
    return outcomes    

def read_assignments(assignments_file):
    assignments_df = pd.read_excel(assignments_file)
    return assignments_df.set_index('Outcome')['Assignment'].to_dict()

def read_grades(grades_file, required_columns):
    grades_df = pd.read_csv(grades_file)
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
            assignments_mapping = read_assignments(section_data['assignments_file'])
            final_outcomes = {
                outcome: [assignments_mapping.get(outcome, crit) for crit in criteria] 
                for outcome, criteria in outcomes.items()
            }

            student_data = read_grades(section_data['grades_file'], sum(final_outcomes.values(), []))

            acat = ACAT(course_name, semester, section, final_outcomes, student_data)
            student_outcomes = acat.compute_course_outcomes()
            acat.summarize_outcomes(student_outcomes)

            excel_output = os.path.join(config['output']['excel_folder'], 
                                        f"{course_name}_{semester}_{section}_outcomes.xlsx")
            db_output = os.path.join(config['output']['database_folder'], 
                                     f"{course_name}_{semester}_{section}_outcomes.db")

            os.makedirs(config['output']['excel_folder'], exist_ok=True)
            os.makedirs(config['output']['database_folder'], exist_ok=True)

            acat.save_to_excel(student_outcomes, excel_output)
            acat.save_to_sqlite(db_output, student_outcomes)

if __name__ == "__main__":
    main()

