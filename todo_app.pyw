'''A simple desktop app to track to do items. Task file is plaintext
    with new items on each line. Ex.
    Item 1
    Item 2
    Item 3
'''
import PySimpleGUI as sg
import time
import json

sg.theme('DarkGrey6')

def load_tasks():
    '''load the main tasks file and save as list'''
    with open('tasks.txt', 'r') as f:
        tasks = f.read().splitlines()

    return tasks


def load_perf():
    '''load the scoring dictionary'''
    with open('performance.json', 'r') as f:
        performance = json.load(f)

    return performance   


def update_list(tasks):
    '''Updates task file with new or removed items'''
    with open('tasks.txt', 'w') as f:
        for task in tasks:
            f.writelines(task+'\n')


def productivity(key):
    '''Takes key for task and calculates the time delta between open and closed.
        Returns value in hours rounded to 4 places'''
    diff = round((key[1] - key[0]) / 3600, 4)

    return diff


def scoring(d):
    '''Calculate scores based on close-open time'''
    scores = []
    for num in d.values():
        try:
            scores.append(num[2])
        except IndexError:
            pass

    return round(max(scores),4), round(min(scores),4), round(sum(scores) / len(scores),4)

# Load in variables
tasks = load_tasks()
performance = load_perf()
layout = [
         [sg.Text('Things to do today! Add a new item below'), sg.Button('Metrics', key='metrics')],
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
        if values['-IN-'] == '':
            sg.popup('Task was left blank', no_titlebar=True, keep_on_top=True)

        else:
            tasks.append(values['-IN-'])
            performance[values['-IN-']] = [time.time()]
            with open('performance.json', 'a') as outfile:
                json.dump(performance, outfile)
            window['items'].Update(values=tasks)
            window['add_item'].Update('Add')
            window['-IN-'].Update('')
            window['counter'].Update(value=f'You have {len(tasks)} items remaining')
            update_list(tasks)


    elif event == 'del_item':
        try:
            tasks.remove(values['items'][0])
            window['items'].Update(values=tasks)
            sg.popup(f'{values["items"][0]} was deleted', no_titlebar=True, keep_on_top=True)
            window['counter'].Update(value=f'You have {len(tasks)} items remaining')
            performance[values['items'][0]].append(time.time())
            diff = productivity(performance[values['items'][0]])
            performance[values['items'][0]].append(diff)
            with open('performance.json', 'w+') as outfile:
                json.dump(performance, outfile)
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

    elif event == 'metrics':
        try:
            metrics = load_perf()
            print(metrics)
            sg.popup('Here are some stats (hours)...', 
                    f'Max time open: {scoring(metrics)[0]}', 
                    f'Min time open: {scoring(metrics)[1]}', 
                    f'Ave time open: {scoring(metrics)[2]}',
                        no_titlebar=True, keep_on_top=True)
        except ValueError:
            sg.popup('No scoring available. Tasks need to created and closed to view this',
                        no_titlebar=True, keep_on_top=True)


window.close()
