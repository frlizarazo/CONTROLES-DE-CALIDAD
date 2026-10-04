import tkinter.ttk as ttk

from Estilos.colores import *
from Estilos.fuentes import FUENTE_NEGRITA, FUENTE_PEQUEÑA

def apply_style():
    style = ttk.Style()
            
    style.theme_create('Background.TNotebook', parent='alt', settings={
        'TNotebook': {
            'configure': {
                'borderwidth': 0,
                'background': COLOR_FONDO
            }
        },
        'TNotebook.Tab': {
            'configure': {
                'padding': [15, 5], 
                'background': COLOR_FONDO, 
                'borderwidth': 0,
                'foreground': COLOR_FUENTE_SECUNDARIA,
                **FUENTE_PEQUEÑA
            },
            'map': {
                'background': [('selected', COLOR_PRINCIPAL), 
                               ('active'  , COLOR_PRINCIPAL)],
                'foreground': [('selected', COLOR_FUENTE_PRINCIPAL), 
                               ('active'  , COLOR_FUENTE_PRINCIPAL)],
                'expand': [('selected', [1, 2, 1, 0])]
            }
        },
        'TSeparator': {
            'configure': {
                'relief': 'flat',
                'background': COLOR_FONDO,
                'borderwidth': 2
            }
        },
        'Treeview': {
            'configure': { 
                'background': COLOR_CLARO,
                'foreground': COLOR_FUENTE_SECUNDARIA,
                'rowheight' : 25,
                'fieldbackground': COLOR_FONDO,
                **FUENTE_PEQUEÑA
            }
        },
        'Treeview.Heading': {
            'configure': {
                'background': COLOR_PRINCIPAL,
                'foreground': COLOR_FUENTE_PRINCIPAL,
                **FUENTE_NEGRITA
            },
        },
        'TProgressbar': {
            'configure': {
                'background': COLOR_PRINCIPAL, 
                'troughcolor': COLOR_CLARO, 
                'thickness': 15,
                'borderwidth': 0,
                'troughrelief': 'flat'
            },
        },
        'TCombobox' : {
            'configure' : {
                'background'      : COLOR_PRINCIPAL,
                'foreground'      : COLOR_OSCURO,
                'arrowcolor'      : COLOR_FUENTE_PRINCIPAL,
                'fieldbackground' : COLOR_CLARO,
                'relief'          : 'flat',
                'borderwidth'     : 0,
                'padding'         : 0,
                'selectbackground': COLOR_CLARO,
                'selectforeground': COLOR_OSCURO,
                'troughrelief': 'flat'
            }
        },
        'TSpinbox' : {
            'configure' : {
                'background'      : COLOR_PRINCIPAL,
                'foreground'      : COLOR_OSCURO,
                'arrowcolor'      : COLOR_FUENTE_PRINCIPAL,
                'fieldbackground' : COLOR_CLARO,
                'relief'          : 'flat',
                'borderwidth'     : 0,
                'padding'         : 0,
                'selectbackground': COLOR_CLARO,
                'selectforeground': COLOR_OSCURO,
                'troughrelief': 'flat'
            }
        },
        'TCombobox.Listbox' : {
            'configure' : {
                'background' : '#f0f0f0', 
                'foreground' : 'blue'
            }
        }
    })
    
    style.theme_use('Background.TNotebook')
    style.layout('TNotebook.Tab', [])
    style.layout('Background.TNotebook', [])
    style.layout('Treeview', [('Edge.Treeview.treearea', {'sticky': 'nsew'})])