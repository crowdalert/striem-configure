from prompt_toolkit.layout import HSplit, AnyContainer
from prompt_toolkit.widgets import Label
from prompt_toolkit.formatted_text import HTML

from sources._source import Source


class GithubEnterpriseAudit(Source):
    label = "Github Enterprise Audit Logs"

    def __init__(self, id=None):
        super().__init__(id)

    def validate(self):
        return True

    def dump(self) -> str:
        return self.template.substitute(id=self.id)

    @property
    def friendly_id(self) -> str:
        return str(self.id)

    @property
    def body(self) -> AnyContainer:
        return HSplit(
            [
                Label(text=HTML("<b>HEC Token</b>")),
                Label(text=str(self.id)),
            ]
        )
