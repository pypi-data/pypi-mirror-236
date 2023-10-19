import os
from .abstract_gui import create_window_manager,get_gui_fun,create_row_of_buttons
from abstract_utilities.path_utils import get_directory,is_file
window_browser_mgr,browse_bridge,browse_script_name=create_window_manager(script_name="browse_script",global_var=globals())
def return_directory():
    values = window_browser_mgr.get_values()
    directory = values['-DIR-']
    if is_file(values['-DIR-']):
        directory = get_directory(values['-DIR-'])
    if directory == '':
        directory = os.getcwd()
    return directory
def scan_window(event):
    values = window_browser_mgr.get_values()
    if event == "files":
        window['-DIR-'].update(value=values["files"])
    if event == "directory":
        window['-DIR-'].update(value=values["directory"])
    if event == '-SCAN-':
        js_browse_bridge["last_scan"]=is_file(values['-DIR-'])
        scan_results = scan_directory(return_directory(), js_browse_bridge["scan_mode"])
        window['-FILES-'].update(scan_results)
    if event == 'Select Highlighted':
        if len(values['-FILES-'])>0:
            window['-DIR-'].update(value=os.path.join(return_directory(), values['-FILES-'][0]))
    if event == '-MODE-':
        js_browse_bridge["scan_mode"] = 'folder' if js_browse_bridge["scan_mode"] == 'file' else 'file'
        window.Element('-MODE-').update(text=f"F{js_browse_bridge['scan_mode'][1:]}  Scan Mode")

    if event == "<-":
        # Navigate up to the parent directory
        if return_directory() not in js_browse_bridge["history"]:
            js_browse_bridge["history"].append(return_directory())
        directory = os.path.dirname(return_directory())  # This will give the parent directory
        window['-DIR-'].update(value=directory)
        window['-FILES-'].update(values=scan_directory(directory, js_browse_bridge["scan_mode"]))
    if event == "->":
        # Navigate down into the selected directory or move to the next history path
        if values['-FILES-']:  # If there's a selected folder in the listbox
            directory = os.path.join(return_directory(), values['-FILES-'][0])
            forward_dir(directory)
            
        elif js_browse_bridge["history"]:  # If there's a directory in the history stack
            next_directory = js_browse_bridge["history"].pop()
            window['-DIR-'].update(value=next_directory)
            window['-FILES-'].update(values=scan_directory(next_directory, js_browse_bridge["scan_mode"]))
def forward_dir(directory):
    if os.path.isdir(directory):
        window_browser_mgr.update_values(key='-DIR-',args={"value":directory})
        window_browser_mgr.update_values(key='-FILES-',args={"values":scan_directory(directory, js_bridge["scan_mode"])})
def scan_directory(directory_path, mode):
    if mode == 'file':
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    else: # mode == 'folder'
        return [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
def get_scan_browser():
    layout = [
        [get_gui_fun("Text",args={"text":'Directory to scan:'}), get_gui_fun("InputText",args={"default_text":os.getcwd(),"key":'-DIR-'}),
         get_gui_fun("FolderBrowse",args={"button_text":"Folders", "enable_events":True, "key":"directory"}),
         get_gui_fun("FileBrowse",args={"button_text":"Files", "enable_events":True, "key":"files"})],
        [get_gui_fun("Listbox",args={"values":[],"size":(50, 10),"key":'-FILES-',"enable_events":True})],
        [create_row_of_buttons({"button_text":"Scan","key":"-SCAN-","enable_events":True},"<-",{"button_text":"File Scan Mode","key":"-MODE-","enable_events":True},"->",'Select Highlighted','Ok')]
    ]
    
    js_browse_bridge = browse_bridge.return_global_variables(script_name=browse_script_name)
    js_browse_bridge["scan_mode"]="file"
    js_browse_bridge["history"] = []
    window = window_browser_mgr.get_new_window('File/Folder Scanner',args={"layout":layout,"event_function":"scan_window"})
    window_browser_mgr.while_basic(window=window)
    return browse_bridge['-DIR-']
