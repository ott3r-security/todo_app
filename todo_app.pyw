'''A simple desktop app to track to do items. Task file is plaintext
    with new items on each line. Ex.
    Item 1
    Item 2
    Item 3
'''
import PySimpleGUI as sg


sg.theme('DarkGrey6')

def load_tasks():
    '''load the main tasks file and save as list'''
    with open('tasks.txt', 'r') as f:
        tasks = f.read().splitlines()

    return tasks

def update_list(tasks):
    '''Updates task file with new or removed items'''
    with open('tasks.txt', 'w') as f:
        for task in tasks:
            f.writelines(task+'\n')

tasks = load_tasks()
layout = [
         [sg.Text('Things to do today! Add a New Item Below')],
         [sg.Input(key='-IN-', size=(43, 4))],
         [sg.Listbox(values=tasks, size=(41, 15), key="items")], 
         [sg.Button('Add', key='add_item', size=(8, 3)), sg.Button('Remove', key='del_item', size=(8, 3)),
            sg.Button('Edit', size=(8, 3), key='edit'), sg.Button('Exit', size=(8, 3))],
         [sg.Text(f'You have {len(tasks)} items remaining', key='counter')],
         ]

window = sg.Window('To Do App', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        break

    elif event == 'add_item':
        print(event, values)
        if values['-IN-'] == '':
            sg.popup('Task was left blank', no_titlebar=True, keep_on_top=True)

        else:
            tasks.append(values['-IN-'])
            window['items'].Update(values=tasks)
            window['add_item'].Update('Add')
            window['-IN-'].Update('')
            window['counter'].Update(value=f'You have {len(tasks)} items remaining')
            update_list(tasks)

    elif event == 'del_item':
        try:
            tasks.remove(values['items'][0])
            window['items'].Update(values=tasks) #changed values to singular
            sg.popup(f'{values["items"][0]} was deleted', no_titlebar=True, keep_on_top=True)
            window['counter'].Update(value=f'You have {len(tasks)} items remaining')
            update_list(tasks)
        except IndexError:
            sg.popup('No items to remove or nothing selected to remove', no_titlebar=True, keep_on_top=True)

    elif event == 'edit':
        try:
            EDIT_VAL = values['items'][0]
            tasks.remove(EDIT_VAL)
            window['items'].Update(values=tasks)
            window['-IN-'].Update(value=EDIT_VAL)
            window['add_item'].Update('Save')
        except IndexError:
            sg.popup('Choose an item to edit', no_titlebar=True, keep_on_top=True)

window.close()
