##DEMO: [link](https://mattho3-tortoise-qa-streamlit-demo-rot6fs.streamlit.app/)
## Inspiration
As student ourselves, we know how overwhelming and stressful final exams can be. We often found ourselves and others feeling anxious and overwhelmed, unsure of how to effectively study and retain all the information we needed to know. This inspired us to create Tortoise, a tutoring app that offers a patient and methodical approach to learning. With Tortoise, students can take their time and learn at their own pace, allowing them to feel more confident and prepared for their exams. We believe that by offering a personalized and relaxed approach to learning, Tortoise can help students reduce their stress and feel more prepared for their exams.

## What it does
Streamlit demo:
The app has two main components: a chat feature and a notes area. The chat feature uses AssemblyAI to allow users to interact with the tutor in real-time, asking questions and receiving answers in a natural and conversational manner. The conversation in the chat is also added to the notes area, so that users can review and revisit important information later on. The notes area only supports text, allowing users to take and organize notes in a simple and straightforward manner.

CLI demo:
We also developed a feature that unfortunately didn't make it into the Streamlit demo. The idea was to allow users to upload their textbook, so that the tutor could provide help on topics sourced from their class materials. We thought this would be a more appealing feature for a wider range of students, as it would provide personalized and relevant help based on their specific course materials. However, due to time constraints, we were unable to include this feature in the demo.

## How we built it
We built this app using a combination of Python for the backend and the Streamlit library for the frontend. For the chat feature in the Streamlit demo, we used Cohere's open-source grounded QA bot [link](https://github.com/cohere-ai/sandbox-grounded-qa). We utilized many of Streamlit's options to add various features to the frontend, including Assembly AI's real-time transcription to make the chat interactive. Overall, the use of these technologies allowed us to create a versatile and user-friendly app.

## Challenges we ran into
Cohere: In order to use Cohere's generate function, the text to be summarized must be limited to 2048 tokens, including prompts. Since summaries typically require many more tokens, we had to perform some preprocessing on the input text to ensure it meets the requirements of Cohere's generate function.

AssemblyAI: As neither of us had experience working with audio, we faced a steep learning curve when it came to incorporating audio into our product. Initially, we considered using .wav files, but ultimately decided that real-time transcription would be a better fit for our project because it would require less user input.

Streamlit: Although Streamlit made it easy to create a user-friendly front-end, we wanted something that offered more customization options. In particular, we wanted to incorporate highlighted input from the user for a more interactive experience. However, after spending an hour trying to implement this feature, we decided to move on to other features instead.

## Accomplishments that we're proud of
We enjoyed the challenge of incorporating audio into our product, and believe that the potential interactions between its components make it unique. We have also become attached to the project and want to continue developing it in order to make it a useful tool for other people. By continuing to work on the project, we hope to expand its capabilities and improve its functionality, ultimately making it a valuable resource for learners.

## What we learned
Participating in the hackathon allowed us to gain experience using large language models for a variety of tasks. This gave us a better understanding of how to leverage these models for interesting product features. We also gained proficiency in using various APIs, as our goal was to create a complete and functional product. The hackathon experience also taught us about the challenges of working with large language models, such as controlling their output and getting them to do our bidding. Overall, the hackathon was a valuable learning experience that helped us develop our skills and knowledge in this area.

## What's next for Tortoise
In order to improve the app, we plan to implement the following changes:
- Build a proper front-end using React
- Enhance the bot's conversational capabilities by using more of Assembly AI's features, including the ability to return verbal responses to the user
- Fully incorporate the summary feature by properly training language models
- Add more processing capabilities to the notes section, allowing it to be more than just a log of the chat
- Implement interactive highlighting, which will allow the user to more clearly express their learning goals and needs to the AI
- Develop the AI's ability to generate additional topics for discussion and learning.
