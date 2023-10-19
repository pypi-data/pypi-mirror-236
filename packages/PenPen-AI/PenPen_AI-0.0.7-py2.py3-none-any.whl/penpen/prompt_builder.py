from typing import Optional, List, Dict


class FactFormatError(Exception):
    """Passed facts MUST have a tag and a content key field."""

    pass


class PromptBuilder:
    def __init__(
        self,
        facts: Optional[List[Dict[str, str]]] = None,
        fact_tag_filter: Optional[List[str]] = None,
        persona: str = "",
        task_parameters: Optional[Dict] = None,
        task_template: str = "",
    ):
        self.facts = facts or []
        self.fact_tag_filter = fact_tag_filter or []
        self.persona = persona
        self.task_parameters = task_parameters or {}
        self.task_template = task_template

    def getOpenAIPrompt(self):
        messages = []

        # add persona system message
        persona_message = {
            "role": "system",
            "content": self.persona,
        }
        messages.append(persona_message)

        # filter facts and parse them as markdown formatted system message
        formatted_facts = []

        # Verify each fact has the required keys
        for fact in self.facts:
            if "tag" not in fact.keys() or "content" not in fact.keys():
                raise FactFormatError(
                    "Each element of 'facts' must contain a 'tag' key and a 'content' key."
                )
            if fact["tag"] in self.fact_tag_filter:
                formatted_facts.append(f"## {fact['tag']}: {fact['content']}")

        if formatted_facts:
            facts_md = "\n".join(formatted_facts)
            messages.append(
                {
                    "role": "system",
                    "content": f"---FACTS---\n{facts_md}\n---END-FACTS---",
                }
            )

        # add task user message
        messages.append(
            {
                "role": "user",
                "content": self.task_template.format(**self.task_parameters),
            },
        )

        return messages
