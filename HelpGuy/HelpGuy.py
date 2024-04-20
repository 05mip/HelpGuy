"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

from HelpGuy import style

class State(rx.State):
    message = ''
    def assign_message(self, message):
        self.message = message


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Ask a question",

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
        ),
        justify = 'center'
    )


def index() -> rx.Component:

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
            padding_top = "4em"
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
                align = 'center'),
                align = 'end', 
                justify = 'end', 
                padding_top = "18em"
            ),
            direction = 'column',
            background_image = "url('https://media.discordapp.net/attachments/1230238647618371665/1231197092656185415/image.png?ex=663614a5&is=66239fa5&hm=5217e91f091d2ab13c5e6d6a723dec685b9215c07f2f517f1fef9bea318b5952&=&format=webp&quality=lossless&width=1554&height=978')",
            height="100vh",
            background_size = "cover",
    )

app = rx.App()
app.add_page(index)

