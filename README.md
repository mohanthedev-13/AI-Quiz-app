# AI-Quiz-app
A Quiz Generator Application built with Python, Streamlit, and Gemini AI provides an efficient platform to create quizzes dynamically. It uses AI to generate various question types (MCQs, True/False, short answer) based on user-input topics or text. 

## Getting Started
### Prerequisites
Ensure you have the following installed:

` Python 3.8 or higher `

` pip (Python package manager) `

### Installation
Clone this repository:

``` 
git clone https://github.com/mohanthedev-13/AI-Quiz-app.git
cd AI-Quiz-app
```

Install the required dependencies:

```
pip install -r requirements.txt
```
### How to Run a sample response from quiz generator without authentication
Start the Streamlit application:

```
streamlit run sample.py
```
Open your web browser and navigate to the URL displayed in the terminal (default is http://localhost:8501).

### To run Full application 
Start the Streamlit application:

```
streamlit run quizapp.py
```
Open your web browser and navigate to the URL displayed in the terminal (default is http://localhost:8501).

## To integrate Gemini AI:

Obtain an API key from Gemini AI (if required).
Add the key to the application configuration:
Create a .env file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
```
