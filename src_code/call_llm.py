from google import genai

client = genai.Client(api_key="AQ.Ab8RN6I5VsRVMIwrTPF-_hQhyaCo-imRd0rGK4dFVVzJKo7Gaw")
    
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

    