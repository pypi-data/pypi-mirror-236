from .visualize import visualize_COG
from .utils import clear_metadata, get_key
from .const import DATASETS, BASE_URL, seasons, months, diurnal, daily, base_url

import json
import requests
from IPython.display import display
from IPython.display import clear_output
import ipywidgets as widgets  # Import ipywidgets

#renders dropdowns 
def drop_down(options=DATASETS, value=None , _id='name', metadata={}):

    if _id == 'name':
        print("Select a dataset from the options below: ", end="")

    output = widgets.Output()
    dropdown = None
    # Create the dropdown widget
    if value != None:
        dropdown = widgets.Dropdown(options=options, description='', value=value)
    else:
        dropdown = widgets.Dropdown(options=options, description='', value=None)
    # Define a function to handle the dropdown's value change
    def handle_dropdown_change(change):
        with output:
            clear_output()
            selected_option = change.new
            handle_dataset_input(options, selected_option, _id, metadata=metadata)
    # Attach the function to the dropdown's value change event
    dropdown.observe(handle_dropdown_change, names='value')
    # Display the dropdown widget
    display(dropdown, output)

#clears a cell output and re-renders the dropdowns based on metadata
def clear_cell_and_render(metadata={}):
    pass

#input handler for dropdown
def handle_dataset_input(options, selected_option, _id, metadata={}):  
    metadata = clear_metadata(_id, options, selected_option, metadata)
    if metadata['name']['selected_option'] == DATASETS[0]:
        handle_trmm_lis_full(metadata)
    elif metadata['name']['selected_option'] == DATASETS[1]:
        handle_trmm_lis_seasonal(metadata)
    elif metadata['name']['selected_option'] == DATASETS[2]:
        handle_trmm_lis_monthly(metadata)
    elif metadata['name']['selected_option'] == DATASETS[3]:
        handle_trmm_lis_diurnal(metadata)
    elif metadata['name']['selected_option'] == DATASETS[4]:
        handle_trmm_lis_daily(metadata)
    elif metadata['name']['selected_option'] == DATASETS[5]:
        handle_otd_full(metadata)
    elif metadata['name']['selected_option'] == DATASETS[6]:
        handle_otd_monthly(metadata)
    elif metadata['name']['selected_option'] == DATASETS[7]:
        handle_otd_diurnal(metadata)
    elif metadata['name']['selected_option'] == DATASETS[8]:
        handle_otd_daily(metadata)
    elif metadata['name']['selected_option'] == DATASETS[9]:
        handle_isslis(metadata)
    elif metadata['name']['selected_option'] == DATASETS[10]:
        handle_nalma(metadata)
    elif metadata['name']['selected_option'] == DATASETS[11]:
        handle_hs3(metadata)


#handlers for different datasets

################################################Handlers for TRMM-LIS dataset################################################
def handle_trmm_lis_full(metadata={}):
    clear_cell_and_render(metadata)
    visualize_COG(BASE_URL+"VHRFC/201301/LIS/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.325,23.426]")
def handle_trmm_lis_seasonal(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"VHRSC/{seasons[metadata['arg2']['selected_option']]}"+"/LIS/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.00010455249866936356,0.06766455620527267]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select season: ", end="")
        drop_down(get_key(seasons), _id='arg2', metadata=metadata)
def handle_trmm_lis_monthly(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"VHRMC/{months[metadata['arg2']['selected_option']]}"+"/LIS/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.00010455249866936356,0.06766455620527267]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select month: ", end="")
        drop_down(get_key(months), _id='arg2', metadata=metadata)
def handle_trmm_lis_diurnal(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"VHRDC/{diurnal[metadata['arg2']['selected_option']]}"+"/LIS/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.00010455249866936356,0.06766455620527267]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select Time: ", end="")
        drop_down(get_key(diurnal), _id='arg2', metadata=metadata)
def handle_trmm_lis_daily(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"VHRAC/{daily[metadata['arg2']['selected_option']]}"+"/LIS/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.00010455249866936356,0.06766455620527267]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select day: ", end="")
        drop_down(get_key(daily), _id='arg2', metadata=metadata)
        
##################################################Handlers for OTD dataset################################################
def handle_otd_full(metadata={}):
    clear_cell_and_render(metadata)
    visualize_COG(BASE_URL+"HRFC/201301/OTD/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.325,55.426]")
def handle_otd_monthly(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"HRMC/{months[metadata['arg2']['selected_option']]}"+"/OTD/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0,0.2]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select month: ", end="")
        drop_down(get_key(months), _id='arg2', metadata=metadata)
def handle_otd_diurnal(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"LRDC/{diurnal[metadata['arg2']['selected_option']]}"+"/OTD/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0,0.002]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select Time: ", end="")
        drop_down(get_key(diurnal), _id='arg2', metadata=metadata)
def handle_otd_daily(metadata={}):
    clear_cell_and_render(metadata) 
    #name is already selected, ask for which season now
    if metadata.get('arg2') != None:
        url = f"HRAC/{daily[metadata['arg2']['selected_option']]}"+"/OTD/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0.00010455249866936356,0.06766455620527267]"
        visualize_COG(BASE_URL+url)
    else:
        print("Select day: ", end="")
        drop_down(get_key(daily), _id='arg2', metadata=metadata)
