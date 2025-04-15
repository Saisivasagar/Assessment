import pandas as pd
import sqlite3

class ACAT:
    def __init__(self, course_name, semester, section, outcomes, student_data):
        self.course_name = course_name
        self.semester = semester
        self.section = section
        self.outcomes = outcomes
        self.student_data = student_data
    
    def compute_course_outcomes(self):
        student_outcomes = {}
        for student_id, grades in self.student_data.items():
            print("\n\nstudent_id: ", student_id)
            print("grades\n", grades)
            student_outcomes[student_id] = {}
            for outcome, criteria in self.outcomes.items():
                outcome_scores = [grades[criterion] for criterion in criteria if criterion in grades]
                avg_score = sum(outcome_scores) / len(outcome_scores) if outcome_scores else 0
                likert_score = self.to_likert(avg_score)
                print("\noutcome: ", outcome)
                student_outcomes[student_id][outcome] = likert_score
        return student_outcomes

    @staticmethod
    def to_likert(score):
        if score >= 90:
            return 5
        elif score >= 80:
            return 4
        elif score >= 70:
            return 3
        elif score >= 60:
            return 2
        else:
            return 1

    def summarize_course_outcomes(self, student_outcomes):
        summary = {}
        for outcome in self.outcomes:
            outcome_scores = [scores[outcome] for scores in student_outcomes.values()]
            avg_score = sum(outcome_scores) / len(outcome_scores)
            summary[outcome] = avg_score
            print(f"Course Outcome: {outcome}, Class Likert Average: {avg_score:.2f}")
        return summary

    def save_to_excel(self, student_outcomes, filename):
        df = pd.DataFrame.from_dict(student_outcomes, orient='index')
        df.to_excel(filename)

    def save_to_sqlite(self, db_name, student_outcomes):
        conn = sqlite3.connect(db_name)
        df = pd.DataFrame.from_dict(student_outcomes, orient='index')
        table_name = f"{self.course_name}".replace("-", "_")
        df.to_sql(table_name, con=conn, if_exists='replace', index_label='SIS_User_ID')
        conn.close()

    def compute_program_outcomes(self, program_config, course_results):
        program_outcomes = {}
        for program, outcomes in program_config.items():
            print("\n\nProgram: ", program)
            print("\nOutcomes\n", outcomes)
            program_outcomes[program] = {}
            for po, course_outcome_ids in outcomes.items():
                combined_scores = []
                for outcome_id in course_outcome_ids:
                    course, semester, outcome_name = outcome_id.split('.')
                    outcome_key = f"{course}_{semester}"
                    if outcome_key in course_outcomes_results:
                        combined_scores.extend(course_outcomes_results[outcome_key][outcome_name])
                avg_score = sum(combined_scores) / len(combined_scores) if combined_scores else 0
                program_outcomes[outcome] = avg_score
        return program_outcomes

    def compute_institution_outcomes(self, institution_config, program_outcomes_results):
        institution_outcomes = {}
        for outcome, program_outcome_ids in institution_config.items():
            combined_scores = []
            for po_id in program_outcome_ids:
                program, po = po_id.split('.')
                if program in program_outcome_results:
                    combined_scores.append(program_outcome_results[program][po])
            avg_score = sum(combined_scores) / len(combined_scores)
            institution_outcomes[outcome] = avg_score
        return institution_outcomes