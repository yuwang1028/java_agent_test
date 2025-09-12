from vertexai import init
from vertexai.preview.generative_models import GenerativeModel

init(project="gemini-test-0925", location="us-central1")
model = GenerativeModel("gemini-2.5-pro")
resp = model.generate_content("Hello from Vertex AI")
print(resp.text)
