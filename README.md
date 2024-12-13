# skin-care-assistant
AI-powered personalized skincare assistant providing tailored product recommendations and routines using LlamaIndex, RAG, and GPT integration.

### Steps to setup

1. Have a working open ai key. Goto https://platform.openai.com/api-keys and ensure a project key with a valid, positive usage limit has been setup.
2. Create an account on ngrok. Then headover to https://dashboard.ngrok.com/get-started/your-authtoken to get the ngrok auth token
3. Replace your_open_ai_api_key with the OpenAI api key everywhere. Replace your_ngrok_token_here with the actual ngrok token.
4. Before running the colab notebook:
	a. Switch the runtime environment to GPU T4.
	b. Upload the skincare_knowledge_base.zip file on the root level of uploads
	c. Upload the templates and static folder. These will be needed for running the flask web application
5. Run all the cells. Visit the public URL generated in the last cell.