# método para limpar a tela

def clear():
    # no windows e no linux
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
