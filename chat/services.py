from google import genai
from django.conf import settings

api_key = genai.Client(api_key=settings.GEMINI_API_KEY)

# First aid instructions dictionary
FIRST_AID_INSTRUCTIONS = {
    "burns": "1. Cool the burn under running water for 10–20 minutes.\n2. Remove tight items like rings.\n3. Cover with a clean cloth or sterile dressing.\n4. Do NOT apply ice or butter.\n5. Seek medical help if severe.",
    "cpr": "1. Check responsiveness and breathing.\n2. Call emergency services if no response.\n3. Place hands in the center of the chest.\n4. Perform 30 chest compressions at 100–120 per minute.\n5. Give 2 rescue breaths, then continue cycles of 30:2.\n6. Continue until help arrives or the person shows signs of life.",
    "choking": "1. Encourage coughing if conscious.\n2. Perform Heimlich maneuver if choking persists.\n3. Call emergency services if person becomes unconscious.",
    "bleeding": "1. Apply pressure to the wound.\n2. Elevate the injured part if possible.\n3. Clean and bandage the wound.\n4. Seek medical help for severe bleeding.",
    "fractures": "1. Immobilize the limb.\n2. Apply a splint if trained.\n3. Avoid moving the person unnecessarily.\n4. Seek professional medical help.",
    "fainting": "1. Lay the person on their back.\n2. Elevate legs above heart level.\n3. Loosen tight clothing.\n4. Keep them cool and comfortable.\n5. If unconscious for more than a minute, call emergency services.",
    "sprains": "1. Rest the injured limb.\n2. Apply ice for 15–20 minutes every 2-3 hours.\n3. Compress with an elastic bandage.\n4. Elevate above heart level.\n5. Seek medical attention if severe.",
    "nosebleed": "1. Sit upright and lean slightly forward.\n2. Pinch the soft part of the nose for 10 minutes.\n3. Apply a cold compress to the nose.\n4. Seek medical help if bleeding persists.",
    "cuts": "1. Clean the wound with water.\n2. Apply antiseptic.\n3. Cover with a sterile bandage.\n4. Watch for signs of infection."
}

def get_chatbot_response(user_message):
    key = user_message.strip().lower()
    
    # 1️⃣ Check if user typed a known first aid topic
    if key in FIRST_AID_INSTRUCTIONS:
        return FIRST_AID_INSTRUCTIONS[key]

    # 2️⃣ Otherwise, fallback to Gemini AI
    try:
        response = api_key.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        return response.text.strip()

    except Exception as e:
        print("🔥 GEMINI ERROR:", e)
        # 3️⃣ If Gemini fails, provide polite fallback
        return (
            "Sorry, I only provide first aid instructions right now. "
            
        )