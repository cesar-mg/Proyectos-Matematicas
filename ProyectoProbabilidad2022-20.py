import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# CONSTANTES DE CONFIGURACION
# ------------------------------------------------------------------
## N -> Numero de simulaciones
N = 100
## m -> Numero de clientes
m = 20
## k -> Nodos en la red
k = 5
## Matriz de probabilidades. Probabilidad de ir de i a j.
P = []
for i in range(k):
    P.append([])
    for j in range(k):
        if i != j:
            P[i].append(1/(k-1))
        else:
            P[i].append(0)

## Parametros de la distribución exponencial en la j-ésima posición
B = np.array([ 1 + float(i/10) for i in range(k)])
## Distribución inicial de clientes.
n = [int(m/k) for i in range(k)]

# ------------------------------------------------------------------
# FUNCIONES
# ------------------------------------------------------------------

## Funcion que busca el nodo que se demora menos tiempo.
def minNode():
    min = 100000000000000
    ## Validamos cada uno de los k nodos.
    for i in range(k):
        ## Seguimos unicamente si el nodo tiene clientes.
        if n[i] > 0:
            ## Obtenemos el tiempo que se demora cada nodo, con base a su respectiva distribución exponencial
            d = np.random.exponential(B[i])
            ## Buscamos el minimo.
            if d < min:
                node = i
                min = d
    return node, min

## Función que realiza la simulación. T = Tiempo total a simular
def simulate(T: float):
    # Matriz de estados de la simulacion. Q(t) = (Q_1(t)....Q_k(t)) donde 
    # Q_i(t) muestra el numero de clientes en el nodo i en el tiempo t.
    Q = []

    ## Tiempo actual de la simulación
    t = 0
    ## Obtenemos el nodo inicial.    
    node, tAcum = minNode()

    ## Obtenemos el siguiente nodo.
    next = np.random.choice(k, p = P[node])

    ## Simulamos
    while T >= t:
        
        # Agrege el estado en el tiempo t.
        if t < tAcum:
            Q.append(list.copy(n))
            
            t+= 1
        # Hace un movimiento de clientes si en el tiempo t sucede esto.
        else:
            ## Mueve los clientes
            n[node] -=1
            n[next] +=1

            ## Obtenemos el nodo donde sale el cliente.
            node, temp = minNode()
            ## Sumamos el tiempo de atención al tiempo acumulado.
            tAcum += temp
            
            ## Obtenemos el siguiente nodo.
            next = np.random.choice(k, p = P[node])

    return Q

## Calcula la integral
def integrate(Q):
    Q = np.array(Q)
    ## Matriz de respuesta de la integral para cada nodo i.
    result = []
    for i in range(k):
        ## Obtenemos los datos de la columna i, representando el estado del i-esimo nodo en cada tiempo t.
        actual = Q[:,i]
        ## Lista con los valores de la integral en el tiempo t.
        integral = []
        ## Calculamos los valores mediante la regla del trapecio, y de acuerdo a la definición de la integral.
        for j in range(len(actual)):
            integral.append(np.trapz(actual[:j])/(j+1))
        result.append(integral)
    return result

## Crea las graficas del i-esimo nodo entrado por parametro
def createGraph(result,i):
    ## Agregamos las simulaciones a la grafica.
    for j in result:
     plt.plot(j)

    ## Configuración de la grafica
    plt.title("Nodo: " + str(i))
    plt.ylabel(" Número de clientes ")
    plt.xlabel(" T ")
    plt.show()
## Calculamos el limite promediando el valor de la integral para las simulaciones
def limite(simulaciones):
    arr = np.array(simulaciones)
    for i in range(k):
        ## Obtenemos el valor de la integral de 0 a T del i-esimo nodo 
        lista = (arr[i][:,N-1]).tolist()
        ## Lo promediamos
        prom = sum(lista) / len(lista) 
        print("El valor del limite del nodo " + str(i) + " es " + str(prom) )
## Corre el programa
def main():
    data = [[] for z in range(k)]
    ## Simula N veces, y calcula la integral
    for j in range(N):
        simulation = integrate(simulate(10000))
        ## Guardamos los resultados de los k nodos.
        for i in range(k):
            data[i].append(simulation[i])

    ## Creamos las graficas
    for i in range(k):
        createGraph(data[i],i)
        
    ## Calculamos los limites 
    limite(data)
    
main()


