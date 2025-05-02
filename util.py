class Util:

    def __init__(self):
        pass

    def RemoverCaracteresEspeciais(self, texto):
        texto = texto.replace("'", "")
        texto = texto.replace('"', "")
        texto = texto.replace("`", "")
        texto = texto.replace("´", "")
        texto = texto.replace("`", "")
        texto = texto.replace("*", "")
        texto = texto.replace("**", "")

        return texto
