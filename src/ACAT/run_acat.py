import os
import json
import pandas as pd
import src.ACAT.acat as ac
#from acat import ACAT

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def main():
    config = load_config("acat_config.json")
    course_outcomes_results = {}

    for course in config['courses']:
        course_name = course['course_name']
        semester = course['semester']
        outcomes = ac.read_outcomes(course['outcomes_file'])

        for section_data in course['sections']:
            section = section_data['section']
            assignments_mapping = ac.read_assignments(section_data['assignments_file'])
            final_outcomes = {
                outcome: [assignments_mapping.get(outcome, crit) for crit in criteria] 
                for outcome, criteria in outcomes.items()
            }

            student_data = ac.read_grades(section_data['grades_file'], sum(final_outcomes.values(), []))

            acat = ac.ACAT(course_name, semester, section, final_outcomes, student_data)
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

