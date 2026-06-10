from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import africastalking


@csrf_exempt
def ussd_callback(request):
    session_id = request.POST.get("sessionId")
    phone_number = request.POST.get("phoneNumber")
    text = request.POST.get("text", "")

    # Spliting the text to handle submenus
    # in the following way e.g. "1*2" → ["1", "2"]
    user_response = text.split("*")

    if text == "":
        response = "CON Welcome to First Aid Chatbot.\nPlease tag your area of interest today.\n1. Tips\n2. Emergency Numbers\n3. About"
    elif user_response[0] == "1":
        if len(user_response) == 1:
             response = (
    "CON First Aid Tips:\n"
    "1. Bleeding\n"
    "2. Burns\n"
    "3. Fractures\n"
    "4. Snakebite\n"
    "5. Choking\n"
    "6. Suffocation"
)
        elif len(user_response) == 2:
            if user_response[1] == "1":
                response = "END Bleeding Tips:\n- Apply pressure\n- Elevate limb\n- Call help if serious"
            elif user_response[1] == "2":
                response = "END Burns Tips:\n- Cool with water\n- Cover with clean cloth\n- Call help if severe"
            elif user_response[1] == "3":
                response = "END Fracture Tips:\n- Immobilize\n- Avoid moving\n- Seek medical help"
            elif user_response[1] == "4":
                response = "END Snakebite Tips:\n- Keep victim calm & still\n- Keep bite below heart level\n- Clean wound & seek hospital"
            elif user_response[1] == "5":    
            
                response = "END Choking Tips:\n- Give 5 back blows\n- Give 5 abdominal thrusts\n- Repeat until clear or passed out"
            elif user_response[1] == "6":
                response = "END Suffocation Tips:\n- Move victim to fresh air\n- Loosen tight clothing\n- Check breathing & start CPR if needed"
            else:
                response = "END Invalid option. Try again."
        
    elif user_response[0] == "2":
        if len(user_response) == 1:
            response = "CON Emergency Numbers:\n1. Ambulance\n2. Fire\n3. Police"
        elif len(user_response) == 2:
            if user_response[1] == "1":
                response = "END Ambulance: 911"
            elif user_response[1] == "2":
                response = "END Fire: 999"
            elif user_response[1] == "3":
                response = "END Police: 112"
            else:
                response = "END Invalid option. Try again."
    elif user_response[0] == "3":
        response = "END First Aid Chatbot v1.0. Provides tips and emergency numbers."
    else:
        response = "END Invalid option. Try again."

    return HttpResponse(response, content_type='text/plain')