"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import time

from HelpGuy import style

data = [
    {"name": "Page A", "uv": 4000, "pv": 2400, "amt": 2400},
    {"name": "Page B", "uv": 3000, "pv": 1398, "amt": 2210},
    {"name": "Page C", "uv": 2000, "pv": 9800, "amt": 2290},
    {"name": "Page D", "uv": 2780, "pv": 3908, "amt": 2000},
    {"name": "Page E", "uv": 1890, "pv": 4800, "amt": 2181},
    {"name": "Page F", "uv": 2390, "pv": 3800, "amt": 2500},
    {"name": "Page G", "uv": 3490, "pv": 4300, "amt": 2100},
]

data01 = [
    {"name": "Group A", "value": 400},
    {"name": "Group B", "value": 300},
    {"name": "Group C", "value": 300},
    {"name": "Group D", "value": 200},
    {"name": "Group E", "value": 278},
    {"name": "Group F", "value": 189},
]
class TextfieldControlled(rx.State):
    text: str = ""
class State(rx.State):
    """The app state."""

    prompt = ""
    processing = False
    complete = False

    def process_output(self):
        """Get the output from the prompt."""
        if self.prompt == "":
            return rx.window_alert("Prompt Empty")
        self.processing = True
        time.sleep(2)
        self.complete = True
        if self.complete:
            print("should change to another page")
            return rx.redirect("/results")

        #self.processing, self.complete = True, False
        # ai stuff
        # response = openai_client.images.generate(
        #     prompt=self.prompt, n=1, size="1024x1024"
        # )
        # self.image_url = response.data[0].url
        # self.processing, self.complete = False, True

def action_bar() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Ask a question",
            on_blur=State.set_prompt,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            rx.icon(tag = "heart"),
            class_name = "transition transform hover:-translate-y-1 motion-reduce:transition-none motion-reduce:hover:transform-none ...",

            border_radius = "1em",
            box_shadow = "rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
            background_image = "linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
            box_sizing = "border-box",
            color = "white",
            opacity = 1,
            _hover = {
                "opacity": 0.5,
            },
           on_click = State.process_output
        ),
        justify = "center",
        align="end"
    )


# def index() -> rx.Component:

    return rx.flex(rx.stack(
        rx.box(
            rx.text('Your Chat Bot',
                    class_name=" overflow-hidden whitespace-nowrap border-r-4 border-r-white pr-5 text-5xl text-black font-bold",),
                    text_align='center',
                    font_weight='bold',
                    ),
            action_bar(),
            direction = 'column',
            align = 'center',
            justify = 'center',
        ),

        rx.text(State.response),

        rx.vstack(
            rx.hstack(
                rx.box(rx.text('Welcome! Enter your health information above', 
                               color='white'),  
                        border_radius="9px",
                        width="30%",
                        margin="4px",
                        padding="30px", 
                        background="linear-gradient(45deg, var(--tomato-9), var(--plum-9))", 
                        class_name = 'animate-bounce', 
                        ),
                rx.box(rx.image(src = "/dino.png", 
                                width = "300px", 
                                height = "auto"),
                        ), 
                align = 'center'),
                align = 'end', 
                justify = 'end', 
            ),
            justify="end"
            direction = 'column',
            background_image = "url('https://media.discordapp.net/attachments/1230238647618371665/1231197092656185415/image.png?ex=663614a5&is=66239fa5&hm=5217e91f091d2ab13c5e6d6a723dec685b9215c07f2f517f1fef9bea318b5952&=&format=webp&quality=lossless&width=1554&height=978')",
            height="100vh",
            background_size = "cover",
    )

app = rx.App()
app.add_page(index)

