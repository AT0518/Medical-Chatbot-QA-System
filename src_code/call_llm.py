from google import genai

client = genai.Client(api_key="AQ.Ab8RN6J1x14g5uAjkCVymlin9-y_NoGwiiLXPI6pzwdtnnOwLw")\
    
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

    