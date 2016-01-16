
class Classes:
    def __init__(self,horain,horaf,di):
        self.dia= di
        self.horainici=horain
        self.horafi=horaf
    def getHoraInici(self):
        return self.horainici
    def getHoraFi(self):
        return self.horafi
    def getDia(self):
        return self.dia


class Grup:

    def __init__(self,gr,clas):
        self.classes= clas
        self.grup=gr
    def getGrup(self):
        return self.grup
    def getClasses(self):
        return self.classes


class Assignatura:

    def __init__(self,nomi,gr):
        self.nom=nomi
        self.grups=gr
    def getNom(self):
        return self.nom
    def getGrups(self):
        return self.grups

def comparaHores(horaInici,horaFi,hora):
    return horaInici<=hora and horaFi>=hora

def solapar(classe1,classe2):
    if(classe1.getDia() != classe2.getDia()):
        return False
    elif(comparaHores(classe1.getHoraInici(),classe1.getHoraFi(), classe2.getHoraInici())):
        return False
    elif(comparaHores(classe1.getHoraInici(),classe1.getHoraFi(), classe2.getHoraFi())):
        return False
    elif(comparaHores(classe2.getHoraInici(),classe2.getHoraFi(), classe1.getHoraInici())):
        return False
    elif(comparaHores(classe2.getHoraInici(),classe2.getHoraFi(), classe1.getHoraFi())):
        return False
    return True



def valoracio(sol):

    ar = sol.pop()
    count = 0
    for s in sol:
        for c in s.getClasses():
            for a in ar.getClasses():
                if(solapar(c,a)):
                    count = count +1

    return count + valoracio(sol)

def generadorafuncions(n):
    return lambda sol:generatuple(valoracio(sol),n)


def generatuple(valor,n):
    return (valor<n,valor)



def donemhorari(assig,f,sol):

    if(len(assig)==0):
        return [sol]
    else:
        a = assig.pop()
        sol_def = []
        for c in a.getGrups:
            soli = sol.add(c)
            sol_d = soli[:]
            fc = f(sol_d)
            if(fc[0]):
                sd = donemhorari(assig,f,(fc[1],soli))
                sol_def = sol_def +sd
        return sol_def