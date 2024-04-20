"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""


class TextfieldBlur(rx.State):
    text: str = ""


def blur_example() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Search here...",
            on_blur=TextfieldBlur.set_text,
            width="50vw",
            height="5vh",
        ),
    )


def search_button() -> rx.Component:
    return rx.button(
        ("\u2315"),
        height="5vh",
        font_size="30px"
    )


def dino() -> rx.Component:
    return rx.image(
        src="https://media.discordapp.net/attachments/1230238647618371665/1231229218784936057/dino_cliff_2.png?ex=66363290&is=6623bd90&hm=c455234ce0fe0ad820225cfe17fbd7ffe50826af25a31f262b555b5999bc716b&=&format=webp&quality=lossless&width=978&height=978",
        width="20vw",
        height="auto",
    )


def index() -> rx.Component:
    return rx.vstack(
        dino(),
        rx.center(
            blur_example(),
            search_button(),
        ),
        padding_top="15vh",
        align="center",
        height="100vh",
        background_image="url('https://media.discordapp.net/attachments/1230238647618371665/1231197092656185415/image.png?ex=663614a5&is=66239fa5&hm=5217e91f091d2ab13c5e6d6a723dec685b9215c07f2f517f1fef9bea318b5952&=&format=webp&quality=lossless&width=1554&height=978')",
        background_size="cover",
    )


app = rx.App()
app.add_page(index)