"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import time

from HelpGuy import style

data = [
    {"name": "Page A", "uv": 4000, "pv": 2400, "amt": 2400},
    {"name": "Page B", "uv": 3000, "pv": 1398, "amt": 2210},
    {"name": "Page C", "uv": 2000, "pv": 9800, "amt": 2290},
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
            return rx.redirect('/results')

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
            # on_click = rx.redirect('/results')
           on_click = State.process_output
        ),
        justify = "center",
        align="end"
    )


def index() -> rx.Component:

    return rx.flex(

        rx.cond(State.processing, rx.text('in progress')),

    rx.stack(
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
                align = "center"),
                align = 'end',
                justify = 'end',
            ),
            justify = 'end',
            direction = 'column',
            background_image = "url('https://media.discordapp.net/attachments/1230238647618371665/1231197092656185415/image.png?ex=663614a5&is=66239fa5&hm=5217e91f091d2ab13c5e6d6a723dec685b9215c07f2f517f1fef9bea318b5952&=&format=webp&quality=lossless&width=1554&height=978')",
            height="100vh",
            background_size = "cover",
    )
@rx.page(route="/results", title="Results Page")
def about() -> rx.Component:

    return(rx.flex(

           rx.grid(
               rx.foreach(
                rx.Var.range(3),  # Assuming you want to display 3 cards
                lambda i: rx.card(rx.recharts.bar_chart(
                rx.recharts.bar(data_key="uv", stroke="#8884d8", fill="#8884d8"),
                rx.recharts.x_axis(data_key="name"),
                rx.recharts.y_axis(),
                data=data,
            ),
                                   height="25vh"),

            ),
            rows="3",  # This specifies that you want 3 rows for your cards
            flow="column",  # This sets the flow to column, aligning items vertically
            justify="start",  # Aligns the grid to the start (left side) of its container
            spacing="4",  # Sets spacing between cards
            width="50%",  # Ensures the grid takes the full width of its container
            ),


            rx.hstack(
                action_bar(),
                rx.box(rx.image(src="/dino.png",
                                width="300px",
                                height="auto"),
                                )

            ),


            bg="lightblue",
            width="100%",
            height="100vh",
            display="flex",
            flex_direction="row",
            align_items="center",
            justify_content="center",
            padding="5%",
            overflow="hidden"
            )
        )



app = rx.App()
app.add_page(index)
app.compile()
