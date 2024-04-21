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
class correctOutputState(rx.State):
    is_correct = False
    button_click = False

    def set_correct(self):
        self.button_click = True
        self.is_correct = True
    def set_need_to_check(self):
        self.button_click = True
        self.is_correct = False

class State(rx.State):
    """The app state."""

    prompt = ""
    processing = False
    complete = False

    def process_output(self):
        """Get the output from the prompt."""
        correctOutputState.is_correct = False
        correctOutputState.button_click = False
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
            background_size = "cover",)

def line_chart() -> rx.Component:
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key = "pv",
            stroke = "#7A8FB8",
        ),
        rx.recharts.line(
            datakey = "uv",
            stroke = "#7A8FB8",
        ),
        rx.recharts.x_axis(data_key = "name"),
        rx.recharts.y_axis(),
        rx.recharts.cartesian_grid(stroke_dasharray = "3 3"),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        data = data, )

def pi_chart() -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=data01,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            fill="#7A8FB8",
            label=True,

    ),
        rx.recharts.legend(),
        height ="90%",
        width="90%"
    )

def scroll_area() -> rx.Component:
    return rx.scroll_area(
        rx.flex(
            rx.heading("Symptoms",  font_family="Rajdhani"),
                        rx.text(
                """Three fundamental aspects of typography are legibility, readability, and
            aesthetics. Although in a non-technical sense “legible” and “readable”
            are often used synonymously, typographically they are separate but
            related concepts.""",
            ),
            rx.text(
                """Legibility describes how easily individual characters can be
            distinguished from one another. It is described by Walter Tracy as “the
            quality of being decipherable and recognisable”. For instance, if a “b”
            and an “h”, or a “3” and an “8”, are difficult to distinguish at small
            sizes, this is a problem of legibility.""",
            ),
            rx.text(
                """Typographers are concerned with legibility insofar as it is their job to
            select the correct font to use. Brush Script is an example of a font
            containing many characters that might be difficult to distinguish. The
            selection of cases influences the legibility of typography because using
            only uppercase letters (all-caps) reduces legibility.""",
            ),
            direction = "column",
            spacing = "4",
        ),
        type = "always",
        scrollbars = "vertical",
    )

def scroll_horizontal_area() -> rx.Component:
    return rx.grid(
        rx.scroll_area(
            rx.flex(
                rx.text("first treatment",  font_family="Rajdhani", weight = "bold"),
                rx.text(
                    """Legibility describes how easily individual characters can be
            distinguished from one another. It is described by Walter Tracy as "the
            quality of being decipherable and recognisable". For instance, if a "b"
            and an "h", or a "3" and an "8", are difficult to distinguish at small
            sizes, this is a problem of legibility.""",
                    size = "2",
                    trim = "both",
                ),
                padding = "8px",
                direction = "column",
                spacing = "4",
            ),
            type = "auto",
            scrollbars = "vertical",
            style = {"height": 200},
        ),
        rx.scroll_area(
            rx.flex(
                rx.text("second treatment",  font_family="Rajdhani", weight = "bold"),
                rx.text(
                    """Legibility describes how easily individual characters can be
            distinguished from one another. It is described by Walter Tracy as "the
            quality of being decipherable and recognisable". For instance, if a "b"
            and an "h", or a "3" and an "8", are difficult to distinguish at small
            sizes, this is a problem of legibility.""",
                    size = "2",
                    trim = "both",
                ),
                padding = "8px",
                direction = "column",
                spacing = "4",
            ),
            type = "always",
            scrollbars = "vertical",
            style = {"height": 200},
        ),
        rx.scroll_area(
            rx.flex(
                rx.text("third treatment",  font_family="Rajdhani", weight = "bold"),
                rx.text(
                    """Legibility describes how easily individual characters can be
            distinguished from one another. It is described by Walter Tracy as "the
            quality of being decipherable and recognisable". For instance, if a "b"
            and an "h", or a "3" and an "8", are difficult to distinguish at small
            sizes, this is a problem of legibility.""",
                    size = "2",
                    trim = "both",
                ),
                padding = "8px",
                direction = "column",
                spacing = "4",
            ),
            type = "scroll",
            scrollbars = "vertical",
            style = {"height": 200},
        ),
        rx.scroll_area(
            rx.flex(
                rx.text("fourth treatment",  font_family="Rajdhani", weight = "bold"),
                rx.text(
                    """Legibility describes how easily individual characters can be
            distinguished from one another. It is described by Walter Tracy as "the
            quality of being decipherable and recognisable". For instance, if a "b"
            and an "h", or a "3" and an "8", are difficult to distinguish at small
            sizes, this is a problem of legibility.""",
                    size = "2",
                    trim = "both",
                ),
                padding = "8px",
                direction = "column",
                spacing = "4",
            ),
            type = "hover",
            scrollbars = "vertical",
            style = {"height": 200},
        ),
        columns = "4",
        spacing = "2",
    )
@rx.page(route="/results", title="Results Page")
def about() -> rx.Component:

    return (
        rx.flex(rx.vstack(
            rx.hstack(
            rx.card(scroll_area(), width="60%", height="400px"),
                    rx.card(rx.heading("Recovery Time",
                                       font_family="Rajdhani"),
                            line_chart(),
                            width="60%",
                            height="400px"),
                    rx.vstack(
                        rx.card(
                            rx.heading("Probability Metric",
                                       font_family="Rajdhani"),
                            pi_chart(),
                            width="100%",
                            height="300px"),
                              rx.card(
                                  rx.heading("Most Likely Match:",
                                             font_family="Rajdhani"),
                                  rx.text("Nosebleeds"),
                                  width="100%",
                                  height="100px"),
                        width="40%"),

                justify = "between",
                align = "stretch",
                spacing = "4",
                width="100%"
            ),
            rx.hstack(
                rx.cond((correctOutputState.button_click == False) |
                        ((correctOutputState.is_correct == True) & (correctOutputState.button_click == True)),
                        rx.card(
                            rx.heading("Treatments", font_family = "Rajdhani"),
                            scroll_horizontal_area(), width = "70%", height = "200px"),
                        ),

                # action_bar(),
                rx.cond(correctOutputState.button_click == False, rx.box(
                    rx.text("Does this look accurate?",
                               color = "white"),
                       rx.vstack(
                           rx.hstack(
                               rx.button(
                                   rx.icon(tag = "check"),
                                   on_click = correctOutputState.set_correct,

                               ),
                               rx.button(
                                   rx.icon(tag = "x"),
                                   on_click = correctOutputState.set_need_to_check,
                               ),
                               spacing = "2",
                               justify = "end",
                               align = "center"
                           ),
                       ),

                       border_radius = "9px",
                       width = "20%",
                       margin = "4px",
                       padding = "30px",
                       align="end",
                       background = "linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                       ),),
                rx.cond((correctOutputState.is_correct == False) & (correctOutputState.button_click == True),
                        action_bar()
                        ),
                rx.box(
                    rx.image(src = "/dino.png",
                            width = "300px",
                            height = "auto"),
                       style = style.dino_style
                       ),
                align = "stretch",
                width = "100%"
            ),

            bg = "linear-gradient(#048C7F, #8A9EBE)",
            width="100%",
            height="100vh",
            display="flex",
            direction = "column",
            align_items="center",
            justify_content="center",
            padding="8%",
            overflow="hidden"
        ))

    )


app = rx.App(
stylesheets=[
        "https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap"
    ],
)
app.add_page(index)

