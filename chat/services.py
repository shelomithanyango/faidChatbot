from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

FIRST_AID_INSTRUCTIONS = {
    "burns": "1. Cool the burn under running water for 10–20 minutes.\n2. Remove tight items like rings.\n3. Cover with a clean cloth or sterile dressing.\n4. Do NOT apply ice or butter.\n5. Seek medical help if severe.",
    "cpr": "1. Check responsiveness and breathing.\n2. Call emergency services if no response.\n3. Place hands in the center of the chest.\n4. Perform 30 chest compressions at 100–120 per minute.\n5. Give 2 rescue breaths, then continue cycles of 30:2.\n6. Continue until help arrives or the person shows signs of life.",
    "choking": "1. Encourage coughing if conscious.\n2. Perform Heimlich maneuver if choking persists.\n3. Call emergency services if person becomes unconscious.",
    "bleeding": "1. Apply pressure to the wound.\n2. Elevate the injured part if possible.\n3. Clean and bandage the wound.\n4. Seek medical help for severe bleeding.",
    "fractures": "1. Immobilize the limb.\n2. Apply a splint if trained.\n3. Avoid moving the person unnecessarily.\n4. Seek professional medical help.",
    "fainting": "1. Lay the person on their back.\n2. Elevate legs above heart level.\n3. Loosen tight clothing.\n4. Keep them cool and comfortable.\n5. If unconscious for more than a minute, call emergency services.",
    "sprains": "1. Rest the injured limb.\n2. Apply ice for 15–20 minutes every 2-3 hours.\n3. Compress with an elastic bandage.\n4. Elevate above heart level.\n5. Seek medical attention if severe.",
    "nosebleed": "1. Sit upright and lean slightly forward.\n2. Pinch the soft part of the nose for 10 minutes.\n3. Apply a cold compress to the nose.\n4. Seek medical help if bleeding persists.",
    "cuts": "1. Clean the wound with water.\n2. Apply antiseptic.\n3. Cover with a sterile bandage.\n4. Watch for signs of infection.",
    "suffocation": "1. Call emergency services immediately.\n2. If trained, perform rescue breathing.\n3. If the person is unconscious, place them in the recovery position.\n4. Continue until help arrives.",
}

def get_chatbot_stream(user_message):
    key = user_message.strip().lower()
    
    # 1. If it's a predefined hardcoded local keyword, yield it instantly as a single chunk
    if key in FIRST_AID_INSTRUCTIONS:
        yield FIRST_AID_INSTRUCTIONS[key]
        return

    # 2. Otherwise, fetch live streaming tokens from Gemini 2.5 Flash
    try:
        response_stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=f"""
You are a first aid assistant. 
Provide instructions for: {user_message}
Format your answer in short numbered steps. 
Be brief and concise, maximum 5 steps.
"""
        )
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        print("🔥 GEMINI ERROR:", e)
        yield "Sorry, something went wrong while generating instructions. Please try again."
