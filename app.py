import gradio as gr
import openai

import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("openai_api_key")

history = []
character_name = "AI"
chat_history = []

def openai_chat(prompt):
    print("buda prompt", prompt)
    history.append({"role": "user", "content": prompt})
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        max_tokens=150,
        temperature=0.6,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.0 
    )
    print(response.choices[0].message["content"].strip())
    return  response.choices[0].message["content"].strip()
    

# def character_selection(prompt_input):
#     history.append(prompt_input)
    
def set_character_name(prompt_input):
    print(prompt_input)
    character_name = prompt_input
    history.append({"role": "system", "content": f"You are {character_name}. You will talk and think like {character_name} from now on."})
  
    return {msg: msg.update(visible=True), chatbot: chatbot.update(visible=True), char_selection : char_selection.update(visible=False), title: title.update( value = f"Chat with {character_name.upper()}",visible=True)}
    
def respond(message):
    bot_message = openai_chat(message)
    history.append({"role": "assistant", "content": bot_message})
    chat_history.append((message, bot_message))
    return {msg: msg.update(value="", visible=True), chatbot: chatbot.update(value= chat_history,visible=True)}


with gr.Blocks() as demo:
    char_selection = gr.Textbox(lines=1 , label="Enter the character you want to talk to:")
    title = gr.Markdown( visible=False)
    chatbot = gr.Chatbot(visible=False)
    msg = gr.Textbox(visible=False)
    
    char_selection.submit(set_character_name, char_selection, [chatbot, msg, char_selection, title])
    
    msg.submit(respond, msg, [chatbot, msg])
        


demo.launch(share= True)
