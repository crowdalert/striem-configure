import yaml

from prompt_toolkit.layout import AnyContainer
from prompt_toolkit.widgets import TextArea, Label, Checkbox
from prompt_toolkit.layout.containers import HSplit, ConditionalContainer
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.filters import Condition

from . import Source


class GCP(Source):
    label = "Google Workspace / GCP Audit Logs"

    project: TextArea
    subscription: TextArea
    credentials_path: TextArea
    api_key: TextArea
    system_creds: Checkbox

    def __init__(self, *args, **kwargs):
        self.subscription = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=50),
        )
        self.project = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=50),
        )
        self.credentials_path = TextArea(
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
            text="Use system or environment GCP credentials", checked=False
        )
        self.container = HSplit(
            [
                Label(text="GCP Project"),
                self.project,
                Label(text="Pub/Sub Subscription"),
                self.subscription,
                ConditionalContainer(
                    HSplit(
                        [
                            Label(text=""),
                            Label(text="Service Account JSON File"),
                            self.credentials_path,
                            Label(text=" or"),
                            Label(text="API Key"),
                            self.api_key,
                            Label(text=" or"),
                        ],
                    ),
                    filter=Condition(lambda: not self.system_creds.checked),
                ),
                self.system_creds,
            ],
        )

        super().__init__(*args, **kwargs)

    def validate(self):
        return all([self.project.text, self.subscription.text]) and (
            self.system_creds.checked
            or any([self.api_key.text, self.credentials_path.text])
        )

    def dump(self) -> str:
        data = {
            "project": self.project.text,
            "subscription": self.subscription.text,
        }
        if not self.system_creds.checked:
            if self.api_key.text:
                data["api_key"] = self.api_key.text
            else:
                data["credentials_path"] = self.credentials_path.text

        return "\n".join(
            [
                yaml.dump(
                    {
                        "sources": {
                            f"source-gcp-{self.id}": {
                                "type": "gcp_pubsub",
                                "decoding": {"codec": "json"},
                            }
                            | data
                        }
                    }
                ),
                self.template.substitute(id=self.id),
            ]
        )

    @property
    def body(self) -> AnyContainer:
        return self.container
