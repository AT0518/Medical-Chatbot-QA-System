from google import genai

client = genai.Client(api_key="AQ.Ab8RN6LOPz2rTaClzhUKemgMReYOes1ccUNwKRah3BmELxl8rw")\
    
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

    