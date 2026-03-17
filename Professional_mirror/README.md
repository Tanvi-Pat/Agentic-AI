Professional digital mirror

This is a Personal Digital Twin that learns about your professional career by reading your LinkedIn profile and a summary file from the "me" folder. The summary includes your introduction, detailed project descriptions, and answers to common behavioral questions like "Describe an Initiative, Challenge, or Negotiation."

It launches a chatbot through a Gradio interface, powered by the OpenAI library, that can answer any professional questions asked about you. If a question comes up that isn't covered in your LinkedIn profile or summary file, it automatically sends you a text message via Pushover to keep you in the loop.

Under the hood, it essentially works as a RAG (Retrieval-Augmented Generation) system, retrieving the most relevant information from your personal knowledge base before generating a response.