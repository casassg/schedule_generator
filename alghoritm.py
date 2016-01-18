import json
import datetime
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
    
    def __init__(self,gr,asig):
        self.classes= []
        self.grup=gr
        self.ass= asig
    def setClasses(self,cl):
        self.classes=cl
    def getGrup(self):
        return self.grup
    def getClasses(self):
        return self.classes
    def getAssig(self):
        return self.ass
    
class Assignatura:
    
    def __init__(self,nomi):
        self.nom=nomi
        self.grups=[]
    def setGrups(self,gr):
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
        return True
    elif(comparaHores(classe1.getHoraInici(),classe1.getHoraFi(), classe2.getHoraFi())):
        return True
    elif(comparaHores(classe2.getHoraInici(),classe2.getHoraFi(), classe1.getHoraInici())):
        return True
    elif(comparaHores(classe2.getHoraInici(),classe2.getHoraFi(), classe1.getHoraFi())):
        return True
    return False
    

    
def valoracio(sol):
    
    if(len(sol)==0):
        return 0
    else:
        ar = sol.pop()
        count = 0
        for s in sol:
            
            for c in s.getClasses():
                for a in ar.getClasses():
                    #print "nom grup c "+ str(s.getGrup()) + " nom grup ar " + str(ar.getGrup())+  "clases c: inici " + str(c.getHoraInici())+  " fi " + str(c.getHoraFi()) + " " + "clases a: inici " + str(a.getHoraInici())+  " fi " + str(a.getHoraFi()) + " "  
                    if(solapar(c,a)):
                        #print "es_solapa"
                        count = count +1
                        
        return count + valoracio(sol)

def generadorafuncions(n):
    return lambda sol:generatuple(valoracio(sol),n)
 
   
def generatuple(valor,n):
    return (valor<n,valor)



def donemhorari(assig,f,sol):
    
    if(len(assig)==0):
        sol_d = sol[:]
        fc = f(sol_d)
        rr = mostrar_json([(fc[1],sol)])
        #print " UNO DOS TRES::::"
        #print rr[0]
        if(fc[0]):
           # print "YEP"
            return [(fc[1],sol)]

        else:
            return []
        
       # return [sol]
    else:
        #print len(assig)
       # print "HIIII"
        a = assig.pop()
        sol_def = []
        #j = -1
        for c in a.getGrups():
            #print type(sol)
            ar = [c]
            #j = j+1
            #for d in c.getClasses():
               # print "JJJJJJJJJ " + str(j) +  " aassig "  + c.getAssig() +" clases grup:  " +  str(c.getGrup()) + " inici " +str(d.getHoraInici())+  " fi " + str(d.getHoraFi()) + " " + str(d.getDia())
            #print type(ar)
            #print len(assig)
            sol_d = sol[:]
            fc = f(sol_d)
            rr = mostrar_json([(fc[1],sol)])
            #print " LLLOOOLLLLLLLLLL::::"
            #print rr[0]
            soli = sol + [c]
            sol_d = soli[:]
            fc = f(sol_d)
            rr = mostrar_json([(fc[1],soli)])
            #print " LLLOOOLLLLLLOoooooooooooo"
            #print rr[0]
            #sol_d = soli[:]
            #c = f(sol_d)
            ass2 = assig[:]
            sd = donemhorari(ass2,f,soli)
            sol_def = sol_def +sd
            #j = j +1
        return sol_def


def mostrar_json(sol):
    sol.sort()
    sol_json = []
    for s in sol:
        dicaux = {}
        dicaux['solapaments']=s[0]
        ass = []
        for g in s[1]:
            dicgrup = {}
            dicgrup['nom_assignatura']=g.getAssig()
            dicgrup['id_grup']= g.getGrup()
            classes = []
            for c in g.getClasses():
                diclass = {}
                diclass['dia']=c.getDia()
                diclass['horaInici']= c.getHoraInici()
                diclass['horaFi']= c.getHoraFi()
                classes = classes +[diclass]
            dicgrup['classes']=classes
            ass = ass  + [dicgrup]
        dicaux['assig']=ass
        sol_json = sol_json + [dicaux]
    dic= dict()
    dic['solucio']= sol_json
    return (dic,json.JSONEncoder(dic) )

c1=Classes(datetime.time(13,0,0),datetime.time(15,0,0),'Dilluns')
c2=Classes(datetime.time(13,0,0),datetime.time(15,0,0),'Dimarts')
c3=Classes(datetime.time(13,0,0),datetime.time(15,0,0),'Dijous')

g1=Grup(1,[c1,c2,c3],'a1')


c4=Classes(datetime.time(16,0,0),datetime.time(18,0,0),'Dilluns')
c5=Classes(datetime.time(16,0,0),datetime.time(18,0,0),'Dimarts')
c6=Classes(datetime.time(16,0,0),datetime.time(18,0,0),'Dijous')


g2=Grup(2,[c4,c5,c6],'a1')


a1=Assignatura('a1',[g1,g2])
    


g3=Grup(1,[c1,c2,c3],'a2')
g4=Grup(2,[c4,c5,c6],'a2')

a2=Assignatura('a2',[g3,g4])
so= []
#print "HII"
#print type(so)
h1=donemhorari([a1,a2],generadorafuncions(5),[])

(d1,j1) = mostrar_json(h1)
