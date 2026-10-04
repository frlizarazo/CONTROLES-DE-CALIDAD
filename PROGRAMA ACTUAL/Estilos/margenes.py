# Espaciado --------------------------------------------------------------------------------------

espacio_normal   = 10
espacio_grande   = 20
espacio_estrecho = 5

MARGEN_NORMAL = {
    'padx' : espacio_normal,
    'pady' : espacio_normal
}

MARGEN_GRANDE = {
    'padx' : espacio_grande,
    'pady' : espacio_grande
}

MARGEN_ESTRECHA = {
    'padx' : espacio_estrecho,
    'pady' : espacio_estrecho
}

MARGEN_HORIZONTAL = {
    'padx' : espacio_grande,
    'pady' : espacio_normal
}

MARGEN_SOLO_HORIZONTAL = {
    'padx' : espacio_grande,
    'pady' : 0
}

MARGEN_VERTICAL = {
    'padx' : espacio_normal,
    'pady' : espacio_grande
}

# Alineación --------------------------------------------------------------------------------------

LEFT = {
    'side' : 'left'
}

RIGHT = {
    'side' : 'right'
}

TOP = {
    'side' : 'top'
}

BOTTON = {
    'side' : 'botton'
}

# Configuración de ocupación del espacio ----------------------------------------------------------

EXPANDIR = {
    'expand' : True, 
    'fill' : 'both'
}

EXPANDIR_HORIZONTAL = {
    'expand' : True, 
    'fill' : 'x'
}

EXPANDIR_VERTICAL = {
    'expand' : True, 
    'fill' : 'y'
}