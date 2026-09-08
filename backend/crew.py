import re

from crewai import Crew, Process
from backend.tasks.learning_tasks import create_learning_tasks
from backend.agents.agents import LearningAgents
from backend.llm.factory import LLMFactory

# Strips common LLM preambles/markers agents sometimes emit despite instructions
# not to (e.g. "Final Answer:"). Applied per-section, since each task's raw
# output is now assembled directly rather than passed through a final
# "aggregator" LLM call that used to normalize this implicitly.
#
# Deliberately does NOT touch ``` anywhere in the body: a section's raw text
# can legitimately contain fenced code examples, and a regex that strips "the
# first bare ``` it finds" can just as easily delete a real closing fence from
# an example as a spurious wrapper — unbalancing fences for the rest of that
# section and corrupting Markdown rendering for everything after it.
_PREAMBLE_PATTERNS = [
    re.compile(r"(?i)^System:.*?\n"),
    re.compile(r"(?i)^You are.*?\n"),
    re.compile(r"(?i)^Final Answer:.*?\n"),
    re.compile(r"(?i)^---.*?\n"),
]


def _sanitize(text: str) -> str:
    clean_text = str(text)
    for pattern in _PREAMBLE_PATTERNS:
        clean_text = pattern.sub("", clean_text, count=1).strip()

    # Some models wrap their *entire* answer in one outer fence (e.g. a whole
    # response inside ```markdown ... ```). Unwrap only a genuine outer pair —
    # first line opens a fence, last line is a bare closing fence — which
    # can't accidentally match a fence that's part of real content in between.
    lines = clean_text.splitlines()
    if len(lines) > 1 and lines[0].lstrip().startswith("```") and lines[-1].strip() == "```":
        clean_text = "\n".join(lines[1:-1]).strip()

    # Defense in depth: if this section still ends up with an odd number of
    # ``` fences (model wrote a genuinely malformed/unclosed code block),
    # close it here rather than let broken fence-parity bleed into whatever
    # section gets concatenated after this one.
    if clean_text.count("```") % 2 == 1:
        clean_text += "\n```"

    return clean_text


class MentorCrew:
    def __init__(self, topic, llm_config=None):
        self.topic = topic
        # Get LLM instance based on config
        self.llm = LLMFactory.get_llm(llm_config)
        self.learning_agents = LearningAgents(self.llm)

    def run(self, task_callback=None):
        roadmap_task, youtube_task, explanation_task = create_learning_tasks(
            self.topic, self.learning_agents
        )

        crew = Crew(
            agents=[
                self.learning_agents.curriculum_planner(),
                self.learning_agents.youtube_search_agent(),
                self.learning_agents.concept_explainer(),
            ],
            tasks=[roadmap_task, youtube_task, explanation_task],
            process=Process.sequential,
            verbose=True,
            task_callback=task_callback,
        )

        crew.kickoff()

        return self._assemble_document(roadmap_task, explanation_task, youtube_task)

    @staticmethod
    def _assemble_document(roadmap_task, explanation_task, youtube_task):
        sections = [
            ("## Learning Roadmap", roadmap_task.output.raw),
            ("## Concept Explanations", explanation_task.output.raw),
            ("## YouTube Resources", youtube_task.output.raw),
        ]
        return "\n\n---\n\n".join(
            f"{header}\n\n{_sanitize(body)}" for header, body in sections
        )
