from django.shortcuts import render
from dashboard.gpio import turn_off_led, turn_on_led, toggle_mode
import json

PI_IP_ADDR = '192.168.2.178:8000'

def dashboard(request):
    out = ''


    if request is None:
        # Handle the case where the request is None
       pass; 
    # For POST requests to page
    elif request.method == 'POST':

        # Check if the power on checkbox is selected
        # Update value
        if request.POST.get('state') == 'on':
            # if selected, turn on via put request
            values = {"name": "on"}
            r = requests.put('http://' + PI_IP_ADDR + '/api/state/1/', json=values)
            manual_state = True

        else:
            # if not selected, turn off via put request
            values = {"name": "off"}
            r = requests.put('http://' + PI_IP_ADDR + '/api/state/1/', json=values)
            manual_state = False

        # Check if the auto mode checkbox is selected
        # Update value
        if request.POST.get('mode') == 'auto':
            # if selected, turn on via put request
            values = {"name": "auto"}
            r = requests.put('http://' + PI_IP_ADDR + '/api/mode/1/', json=values)
            auto_mode()

        else:
            # if not selected, turn off via put request
            values = {"name": "manual"}
            r = requests.put('http://' + PI_IP_ADDR + '/api/mode/1/', json=values)
            toggle_mode()

            if manual_state:
                turn_on_led()
            else:
                turn_off_led()

    
    # get state of state variable, load as json and set currentState variable
    r = requests.get('http://' + PI_IP_ADDR + '/api/state/1/')
    result = r.text
    output = json.loads(result)
    currentstate = output['name']

    # get state of mode variable, load as json and set currentMode variable
    r = requests.get('http://' + PI_IP_ADDR + '/api/mode/1/')
    result = r.text
    output = json.loads(result)
    currentmode = output['name']


    # Context variables to be passed to page
    # used for default slider values
    context = {
        'currentMode': currentmode,
        'currentState': currentstate
    }

    # render page, using variables
    return render(request, 'dashboard.html', context)
