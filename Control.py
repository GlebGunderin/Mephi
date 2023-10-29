import matplotlib.pyplot as plt


const = {'a1': 15.7,
             'a2': 17.8,
             'a3': 0.71,
             'a4': 23.7,
             'a5': 34.0,
             'r0': 1.4,
             'delta_MH': 7.289,
             'delta_mn': 8.071}

class Element:
    def __init__(self, name: str, massNum: int, atomNum: int):
        self.name = name
        self.A = massNum
        self.Z = atomNum

    def Energy(self, N: int = 3) -> float:
        A,Z = self.A, self.Z
        G = A*const.get('a1')-(A**(2/3))*const.get('a2')-const.get('a3')*Z*(Z-1)/(A**(1/3))-const.get('a4')*((A-2*Z)**2)/A
        if A%2 == 0 and Z%2 == 0: G += const.get('a5')*A**(-3/4)
        elif A%2 != 0 and Z%2 != 0: G -= const.get('a5') * A ** (-3 / 4)
        return round(G,N)

    def SpecificEnergy(self, N: int = 3) -> float:
        A, Z = self.A, self.Z
        SG = self.Energy()/A
        return round(SG,N)

    def AtomMass(self) -> float:
        G = self.Energy()
        A, Z = self.A, self.Z
        delta_M = Z * const.get('delta_MH') + (A-Z) * const.get('delta_mn') - G
        M = delta_M + A * 931.5
        return M/931.5


    def Radius(self, N: int = 2) -> float:
        A = self.A
        radius = const.get('r0')*(A**(1/3))
        return round(radius, N)

    def Split(self):
        A, Z = self.A, self.Z
        if A%4 and Z%4:
            print("Деление ядра на 2 четно-четных осколка возможно")
        else:
            print("Деление ядра на 2 четно-четных осколка невозможно")

elements = []
elem = str(input("Введите название элемента таблицы Менделеева. Для прекращения набора напишите 0"))
while elem != '0':
    a = int(input("Введите массовое число этого элемента"))
    z = int(input("Введите зарядовое число этого элемента"))
    element = Element(elem, a, z)
    elements.append(element)
    elem = str(input("Введите название элемента из таблицы Менделеева"))

for el in elements:
    print(el.name)
    print(el.AtomMass())
    print(el.SpecificEnergy())
    print(el.Radius())
    el.Split()

maxZ = 103
arZ = list(range(1, maxZ))

for i in elements:
    plt.scatter(i.Z, i.Radius(), label=f'{i.name}')

plt.grid(True, color='#DDDDDD', linestyle='--', which='both')
plt.ylabel('Радиус, Фм')
plt.xlabel('Зарядовое число Z')
plt.title('Зависимость радиуса ядра R от зарядового числа Z')
plt.legend()
plt.show()

for i in elements:
    plt.scatter(i.Z, i.SpecificEnergy(), label=f'{i.name}')

plt.grid(True, color='#DDDDDD', linestyle='--', which='both')
plt.ylabel('Удельная энергия, МэВ')
plt.xlabel('Зарядовое число Z')
plt.title('Зависимость радиуса ядра R от зарядового числа Z')
plt.legend()
plt.show()