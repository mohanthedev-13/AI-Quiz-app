import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@st.cache_data
def fetch_questions(text_content, quiz_level):
    RESPONSE_JSON = {
        "mcqs": [
            {
                "mcq": "multiple choice question1",
                "options": {
                    "a": "choice here1",
                    "b": "choice here2",
                    "c": "choice here3",
                    "d": "choice here4",
                },
                "correct": "correct choice option in the form of a, b, c or d",
            },
            {
                "mcq": "multiple choice question",
                "options": {
                    "a": "choice here",
                    "b": "choice here",
                    "c": "choice here",
                    "d": "choice here",
                },
                "correct": "correct choice option in the form of a, b, c or d",
            }
        ]
    }

    PROMPT_TEMPLATE = """
    Text: {text_content}
    You are an expert in generating MCQ type quiz on the basis of provided content. 
    Given the above text, create a quiz of 5 multiple choice questions keeping difficulty level as {quiz_level}. 
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide.
    Ensure to make an array of 5 MCQs referring the following response json.
    Here is the RESPONSE_JSON: 

    {RESPONSE_JSON}
    """

    formatted_template = PROMPT_TEMPLATE.format(text_content=text_content, quiz_level=quiz_level,RESPONSE_JSON=RESPONSE_JSON)
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "TEXT:\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\n\nSome high-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); interacting via human speech (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT, and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go). However, many AI applications are not perceived as AI: \"A lot of cutting edge AI has filtered into general applications, often without being called AI because once something becomes useful enough and common enough it's not labeled AI anymore.\"[2][3]\n\nThe various subfields of AI research are centered around particular goals and the use of particular tools. The traditional goals of AI research include reasoning, knowledge representation, planning, learning, natural language processing, perception, and support for robotics.[a] General intelligence—the ability to complete any task performable by a human on an at least equal level—is among the field's long-term goals.[4] To reach these goals, AI researchers have adapted and integrated a wide range of techniques, including search and mathematical optimization, formal logic, artificial neural networks, and methods based on statistics, operations research, and economics.[b] AI also draws upon psychology, linguistics, philosophy, neuroscience, and other fields.[5]\n\nYou are an expert in generating MCQ type quiz on the basis of provided content. \n    Given the above text, create a quiz of 3 multiple choice questions keeping difficulty level as {quiz_level}. \n    Make sure the questions are not repeated and check all the questions to be conforming the text as well.\n    Make sure to format your response like RESPONSE_JSON below and use it as a guide.\n    Ensure to make an array of 3 MCQs referring the following response json.\n    Here is the RESPONSE_JSON: \n{\"mcqs\": [\n            {\n                \"mcq\": \"multiple choice question1\",\n                \"options\": {\n                    \"a\": \"choice here1\",\n                    \"b\": \"choice here2\",\n                    \"c\": \"choice here3\",\n                    \"d\": \"choice here4\",\n                },\n                \"correct\": \"correct choice option in the form of a, b, c or d\",\n            },\n            {\n                \"mcq\": \"multiple choice question\",\n                \"options\": {\n                    \"a\": \"choice here\",\n                    \"b\": \"choice here\",\n                    \"c\": \"choice here\",\n                    \"d\": \"choice here\",\n                },\n                \"correct\": \"correct choice option in the form of a, b, c or d\",\n            },\n            {\n                \"mcq\": \"multiple choice question\",\n                \"options\": {\n                    \"a\": \"choice here\",\n                    \"b\": \"choice here\",\n                    \"c\": \"choice here\",\n                    \"d\": \"choice here\",\n                },\n                \"correct\": \"correct choice option in the form of a, b, c or d\",\n            }\n        ]\n}",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```json\n{\"mcqs\": [{\"mcq\": \"What is the broad definition of Artificial Intelligence (AI)?\", \"options\": {\"a\": \"Intelligence demonstrated by animals and humans.\", \"b\": \"Intelligence displayed by machines, especially computer systems.\", \"c\": \"The study of human intelligence and behavior.\", \"d\": \"The development of advanced computer hardware.\"}, \"correct\": \"b\"}, {\"mcq\": \"Which of the following is NOT mentioned as a high-profile application of AI in the text?\", \"options\": {\"a\": \"Advanced web search engines like Google Search.\", \"b\": \"Recommendation systems used by platforms like YouTube and Netflix.\", \"c\": \"Developing new medical treatments and cures.\", \"d\": \"Generative and creative tools like ChatGPT and AI art.\"}, \"correct\": \"c\"}, {\"mcq\": \"What is considered a long-term goal in the field of AI research?\", \"options\": {\"a\": \"Creating AI that can perform specific tasks better than humans.\", \"b\": \"Developing AI that can play strategic games like chess and Go.\", \"c\": \"Achieving general intelligence, enabling AI to complete any task a human can.\", \"d\": \"Improving the efficiency of existing AI algorithms.\"}, \"correct\": \"c\"}]}\n```",
                ],
            },
        ]
    )

    # Make API request
    response = chat_session.send_message(formatted_template)

    # print(response.text)

    # Extract response JSON
    extracted_response = response.text

    # print(extracted_response)

    return json.loads(extracted_response).get("mcqs", [])


def main():
    st.title("Quiz Generator App")

    # Text input for user to paste content
    text_content = st.text_area("Paste the text content here:")

    # Dropdown for selecting quiz level
    quiz_level = st.selectbox("Select quiz level:", ["Easy", "Medium", "Hard"])

    # Convert quiz level to lower casing
    quiz_level_lower = quiz_level.lower()

    # Initialize session_state
    session_state = st.session_state

    # Check if quiz_generated flag exists in session_state, if not initialize it
    if 'quiz_generated' not in session_state:
        session_state.quiz_generated = False

    # Track if Generate Quiz button is clicked
    if not session_state.quiz_generated:
        session_state.quiz_generated = st.button("Generate Quiz")

    if session_state.quiz_generated:
        # Define questions and options
        questions = fetch_questions(text_content=text_content, quiz_level=quiz_level_lower)

        # Display questions and radio buttons
        selected_options = []
        correct_answers = []
        for question in questions:
            options = list(question["options"].values())
            selected_option = st.radio(question["mcq"], options, index=None)
            selected_options.append(selected_option)
            correct_answers.append(question["options"][question["correct"]])

        # Submit button
        if st.button("Submit"):
            # Display selected options
            marks = 0
            st.header("Quiz Result:")
            for i, question in enumerate(questions):
                selected_option = selected_options[i]
                correct_option = correct_answers[i]
                st.subheader(f"{question['mcq']}")
                st.write(f"You selected: {selected_option}")
                st.write(f"Correct answer: {correct_option}")
                if selected_option == correct_option:
                    marks += 1
            st.subheader(f"You scored {marks} out of {len(questions)}")


if __name__ == "__main__":
    main()