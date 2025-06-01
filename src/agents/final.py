from gpt4all import GPT4All
from scraper import scrape_team_injuries

# Step 1: scrape the data
data = scrape_team_injuries("Manchester United injuries site:whoscored.com", num_results=3)

# Step 2: Prepare a text prompt by combining URL + snippet of HTML (or you can parse to plain text if you want)
prompt = "Here is some info from web pages:\n\n"

for entry in data:
    url = entry['url']
    snippet = entry['html'][:500].replace('\n', ' ')  # first 500 chars, clean newlines
    prompt += f"URL: {url}\nContent snippet: {snippet}\n\n"

prompt += "Based on this, please summarize the current injury status of Manchester United."

# Step 3: Load model and generate response
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", model_path="../../gpt4all")

response = model.generate(prompt)
print(response)
