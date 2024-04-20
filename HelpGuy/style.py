import reflex as rx

# Common styles for questions and answers.
shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
#WIDTH: list[str] = ['90%', '80%', '70%', '65%', '55%']
chat_margin = "20%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)



# Styles for the action bar.
input_style = dict(
   border_width="2px",
    padding="0.5em",
    box_shadow=shadow,
    width="350px",
    height="70px",

)

stack = dict(
    #width="100%",
    align_items="center",
    justify_content="center",
    display="flex",
    padding_top="4em"
)
button_style = dict(
    background_color=rx.color("accent", 10),
    box_shadow=shadow,
)