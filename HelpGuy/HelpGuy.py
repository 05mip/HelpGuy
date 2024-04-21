"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import json
import reflex as rx
import time
import plotly as go
import requests

from HelpGuy import style

ENDPOINT_LINK_PRE = "http://127.0.0.1:5000/search?q="


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
    response = ""
    processing = False
    complete = False
    causes_dict = {}
    recov_time = ''
    treatments = []
    summary = ''
    pielist: list[dict]= []

    async def process_output(self):
        """Get the output from the prompt."""
        outputState = await self.get_state(correctOutputState)
        outputState.is_correct = False
        outputState.button_click = False
        self.causes_dict = {}
        self.recov_time = ''
        self.treatments = []
        self.summary = ''
        self.pielist: list[dict]= []
        
        if self.prompt == "":
            yield rx.window_alert("Prompt Empty")
        else:
            self.processing = True
            yield
        print(f'{self.processing} should set processing here')

        time.sleep(2)

        self.response = self.get_endpoint()
        print(self.response)
        if self.response == None:
            yield rx.window_alert("Error Occured Loading Data")
        
        self.data_filter()
        self.portion_to_int()

        self.complete = True
        self.processing = False
        if self.complete:
            print("should change to another page")
            yield rx.redirect("/results")
        
    def reset_state(self):
        self.processing = False
        self.complete = False
        self.prompt = ''
        
    def data_filter(self):
        in_causes = True
        lines = self.response.split('\n')
        dash_front = lines[0].strip().startswith('-')

        for line in self.response.split('\n')[:-1]:
            if "stimate" in line:
                in_causes = False
                self.recov_time = line[line.index('-')+1:]
                continue
            if in_causes:
                prop = line.split('-')[-1]
                cause = '-'.join(line.split('-')[int(dash_front):-1]).strip()
                self.causes_dict[cause] = prop
            else:
                if len(line) < 3 or "ummary" in line:
                    break
                self.treatments.append(''.join(line.strip('-')[int(dash_front):]).strip())
                    
        self.summary = self.response.split('\n')[-1]
        if len(self.treatments) > 4:
            self.treatments = self.treatments[:4]
        
        print("RESULTS")
        print(self.causes_dict)
        print(self.recov_time)
        print(self.treatments)
        print(self.summary)
    
    def portion_to_int(self):
        for k, v in self.causes_dict.items():
            if v.strip() == '' or len(v.strip()) < 2:
                del self.causes_dict[k]
        self.pielist = sorted([{"name": key, "value": int(value.strip()[:-1])} 
             for key, value in self.causes_dict.items()], key= lambda x: x['value'])
        
    def set_text(self, new_text):
        self.prompt = new_text

    def get_endpoint(self):
        url = ENDPOINT_LINK_PRE + self.prompt
        try:
            response = requests.get(url)
            response.raise_for_status()
            jdata = json.loads(response.text)
            response = jdata['response']
            return response
        except:
            print("UR cooked")
            return None
#####################################################################        
recovery_data = [
    {"name": "Recovery Time", "uv": 4000, "pv": 2400, "amt": 2400},
]

data01 = State.pielist
#####################################################################        

def action_bar() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Ask a question",
            value=State.prompt,
            on_change=State.set_text,
            on_blur=State.set_text,
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

@rx.page(on_load=State.reset_state)
def index() -> rx.Component:

    return rx.flex(
        rx.cond(State.processing, rx.text('')),
            rx.stack(
                rx.box(
                    rx.text("The Dino Doc",
                            font_family = "Rajdhani",
                            size='9'
                            ),
                        text_align="center",
                        font_weight="bold",
                        ),
                        action_bar(),
                        rx.cond(State.processing, rx.chakra.circular_progress(is_indeterminate=True),),
                        direction = "column",
                        align = "center",
                        justify = "center",
                    ),
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("Hello There! Enter any health related problems you've been having recently",
                                color="white"),
                        border_radius="9px",
                        width="30%",
                        margin="4px",
                        padding="30px",
                        background="linear-gradient(45deg, #6bcef8, #4a3aae)",
                        class_name = "animate-bounce",
                ),
                    rx.box(
                        rx.image(
                            src = "/dino.png",
                            width = "400px",
                            height = "auto"),
                            ),
                    align = "center"
                ),
                padding_top = "20vh",
                width = "100vw",
                align = "end",
                justify = "end",
            ),
            padding_top = "25vh",
            justify = "center",
            direction = "column",
            background_image = "url('https://media.discordapp.net/attachments/1230238647618371665/1231197092656185415/image.png?ex=663614a5&is=66239fa5&hm=5217e91f091d2ab13c5e6d6a723dec685b9215c07f2f517f1fef9bea318b5952&=&format=webp&quality=lossless&width=1554&height=978')",
            height="100vh",
            width="100vw",
            
            background_size = "cover",
        )
        

def recovery_time() -> rx.Component:
    return rx.text(State.recov_time,
                   size='8',
                   fond_family="Rajdhani",
                   padding_top="10vh",
                   align="center",
                   justify="center")

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
        width="90%",
        padding_top="1vh"
    )

def scroll_area() -> rx.Component:
    return rx.scroll_area(
        rx.flex(
            rx.heading("Summary",  font_family="Rajdhani"),
                        rx.text(State.summary),
            direction = "column",
            spacing = "4",
        ),
        type = "always",
        scrollbars = "vertical",
    )



def scroll_horizontal_area() -> rx.Component:
    return rx.grid(

        rx.foreach(
            rx.Var.range(State.treatments.length()),
            lambda i: rx.flex(rx.text(State.treatments[i])),
            
        ),
        columns=f'{State.treatments.length()}',
        spacing="2"
    )


@rx.page(route="/results", title="Results Page")
def about() -> rx.Component:
    return (
        rx.flex(rx.vstack(
            rx.hstack(
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
                                  rx.text(State.pielist[0]["name"]),
                                  width="100%",
                                  height="100px"),
                        width="40%"),
            
                    rx.card(rx.heading("Recovery Time",
                                       font_family="Rajdhani"),
                            recovery_time(),
                            width="40%",
                            height="400px"),
                   rx.card(scroll_area(), width="60%", height="400px"),

                justify = "between",
                align = "stretch",
                spacing = "4",
                width="100%",
            ),
            rx.hstack(
                rx.cond((~correctOutputState.button_click) |
                        ((correctOutputState.is_correct) & (correctOutputState.button_click)),
                        rx.card(
                            rx.heading("Treatments", font_family = "Rajdhani"),
                            scroll_horizontal_area(), width = "60%", height = "200px"),
                        ),

                # action_bar(),
                rx.cond(correctOutputState.button_click == False, 
                rx.box(
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
                       height= "auto",
                       margin = "4px",
                       padding = "30px",
                       align="end",
                       background = "linear-gradient(144deg,#AF40FF,#6bcef8 50%,#00DDEB)",
                       ),),
                rx.cond((~correctOutputState.is_correct) & (correctOutputState.button_click),
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
app.compile()
