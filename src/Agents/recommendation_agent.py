import logging
from .base_agent import BaseAgent


class RecommendationAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Recommendation Agent",
            goal="Provide tailored strategies for curriculum improvement based on analysis and alignment results.",
            backstory="An expert in educational strategy, ensuring curriculum aligns with industry trends and student needs.",
            tools=[],
            **kwargs
        )

        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def suggest_curriculum_updates(self, curriculum_data):
       
        recommended_updates = []

        for course in curriculum_data.get("courses", []):
            if course in ["Introduction to AI", "Cybersecurity Basics"]:
                recommended_updates.append(f"Expand {course} with real-world case studies.")
            if "outdated" in curriculum_data.get("tags", []):
                recommended_updates.append(f"Revise {course} to include recent advancements.")

        return {"curriculum_updates": recommended_updates}

    def tailor_recommendations(self, institution_goals, student_profiles):
       
        tailored_suggestions = []

        if institution_goals.get("focus") == "Tech Innovation":
            tailored_suggestions.append("Introduce courses on Blockchain and Quantum Computing.")
        if student_profiles.get("learning_preference") == "Hands-on":
            tailored_suggestions.append("Increase project-based assessments and lab sessions.")

        return {"tailored_recommendations": tailored_suggestions}

    def highlight_actionable_steps(self, knowledge_gaps):
       
        actions = []

        for gap in knowledge_gaps.get("gaps", []):
            actions.append(f"Develop a targeted workshop for {gap}.")
            actions.append(f"Offer online resources and tutoring sessions on {gap}.")

        return {"actionable_steps": actions}
