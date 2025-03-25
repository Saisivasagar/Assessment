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
#from crewai.knowledge.source.crew_docling_source import CrewDoclingSource

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
    comp_301 = ExcelKnowledgeSource(file_paths=["COMP-301.xlsx"])
    comp_308 = ExcelKnowledgeSource(file_paths=["COMP-308.xlsx"])
    #comp_315 = ExcelKnowledgeSource(file_paths=["COMP-315.xlsx"])
    #comp_335 = ExcelKnowledgeSource(file_paths=["COMP-335.xlsx"])
    #comp_385 = ExcelKnowledgeSource(file_paths=["COMP-385.xlsx"])
    #comp_405 = ExcelKnowledgeSource(file_paths=["COMP-405.xlsx"])
    #comp_431 = ExcelKnowledgeSource(file_paths=["COMP-431.xlsx"])
    #comp_450 = ExcelKnowledgeSource(file_paths=["COMP-450.xlsx"])
    #comp_552 = ExcelKnowledgeSource(file_paths=["COMP_552_MAPPING.xlsx"])
    grades_source = ExcelKnowledgeSource(
       file_paths=["grades_101.xlsx", "grades_103.xlsx", "grades_245.xlsx", "grades_301.xlsx", "grades_308.xlsx"]
    )

    assignment_agent = AssignmentAgent(llm=gpt_4o_high_tokens, knowledge_sources=[grades_source])

    assignment_to_course_outcomes_source = ExcelKnowledgeSource(
       file_paths=[ "grades_101.xlsx", "COMP-101.xlsx", "grades_103.xlsx", "COMP-103.xlsx", "grades_245.xlsx", "COMP-245.xlsx", "grades_301.xlsx", "COMP-301.xlsx", "grades_308.xlsx", "COMP-308.xlsx"]
    )
    course_outcomes_agent = CourseOutcomesAgent(llm=gpt_4o_high_tokens, knowledge_sources=[comp_101, comp_103, comp_245, comp_301, comp_308]
    )

    #course_outcomes_to_program_outcomes_source = ExcelKnowledgeSource( file_paths=["course_outcomes_to_program_outcomes_mapping.xlsx"])



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