###################################################Handlers for isslis, nalma and hs3######################################
def handle_isslis(metadata={}):
    clear_cell_and_render(metadata)
    dataset_name = "isslis"
    if metadata.get('arg2') == None:
        print("Select year: ", end="")
        response = requests.get(f"{base_url}arg1?name={dataset_name}")
        response = json.loads(response.text)
        drop_down(response, _id='arg2', metadata=metadata)
    else:
        if metadata.get('arg3') == None:
            print("Select month: ", end="")
            response = requests.get(f"{base_url}arg2?name={dataset_name}&year={metadata['arg2']['selected_option']}")
            response = json.loads(response.text)
            drop_down(response, _id='arg3', metadata=metadata)
        else:
            if metadata.get('arg4') == None:
                print("Select day: ", end="")
                response = requests.get(f"{base_url}arg3?name={dataset_name}&year={metadata['arg2']['selected_option']}&month={metadata['arg3']['selected_option']}")
                response = json.loads(response.text)
                drop_down(response, _id='arg4', metadata=metadata)
            else:
                if metadata.get('arg5') == None:
                    print("Select Time/Instrument: ", end="")
                    response = requests.get(f"{base_url}arg4?name={dataset_name}&year={metadata['arg2']['selected_option']}&month={metadata['arg3']['selected_option']}&day={metadata['arg4']['selected_option']}")
                    response = json.loads(response.text)
                    drop_down(response, _id='arg5', metadata=metadata)
                else:
                    year = metadata['arg2']['selected_option']
                    month = metadata['arg3']['selected_option']
                    day = metadata['arg4']['selected_option']
                    arg4 = metadata['arg5']['selected_option']
                    url = f"ISS_LIS/{year}{month}{day}/{arg4}"+"/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0,0]"
                    visualize_COG(BASE_URL+url)
    
def handle_nalma(metadata={}):
    clear_cell_and_render(metadata)
    dataset_name = "nalma"
    if metadata.get('arg2') == None:
        print("Select year: ", end="")
        response = requests.get(f"{base_url}arg1?name={dataset_name}")
        response = json.loads(response.text)
        drop_down(response, _id='arg2', metadata=metadata)
    else:
        if metadata.get('arg3') == None:
            print("Select month: ", end="")
            response = requests.get(f"{base_url}arg2?name={dataset_name}&year={metadata['arg2']['selected_option']}")
            response = json.loads(response.text)
            drop_down(response, _id='arg3', metadata=metadata)
        else:
            if metadata.get('arg4') == None:
                print("Select day: ", end="")
                response = requests.get(f"{base_url}arg3?name={dataset_name}&year={metadata['arg2']['selected_option']}&month={metadata['arg3']['selected_option']}")
                response = json.loads(response.text)
                drop_down(response, _id='arg4', metadata=metadata)
            else:
                if metadata.get('arg5') == None:
                    print("Select Time/Instrumnet: ", end="")
                    response = requests.get(f"{base_url}arg4?name={dataset_name}&year={metadata['arg2']['selected_option']}&month={metadata['arg3']['selected_option']}&day={metadata['arg4']['selected_option']}")
                    response = json.loads(response.text)
                    drop_down(response, _id='arg5', metadata=metadata)
                else:
                    year = metadata['arg2']['selected_option']
                    month = metadata['arg3']['selected_option']
                    day = metadata['arg4']['selected_option']
                    arg4 = metadata['arg5']['selected_option']
                    arg4 = arg4.split("_")
                    url = f"NALMA_{arg4[0]}/{year}{month}{day}/{arg4[1]}"+"/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0,1]"
                    visualize_COG(BASE_URL+url, zoom=7, center={"lat": 33.5206608, "lon": -86.8024900})

def handle_hs3(metadata={}):
    clear_cell_and_render(metadata)
    dataset_name = "hs3"
    if metadata.get('arg2') == None:
        print("Select year: ", end="")
        response = requests.get(f"{base_url}arg1?name={dataset_name}")
        response = json.loads(response.text)
        drop_down(response, _id='arg2', metadata=metadata)
    else:
        if metadata.get('arg3') == None:
            print("Select month: ", end="")
            response = requests.get(f"{base_url}arg2?name={dataset_name}&year={metadata['arg2']['selected_option']}")
            response = json.loads(response.text)
            drop_down(response, _id='arg3', metadata=metadata)
        else:
            if metadata.get('arg4') == None:
                print("Select day: ", end="")
                response = requests.get(f"{base_url}arg3?name={dataset_name}&year={metadata['arg2']['selected_option']}&month={metadata['arg3']['selected_option']}")
                response = json.loads(response.text)
                drop_down(response, _id='arg4', metadata=metadata)
            else:
                if metadata.get('arg5') == None:
                    print("Select Time/Instrument: ", end="")
                    response = requests.get(f"{base_url}arg4?name={dataset_name}&year={metadata['arg2']['selected_option']}&month={metadata['arg3']['selected_option']}&day={metadata['arg4']['selected_option']}")
                    response = json.loads(response.text)
                    drop_down(response, _id='arg5', metadata=metadata)
                else:
                    year = metadata['arg2']['selected_option']
                    month = metadata['arg3']['selected_option']
                    day = metadata['arg4']['selected_option']
                    arg4 = metadata['arg5']['selected_option']
                    url = f"HS3/{year}{month}{day}/{arg4}"+"/{z}/{x}/{y}.png?colormap=terrain&stretch_range=[0,0]"
                    visualize_COG(BASE_URL+url)