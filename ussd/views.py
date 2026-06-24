from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from history.models import ChatHistory


# -------------------------
# PHONE NORMALIZATION
# -------------------------
def normalize_phone(number):
    if not number:
        return None

    number = str(number).strip()

    # remove spaces just in case
    number = number.replace(" ", "")

    # already correct format
    if number.startswith("+"):
        return number

    # 2547... → +2547...
    if number.startswith("254"):
        return "+" + number

    # 07... → +2547...
    if number.startswith("0"):
        return "+254" + number[1:]

    return number


# -------------------------
# SAVE CHAT
# -------------------------
def save_chat(phone, question, response):
    try:
        ChatHistory.objects.create(
            user=None,
            phone_number=phone,
            question=question,
            response=response
        )
    except Exception as e:
        print("SAVE ERROR:", e)


# -------------------------
# USSD VIEW
# -------------------------
@csrf_exempt
def ussd_callback(request):

    if request.method != "POST":
        return HttpResponse("END Invalid request", content_type="text/plain")

    # IMPORTANT: correct key from Africa's Talking is "phoneNumber"
    raw_phone = request.POST.get("phoneNumber")

    phone_number = normalize_phone(raw_phone)

    session_id = request.POST.get("sessionId")
    text = request.POST.get("text", "").strip()

    user_response = text.split("*") if text else []

    print("RAW PHONE:", raw_phone)
    print("NORMALIZED PHONE:", phone_number)
    print("TEXT:", text)

    response = "END Something went wrong"

    # ---------------- MAIN MENU ----------------
    if len(user_response) == 0 or user_response[0] == "":
        response = (
            "CON Welcome to First Aid Chatbot\n"
            "1. First Aid Tips\n"
            "2. Emergency Numbers\n"
            "3. About"
        )

    # ---------------- FIRST AID ----------------
    elif user_response[0] == "1":

        if len(user_response) == 1:
            response = (
                "CON First Aid Tips\n"
                "1. Bleeding\n"
                "2. Burns\n"
                "3. Fractures\n"
                "4. Snakebite\n"
                "5. Choking\n"
                "6. Suffocation"
            )

        elif len(user_response) == 2:
            tips = {
                "1": "END Bleeding:\n- Apply pressure\n- Elevate limb\n- Seek help",
                "2": "END Burns:\n- Cool with water\n- Cover wound\n- Avoid creams",
                "3": "END Fractures:\n- Immobilize\n- Do not move victim\n- Go hospital",
                "4": "END Snakebite:\n- Keep calm\n- Immobilize limb\n- Go hospital",
                "5": "END Choking:\n- Back blows\n- Abdominal thrusts\n- Repeat",
                "6": "END Suffocation:\n- Fresh air\n- Loosen clothes\n- CPR if needed"
            }
            response = tips.get(user_response[1], "END Invalid option")

    # ---------------- EMERGENCY ----------------
    elif user_response[0] == "2":

        if len(user_response) == 1:
            response = (
                "CON Emergency Numbers\n"
                "1. Ambulance\n"
                "2. Fire\n"
                "3. Police"
            )
        else:
            numbers = {
                "1": "END Ambulance: 112",
                "2": "END Fire: 999",
                "3": "END Police: 999"
            }
            response = numbers.get(user_response[1], "END Invalid option")

    # ---------------- ABOUT ----------------
    elif user_response[0] == "3":
        response = "END First Aid Chatbot v1.0"

    else:
        response = "END Invalid option"

    # ---------------- SAVE CHAT (IMPORTANT FIX HERE) ----------------
    if response.startswith("END"):
        save_chat(
            phone=phone_number,   # ALWAYS normalized
            question=text,
            response=response
        )

    return HttpResponse(response, content_type="text/plain")