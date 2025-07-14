# 📄 Research Paper Chatbot Assistant

This is a powerful **AI-powered Streamlit web app** that allows you to:

✅ Upload research papers (PDFs)  
✅ Automatically extract and summarize their content  
✅ Chat with your paper to ask questions in natural language  
✅ Switch between Hindi and English  
✅ Download paper summaries  
✅ Use either Gemini API or OpenAI API for AI responses

---

## 💡 Features

- **PDF Upload & Text Extraction**
    - Upload any research paper in PDF format.
    - Automatically extracts text from all pages.

- **Smart Summarization**
    - Summarizes the paper into simple language (English or Hindi).
    - Optionally only summarizes the abstract for faster performance.

- **Conversational Chatbot**
    - Ask any question about your research paper.
    - Get answers in Hindi or English.
    - Works as a general chatbot if no paper is uploaded.

- **Download Summary**
    - Save summarized content as a text file for future reference.

- **Error Handling**
    - Handles API rate limits and errors gracefully.

- **Fast Performance**
    - Optimized summarization process for faster results.

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit** for UI
- **PyMuPDF** for PDF text extraction
- **Gemini API** (Google AI) or **OpenAI API** (ChatGPT)
- HTML/CSS for custom styling

---

## 🚀 How to Run

1. Clone this repo:

    ```bash
    git clone https://github.com/your-username/research-paper-chatbot.git
    cd research-paper-chatbot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set your API key:

    - For **Gemini API**:
        ```bash
        export GEMINI_API_KEY="your_gemini_api_key"
        ```

    - Or for **OpenAI API**:
        ```bash
        export OPENAI_API_KEY="your_openai_api_key"
        ```

4. Run the app:

    ```bash
    streamlit run app.py
    ```

---

## 🔒 Security Note

Never commit your API keys directly in code. Always use environment variables or a secrets manager.

---

## ✨ Future Improvements

- Add multilingual support beyond Hindi and English
- Deploy on cloud for public access
- Support summarization of charts, tables, and figures
- User authentication for saving chat history

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

**Built with ❤️ for research enthusiasts.**
