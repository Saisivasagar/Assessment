import re
from pydantic import BaseModel, Field
from textwrap import dedent
import crewai as crewai
from datetime import datetime
import os
from src.Agents.base_agent import BaseAgent



class CourseOutcomesAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role='Course Outcomes Agent',
            goal="Map student assignment grades to course outcomes",
            backstory='An expert in assessing course outcomes',
            tools=[],
            **kwargs)
        
        self.previous_report = None

    def assess_course_outcomes_from_assignment_grades(self):
            
        
        return crewai.Task(
             description=dedent(f"""

               You have access to the following files for Course 101 and Course 103:

                Course 101 Files:
                1. grades_101.xlsx – Contains student grades for various assignments.
                2. COMP-101.xlsx – Describes mappings of each assignment specification to the course outcomes.
                                
                Course 103 Files:
                1. grades_103.xlsx – Contains student grades for various assignments.
                2. COMP-103.xlsx – Describes mappings of each assignment specification to the course outcomes.
                                
                File Structure:
                - Assessments are limited to Course 101 and Course 103.
                - All necessary data, including outcome mappings, student grades, and assignment specifications, are provided.
                - Student grade files contain student IDs, assignment names, and grades.
                - Ensure that Course 101 uses student IDs: 11, 12, 13, 14, 15.
                - Ensure that Course 103 uses student IDs: Student_1, Student_2, Student_3, Student_4, Student_5.
                                
                Task:
                - Assess student capabilities for each course outcome for Course 101 and Course 103 based on the provided mappings.
                - Utilize assignment grades (Final Exam and Final Project) to determine student performance.
                - Use assignment specifications to understand the context and learning objectives of each assignment.
                - Map assignments to outcomes using the provided course mapping files.
                - Ensure that student IDs are mapped correctly based on their enrollment in Course 101 and Course 103.
                - Calculate the average grade for each student per course outcome based on their performance in the mapped assignments.
                - Generate a summary report displaying the correctly mapped student IDs and their average grades for each course outcome.
                                
                Output Requirements:
                - Clearly label the final report for both Course 101 and Course 103.
                - Include five student IDs in the assessment output for each course.
                - Limit the analysis to four course outcomes for Course 101 and seven course outcomes for Course 103.
                - Ensure the output table is structured with student IDs as rows and course outcomes as columns, with each cell containing the correct average grade for that outcome.
                - The outcome column headings should be simply:
                    Course 101: Outcome:1, Outcome:2, Outcome:3, Outcome:4
                    Course 103: Outcome:1, Outcome:2, Outcome:3, Outcome:4, Outcome:5, Outcome:6, Outcome:7
                                 
                Expected Output:

                -    Provide two well-formatted tables: one for Course 101 and one for Course 103 that showing each student's average grade for each course outcome based on their performance in the Final Exam and Final Project.
                -    Ensure the correct mapping of student IDs and their corresponding average grades per outcome.
                -    Provide a brief summary explaining key insights from the assessment, including identifying top-performing students and areas where students may need improvement.

                                            
            """),

            


            agent=self,
            expected_output="Tables with the course outcomes assessment for course 101 and course 103."
        )
    

