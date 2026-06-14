from groq import Groq                           # GROQ client
from config import API_KEY, CATEGORIES          # the api key + valid category list

def get_category(text):
    # Groq client created using the API key from config
    client = Groq(api_key=API_KEY)

    # build the prompt - precision here controls Groq's output
    prompt = f"""You are an invoice categoriser.
    Read the invoice text below.
    Reply with ONE word only - no explanation, no punctuation.
    Choose from: electricity, food, rent, internet, miscellaneous
    
    Invoice Text:
    {text}"""

    try:
        # send prompt to Groq and get response
        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = [
                {"role": "user", "content": prompt}
            ],
            max_tokens = 10,
            temperature = 0
        )

        # clean the response - remove whitespace and lowercase it
        category = response.choices[0].message.content.strip().lower()
        
        # validate - if Groq said something unexpected, fall back safely
        if category not in CATEGORIES:
            print(f"Unexpected response: {category} - defaulting to miscellaneous")
            return "miscellaneous"
        
        return category # valid category - return it
    
    except Exception as e:
        # any error (network, qouta, timeout) - fall back, never crash
        print(f"Groq error: {e}")
        return "miscellaneous"
    
if __name__ == "__main__":
    # test sameples - simulating what pdfplumber would extract
    test_samples = [
        ("electricity test", "MSEDCL Electricity Bill\nTotal Amount Due: Rs. 2,156\nBilling Period: January 2026"),
        ("food test", "Swiggy Order Invoice\nPaneer Butter Masala x1\nTotal Paid: Rs. 535"),
        ("rent test", "Rent receipt\nLandlord: Ramesh Patil\nMonthly Rent: Rs. 8,000"),
    ]

    for label, sample_text in test_samples:
        print(f"\nTest: {label}")
        print(f"\nInput Preview: {sample_text[:60]}...")
        result = get_category(sample_text)                  # call the function
        print(f"Category returned: {result}")