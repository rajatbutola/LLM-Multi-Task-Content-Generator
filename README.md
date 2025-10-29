#  LLM Multitask Content Genertor

It is a personal open source project that leverages a Large Language Model (LLM) to automate several text-based tasks. With this tool, you can easily generate blog posts, summarize text, and compose professional emails. The project is designed to make content creation and text management more efficient by automating common tasks.

-  **Query preprocessing** – the question is cleaned and converted into an embedding.
-  **Document retrieval** – FAISS searches for the most relevant leaflet chunks.
-  **Prompt construction** – the retrieved passages are combined with a strict bilingual answer template.
-  **LLM generation** – TinyLlama uses this context to produce a grounded response, constrained to the evidence it was given.
-  **Bilingual output** – the final answer is presented in English and Traditional Chinese, with source citations.

By combining lightweight LLM inference with retrieval from vetted medical texts, the chatbot balances interpretability, privacy (runs fully on-premise), and accessibility, making it a practical tool for patient education in clinical settings such as hospitals or waiting rooms.

---

##  Features
-  **Blog Generation**: Automatically generate blog posts based on a provided topic, keywords, and tone.  
-  **Text Summarization**: Condense long articles, reports, or documents into clear and concise summaries.  
-  **Email Generation**: Compose structured leave request emails with customizable fields like recipient name, reason, dates, and more.

##  Requirements

- Python 3.8 or higher
- PyTorch
- Hugging Face's transformers library
- Flask
- CUDA (Optional, for GPU support)


##  Installation

To set up the project locally, follow these steps:

### 1. Clone the repo
```bash
git clone https://github.com/rajatbutola/LLM-Multi-Task-Content-Generator
cd LLM-Multi-Task-Content-Generator
```
### 2. Create and activate a virtual environment:
```bash
python -m venv llmenv
source llmenv/bin/activate   # Linux/Mac
.\llmenv\Scripts\activate    # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Download Pre-trained Models:
The project uses Hugging Face's pre-trained models. The models will automatically download when you run the app, so make sure you have an internet connection.

## Usage

To run the web app locally:

### 1. Start the Flask app:
```bash
python app.py
```
### 2. Open a web browser and go to http://127.0.0.1:5000/. You should see the home page of the application.

### 3. Generate Tasks:

- **Blog Post**: Select "Blog" as the task, then enter the topic, keywords, and tone.
- **Summary**: Paste the text you want to summarize and click "Generate Summary".
- **Email**: Fill out the fields for a leave request email, including recipient, reason, dates, and any handover information.


## API Endpoints

The web app provides a simple form-based interface for interacting with the model. The underlying functions used to generate text are:

### 1. Generate Blog Post:

- Inputs: Topic, Keywords (optional), Tone

- Output: A generated blog post based on the provided inputs.

### 2. Generate Summary:

- Inputs: Text (full text to be summarized)

- Output: A concise summary of the provided text.

### 3. Generate Email:

- Inputs: Subject, Tone, Recipient Name, Reason, Start Date, Duration, Return Date, Handover Details

- Output: A professionally structured leave request email.

## Model Details

### 1. Blog Generation:

- Model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Tokenizer: TinyLlama

### 2. Text Summarization:

- Model: google/flan-t5-small
- Tokenizer: flan-t5-small

### 3. Email Generation:

- Model: google/flan-t5-base
- Tokenizer: flan-t5-base

The models used in this project are pre-trained from Hugging Face, and the app utilizes the ```bash transformers ``` library to load and interact with them.

## Code Overview

- model.py: Contains the model loading, tokenization, and text generation functions for blog posts, summaries, and emails.

- app.py: The Flask web app that handles requests and displays the generated content.

index.html: The HTML page for the main interface of the app.

result.html: The HTML page used to display the generated results.

## GUI screenshots

<img width="1440" height="900" alt="1" src="https://github.com/user-attachments/assets/e0fffba6-e725-41bd-9922-8cd7feee0129" />
<img width="1440" height="900" alt="2" src="https://github.com/user-attachments/assets/c76132af-09d9-45a2-8efc-2c149ae3d33b" />
<img width="1440" height="900" alt="3" src="https://github.com/user-attachments/assets/33b0e44a-5ac8-4d00-888a-7975c68b5454" />
<img width="1440" height="900" alt="4" src="https://github.com/user-attachments/assets/1ecfb1e1-c6e7-4ef6-bf52-e592fd14d98e" />
<img width="1440" height="900" alt="5" src="https://github.com/user-attachments/assets/bc484322-9cc7-422a-9e6d-cd2ece682c5d" />
<img width="1440" height="900" alt="6" src="https://github.com/user-attachments/assets/eb45c562-f2e3-4421-afbd-8bd3aeb43c19" />
<img width="1440" height="900" alt="7" src="https://github.com/user-attachments/assets/40a1b2d3-a8c4-4fa1-968d-21b6554be4d4" />
<img width="1440" height="900" alt="8" src="https://github.com/user-attachments/assets/3191ea4b-2d30-4375-95e0-39fed52c5ad3" />



## Contribution

Contributions are welcome! If you'd like to improve or add features to the project, feel free to open an issue or submit a pull request. Here are some ways you can contribute:

Add new features (e.g., new tasks or additional models)

Fix bugs or improve performance

Update documentation or enhance the user interface
