from prompt_toolkit.layout import AnyContainer
from prompt_toolkit.widgets import TextArea, Label, Checkbox
from prompt_toolkit.layout.containers import HSplit, ConditionalContainer
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.filters import Condition

from . import Source


class GCP(Source):
    label = "Okta Audit Logs"

    url: TextArea
    api_key: TextArea

    def __init__(self, *args, **kwargs):
        self.url = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=50),
        )
        self.api_key = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=50),
            password=True,
        )

        self.system_creds = Checkbox(
            text="Use API key from environment (OKTA_API_KEY)", checked=False
        )
        self.container = HSplit(
            [
                Label(text="Okta URL"),
                self.url,
                ConditionalContainer(
                    HSplit(
                        [
                            Label(text="API Key"),
                            self.api_key,
                        ],
                    ),
                    filter=Condition(lambda: not self.system_creds.checked),
                ),
                self.system_creds,
            ],
        )

        super().__init__(*args, **kwargs)

    @property
    def friendly_id(self) -> str:
        return self.url.text

    def validate(self):
        return bool(self.url.text) and (
            self.system_creds.checked or bool(self.api_key.text)
        )

    def dump(self) -> str:
        return self.template.substitute(id=self.id)

    def striem_config(self) -> dict:
        return {
            "ingest": [
                {
                    "okta": {
                        "url": self.url.text,
                        "api_key": self.api_key.text,
                        "since": 0,
                    }
                }
            ]
        }

    @property
    def body(self) -> AnyContainer:
        return self.container
