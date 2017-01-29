

class poly(object) :
    
    
    def __init__(self,l=None):
        '''les attributs de poly sont 
            -s la liste du polynome (suite a support fini)
            -degre son degre'''
        if l == None :
            self.suite = [0]
        else :
            if type(l) is not list :
                raise TypeError("l'entrée n'est pas une liste")
            self.suite = l[:]
        self.degre = len(self.suite)-1
        if self.suite == [0]:
            self.degre = float('-inf')
        if self.suite != [0] :
            k=len(self.suite)-1
            while self.suite[k] == 0 :
                self.suite.pop(k)
                k-=1
                if k==0 :
                    break
    def donneP(self):
        return self.suite
    def __eq__(self,other):
        return self.suite == other.suite
    def __repr__(self):
        return str(self.afficher())
    def __bool_(self):
        if self.suite == [] :
            return False
        else :
            return True

    def afficher(self):
        '''Affiche le polynome dans une forme habituelle'''
        if self.suite == [0] :
            return '0'
        if self.suite[0] != 0 :
            s='+ '+str(self.suite[0])
        else :
            s=''
        for k in range(1,len(self.suite)):
            if k==1 :
                if self.suite[1] != 0 :
                    s='+ '+str(self.suite[k])+'X '+s
            elif self.suite[k] != 0 and self.suite[k]!= 1 :
                s='+ '+str(self.suite[k])+'X**'+str(k)+' '+s
            elif self.suite[k] == 1 :
                s = '+ ' +'X**'+str(k)+' '+s
        s=s[2:]
        return s
    
        
        
    def evaluer(self,x):
        '''Donne l'valuation du polynome en x avec un schema de Horner'''
        E=0
        for k in range(len(self.suite)-1,-1,-1):
            E=E*x+self.suite[k]
        return E

    def __getitem__(self, x):
        '''permet d'evaluer un polynome en a avec "[a]"'''
        return self.evaluer(x)    
    def __add__(self,other):
        '''permet l'utilisation de "+"'''
        return polyAdd(self,other)
    def __sub__(self,other):
        '''permet l'utilisation de "-"'''
        return polySous(self,other)
    def __floordiv__(self,other):
        '''permet l'utilisation de "//"'''
        return polyDivEuc(self,other)[0]
    def __mod__(self,other):
        '''permet l'utilisation de "%"'''
        return polyDivEuc(self,other)[1]
    def __mul__(self,other):
        '''permet l'utilisation de "*"'''
        return polyProd(self,other)
    def __neg__(self):
        '''permet l'utilisation de "-"'''
        l=[-self.suite[k] for k in range(len(self.suite))]
        return poly(l)
    def __eq__(self,other):
        '''permet l'utilisation de "="'''
        return self.suite == other.suite
    def __repr__(self):
        '''permet d'afficher le polynome quand appelé'''
        return str(self.afficher())
    def __bool_(self):
        '''permet l'utilisation d'un polynome comme booleen :
            le polynome nul est False
            tous les autres sont True'''
        if self.suite == [] :
            return False
        else :
            return True
        
def polyAdd(P,Q):
    '''Renvoie un polynome de class poly qui est la somme de P et Q de class poly'''
    Add=[]
    if len(P.suite)>len(Q.suite):
        for k in range(len(Q.suite)):
            Add.append(P.suite[k]+Q.suite[k])
        Add+=P.suite[len(Q.suite):]
        return poly(Add)
    if len(P.suite)<len(Q.suite):
        for k in range(len(P.suite)):
            Add.append(P.suite[k]+Q.suite[k])
        Add+=Q.suite[len(P.suite):]
        return poly(Add)
    if len(P.suite)==len(Q.suite):
        for k in range(len(P.suite)):
            Add.append(P.suite[k]+Q.suite[k])
        k=len(Add)-1
        while Add[k] == 0 :
            Add.pop(k)
            k-=1
            if k==0 :
                break
        return poly(Add)
        
def polySous(P,Q):
    '''Renvoie un polynome de class poly qui est la difference de P et Q de class poly'''
    Add=[]
    B=poly(Q.suite)
    B=-B
    if len(P.suite)>len(B.suite):
        for k in range(len(B.suite)):
            Add.append(P.suite[k]+B.suite[k])
        Add+=P.suite[len(B.suite):]
        return poly(Add)
    if len(P.suite)<len(B.suite):
        for k in range(len(P.suite)):
            Add.append(P.suite[k]+B.suite[k])
        Add+=B.suite[len(P.suite):]
        return poly(Add)
    if len(P.suite)==len(B.suite):
        for k in range(len(P.suite)):
            Add.append(P.suite[k]+B.suite[k])
        k=len(Add)-1
        while Add[k] == 0 :
            Add.pop(k)
            k-=1
            if k==0 :
                break
        return poly(Add)
        
def polyProd(P,Q):
    '''renvoie un polynome de la class poly, le produit de P et Q de class poly'''
    Prod=[]
    dP=len(P.suite)-1
    dQ=len(Q.suite)-1
    
    a1=0
    a1+=P.suite[0]*Q.suite[0]
    Prod.append(a1)
    for i in range(1,dP+dQ+1):
        ai=0
        for k in range(i):
            if len(P.suite)>k and len(Q.suite)>i-k :
                ai+=P.suite[k]*Q.suite[i-k]
            else :
                ai+=0
        Prod.append(ai)
    return poly(Prod)
    

def polyDivEuc(A,B):
    '''Renvoie pour A et B polynomes de la class poly :
        -Q un polynome de la class poly 
        -R un polynome de la class poly 
    Avec (Q,R) le couple (Quotient,Reste) de la division euclidienne de A par
    B'''
    def polyDomin(P):
            Domin=polySous(P,poly(P.suite[:-1]))
            return Domin
    def DivisionDomin(D1,D2):
        a=D1.suite[-1]/D2.suite[-1]
        degA=D1.degre-D2.degre
        A=[0 for k in range(degA)]+[a]
        return poly(A)
    
    X=poly(A.suite)
    Y=poly(B.suite)
    Q=poly([0])
    R=poly(X.suite)
    while R.degre >-1 and R.degre>=Y.degre:
        M=DivisionDomin(polyDomin(R),polyDomin(Y))
        Q=polyAdd(Q,M)
        R=polySous(R,polyProd(M,Y))
    return Q,R   
    