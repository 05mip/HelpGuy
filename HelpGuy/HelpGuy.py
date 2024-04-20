"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx


class State(rx.State):
    """The app state."""

class TextfieldControlled(rx.State):
    text: str = "Hello World!"


def index() -> rx.Component:
    return rx.center(
        rx.input.root(
            rx.input.slot(
                rx.icon(tag="search"),
            ),
            rx.input.input(
                placeholder="Hello World",
                size=3,
            ),
            
        ),
        height="100vh",
        
    )


app = rx.App()
app.add_page(index)
