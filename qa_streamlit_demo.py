import streamlit as st
from streamlit_chat import message as st_message
import streamlit.components.v1 as components
import random
import string
import websockets
import asyncio
import base64
import json
import pyaudio
from qa.bot import GroundedQaBot

source_url = ''
iframe = None
source_display = None

if 'text' not in st.session_state:
	st.session_state['text'] = ""
	st.session_state['run'] = False

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

def start_listening():
	st.session_state['run'] = True

async def send_receive():
	
	print(f'Connecting websocket to url ${URL}')

	async with websockets.connect(
		URL,
		extra_headers=(("Authorization", st.secrets["assembly_api_key"]),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		r = await asyncio.sleep(0.1)
		print("Receiving SessionBegins ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")


		async def send():
			while st.session_state['run']:
				try:
					data = stream.read(FRAMES_PER_BUFFER)
					data = base64.b64encode(data).decode("utf-8")
					json_data = json.dumps({"audio_data":str(data)})
					r = await _ws.send(json_data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"

				r = await asyncio.sleep(0.01)


		async def receive():
			while st.session_state['run']:
				try:
					result_str = await _ws.recv()
					result = json.loads(result_str)['text']

					if json.loads(result_str)['message_type']=='FinalTranscript':
						# print(result)
						st.session_state['text'] += result
						print(result)
						# st.markdown(st.session_state['text'])
						st.session_state['run'] = False

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"
			
		send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())

### CHAT UPDATED HERE
def getReply():
    user_message = st.session_state.input_text
    history = []
    for chat in st.session_state['history']:
        name = "user" if chat['is_user'] else "bot"
        history.append(f"{name}: {chat['message']}")
    bot.set_chat_history(history)
    reply, source_urls, source_texts = bot.answer(user_message,
                       verbosity=2,
                       n_paragraphs=2,
                       model=st.session_state.model,
                       url=st.session_state.url)
    sources_str = "\n".join(list(set(source_urls))) + '\n'
    reply_incl_sources=f"{reply}\nSource:\n{sources_str}"
    # print(reply_incl_sources)
    st.session_state.links += (sources_str)

    st.session_state.input_text = ''
    st.session_state.history.append({"message": user_message, "is_user": True, "avatar_style": "gridy"})
    st.session_state.history.append({"message": reply, "is_user": False})
    # st.session_state.sources.extend(sources_str)
    st.session_state['notes'] += user_message + "\n\t" + reply + '\n'


if __name__ == "__main__":
    print("new bot")
    bot = GroundedQaBot(st.secrets["cohere_api_token"], st.secrets["serp_api_key"])

    st.set_page_config(layout="wide")

    ### CHAT HISTORY SETUP
    if "history" not in st.session_state:
        st.session_state.history = []
        st.session_state.notes = ""
    if "links" not in st.session_state:
        st.session_state.links = ""

    ### MAIN PAGE LAYOUT
    col1, col2 = st.columns(2)
    with st.sidebar:
        st.title("Tutor")
        st.markdown('This is a Assembly API / Cohere API / Serp API powered contextualized tutor bot!')
        #used for any extra settings
        with st.expander("Advanced Settings"):
            st.text_input("Restrict replies to domain:", key="url", placeholder="Ex: shopify.com")
            st.selectbox('Model:', ('xlarge', 'command-xlarge-20221108'), key="model")
    # notes
    with col1:
        # Create a text area with the label "Enter some text" and the default text "Hello, Streamlit!"
        st.subheader("Notes")

        notes = st.text_area('Enter some text', value=st.session_state['notes'], height=500)
        st.session_state['notes'] = notes

        st.subheader("Sources")
        st.markdown(st.session_state.links)

    #chat
    with col2:
        for chat in st.session_state['history']:
            # call random.choices() string module to find the string in Uppercase + numeric data.
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            st_message(**chat, key=ran)  # laying out messages
        # print(st.session_state['history'])
        st.text_input("",
                      key="input_text",
                      value=st.session_state['text'],
                      on_change=getReply,
                      placeholder="Ask me a question...like 'how far away is the moon'")
        record_start = st.button("Record",on_click=start_listening)
        download_notes_csv = st.session_state['notes']
        download_notes_csv = download_notes_csv.replace("\n\t", ",")
        st.download_button('Download', download_notes_csv)
