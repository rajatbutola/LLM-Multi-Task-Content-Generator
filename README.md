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

Answer:
English: "PrEP is highly effective ..."
Mandarin: "暴露前預防性投藥（PrEP）在正確規律服用時..."
Sources:
1: cdc-prep-leaflet.pdf (chunk 0)
2: cdc-prep-guide.pdf (chunk 1)

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
[git clone https://github.com/your-username/health-education-chatbot.git](https://github.com/rajatbutola/LLM-Multi-Task-Content-Generator)
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

## Contribution

Contributions are welcome! If you'd like to improve or add features to the project, feel free to open an issue or submit a pull request. Here are some ways you can contribute:

Add new features (e.g., new tasks or additional models)

Fix bugs or improve performance

Update documentation or enhance the user interface










Start the Flask server:
```bash
python app_chat.py
```
Open http://127.0.0.1:5000 in your browser.
You can now ask questions like:

-  **“What is PrEP and how effective is it?”

<img width="943" height="783" alt="Health education chatbot 0" src="https://github.com/user-attachments/assets/345a03fe-7bac-4ae7-87a7-14bb4f7f764e" />
<img width="1058" height="840" alt="Health education chatbot 1" src="https://github.com/user-attachments/assets/cb6ff618-6ec3-4af6-9f42-ab2f66000338" />
<img width="1051" height="855" alt="Health education chatbot 2" src="https://github.com/user-attachments/assets/d63d6390-8e15-4051-a6fb-43b051247deb" />
<img width="969" height="829" alt="Health education chatbot 3" src="https://github.com/user-attachments/assets/c3853625-b6bd-45c3-8378-c0b84e77cdfd" />
<img width="960" height="821" alt="Health education chatbot 4" src="https://github.com/user-attachments/assets/6d4b063f-d7e9-4041-b91b-7abff9e347c6" />


Notes on Use

-  This chatbot is for educational purposes only.
-  It is not a diagnostic tool and should not replace medical advice.
-  Always consult healthcare professionals for personal medical concerns.

Please cite the original CDC / NHS / MOHW-HPA sources when redistributing patient education content.



