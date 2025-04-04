from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

style = Style.from_dict(
    {
        "dialog.body select-box": "bg:#cccccc",
        "dialog.body select-box cursor-line": "nounderline bg:ansired fg:ansiwhite",
        "dialog.body select-box last-line": "underline",
        "dialog.body text-area": "bg:#4444ff fg:white",
    }
)

kb = KeyBindings()


@kb.add("f6")
def _exit(event):
    event.app.exit()
