from helpers.extension import Extension

class TestExtension(Extension):
    def __init__(self) -> None:
        self.name = "test"

    async def on_ready(self):
        print("Test extension is ready!")

    async def on_message(self, message, user):
        print("Test extension got a message!")