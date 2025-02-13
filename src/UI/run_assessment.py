from dotenv import load_dotenv
import os
load_dotenv("../")
for key, value in os.environ.items():
    print(f"{key}: {value}")

import sys
import logging
import crewai as crewai
import langchain_openai as lang_oai
import crewai_tools as crewai_tools
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource

from src.Agents.assignment_agent import AssignmentAgent
from src.Agents.course_outcomes_agent import CourseOutcomesAgent
from src.Helpers.pretty_print_crewai_output import display_crew_output

# Initialize logger
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

gpt_4o_high_tokens = lang_oai.ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.0,
    max_tokens=1500
)

class AssessmentCrew:
  def __init__(self):
      self.is_init = True

  def run(self):

    comp_101 = ExcelKnowledgeSource(file_paths=["COMP-101.xlsx"])
    comp_103 = ExcelKnowledgeSource(file_paths=["COMP-103.xlsx"])
    comp_245 = ExcelKnowledgeSource(file_paths=["COMP-245.xlsx"])
    grades_source = ExcelKnowledgeSource(
       file_paths=["synthetic_student_grades.xlsx"]
    )

    assignment_agent = AssignmentAgent(llm=gpt_4o_high_tokens, Knowledge_sources=[grades_source, comp_101, comp_103, comp_245 ])

    assignment_to_course_outcomes_source = ExcelKnowledgeSource(
       file_paths=["synthetic_student_grades.xlsx", "assignment_to_course_outcomes_map.xlsx", "COMP-101.xlsx", "COMP-103.xlsx", "COMP-245.xlsx"]
    )
    course_outcomes_agent = CourseOutcomesAgent(llm=gpt_4o_high_tokens, knowledge_sources=[assignment_to_course_outcomes_source, comp_101, comp_103, comp_245])

    course_outcomes_to_program_outcomes_source = ExcelKnowledgeSource(
       file_paths=["course_outcomes_to_program_outcomes_mapping.xlsx"]
    )



    agents = [ course_outcomes_agent ]

    tasks = [course_outcomes_agent.assess_course_outcomes_from_assignment_grades() ]
    

    # Run initial tasks
    crew = crewai.Crew(
        agents=agents,
        tasks=tasks,
        #knowledge=[grades_source, assignment_to_course_outcomes_source],[]
        process=crewai.Process.sequential,
        verbose=True
    )

    for agent in crew.agents:
      logger.info(f"Agent Name: '{agent.role}'")

    result = crew.kickoff()

    return result

if __name__ == "__main__":
    print("## Assessment Analysis")
    print('-------------------------------')
  
    assessment_crew = AssessmentCrew()
    logging.info("Assessment crew initialized successfully")

    try:
        crew_output = assessment_crew.run()
        logging.info("Assessment crew execution run() successfully")
    except Exception as e:
        logging.error(f"Error during crew execution: {e}")
        sys.exit(1)
    
    # Accessing the crew output
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")

    display_crew_output(crew_output)

    print("Collaboration complete")
    sys.exit(0)
