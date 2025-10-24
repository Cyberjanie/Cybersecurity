import math

# Lire les paramètres
a = 0
while a == 0:  # on répète tant que a vaut 0
    a = float(input("Entrez a (différent de 0) : "))

b = float(input("Entrez b : "))
c = float(input("Entrez c : "))

# Calcul du discriminant
delta = b**2 - 4*a*c

if delta < 0:
    print("Pas de solution réelle")
elif delta == 0:
    x = -b / (2*a)
    print("Une solution unique :", x)
else:
    x1 = (-b - math.sqrt(delta)) / (2*a)
    x2 = (-b + math.sqrt(delta)) / (2*a)
    print("Deux solutions :")
    print("x1 =", x1)
    print("x2 =", x2)