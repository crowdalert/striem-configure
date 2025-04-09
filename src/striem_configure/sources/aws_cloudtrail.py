import yaml

from prompt_toolkit.widgets import Label, Checkbox
from prompt_toolkit.layout import AnyContainer, ConditionalContainer
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.filters import Condition

from . import Source


class AwsCloudtrail(Source):
    label = "AWS CloudTrail"

    queue_url: TextArea
    region: TextArea
    role: TextArea

    def __init__(self, *args, **kwargs):
        self.queue_url = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
        )
        self.region = TextArea(
            text="us-east-1",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
        )
        self.role = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
        )
        self.aws_access_key_id = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
        )
        self.aws_secret_access_key = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
            password=True,
        )

        disabled = Checkbox(text="Use environment IAM credentials", checked=True)
        self.container = HSplit(
            [
                Label(text="SQS Queue URL"),
                self.queue_url,
                Label(text="Region"),
                self.region,
                Label(text="IAM Role ARN to assume"),
                self.role,
                Label(text=""),
                disabled,
                Label(text=""),
                ConditionalContainer(
                    HSplit(
                        [
                            Label(text="AWS Access Key ID"),
                            self.aws_access_key_id,
                            Label(text="AWS Secret Access Key"),
                            self.aws_secret_access_key,
                        ]
                    ),
                    filter=Condition(lambda: not disabled.checked),
                ),
            ],
        )

        super().__init__(*args, **kwargs)

    @property
    def friendly_id(self) -> str:
        return str(self.queue_url.text)

    def validate(self) -> bool:
        return bool(self.queue_url.text) and (
            (self.aws_access_key_id.text and self.aws_secret_access_key.text)
            or (not self.aws_access_key_id.text and not self.aws_secret_access_key.text)
        )

    def dump(self) -> str:
        data = {
            "sqs": {"queue_url": self.queue_url.text},
        }
        if self.aws_access_key_id.text and self.aws_secret_access_key.text:
            data["auth"] = {
                "aws_access_key_id": self.aws_access_key_id.text,
                "aws_secret_access_key": self.aws_secret_access_key.text,
            }

        if self.role.text:
            if data.get("auth") is None:
                data["auth"] = {}
            data["auth"]["assume_role"] = self.role.text

        return "\n".join(
            [
                yaml.dump(
                    {
                        "sources": {
                            f"source-aws_cloudtrail-{self.id}": {
                                "type": "aws_s3",
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
