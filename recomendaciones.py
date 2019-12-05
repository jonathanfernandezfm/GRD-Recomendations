import csv
import math
from random import seed
from random import random

numberOfMovies = 20
randomMovies = []
randomMoviesRatings = []
mediaUsuarioActual = 0
similitudes = []
recomendacionesID = []

def sortSimilitudes(val):
    return val[1]

def similitudUsuarios():
    with open('./ml-latest-small/ratings.csv') as csvfile:
        ratingsReader = csv.reader(csvfile, delimiter=',')
        ratingsList = list(ratingsReader)
        ratingsList.pop(0)

        maxValueUsers = int(ratingsList[len(ratingsList)-1][0]) # Cogemos el numero del ultimo usuario (numero de usuarios que hay)

        for x in range(1, maxValueUsers):
            userRatings = []
            userRatings = [item for item in ratingsList if int(item[0])==x]
            sumatorioUser = 0.0
            mediaUser = 0

            for rating in userRatings:
                sumatorioUser += float(rating[2])
            
            mediaUser = sumatorioUser/len(userRatings)
            numerador = 0
            moduloUser1 = 0
            moduleUser2 = 0
            pearson = 0

            for index, movie in enumerate(randomMovies):
                ratingPeliculaUserActual = randomMoviesRatings[index][1]
                ratingPeliculaUser = list((x for x in userRatings if int(x[1])==int(movie[0]))) # Deberia devolver siempre 1 elemento o 0 si no coinciden

                if(len(ratingPeliculaUser)!=0):
                    ratingPeliculaUser = ratingPeliculaUser[0][2]
                    print("Pelicula: ", movie[0],"Rating propio: ", ratingPeliculaUserActual, "Media propia: ", mediaUsuarioActual, "Rating User: ", ratingPeliculaUser, "Media User", mediaUser)
                    numerador += (ratingPeliculaUserActual-mediaUsuarioActual)*(float(ratingPeliculaUser)-mediaUser)
                    moduloUser1 += pow((ratingPeliculaUserActual-mediaUsuarioActual), 2)
                    moduleUser2 += pow((float(ratingPeliculaUser)-mediaUser), 2)
            
            if(moduloUser1 != 0 and moduleUser2 != 0):
                pearson = numerador/(math.sqrt(moduloUser1)*math.sqrt(moduleUser2))
                similitudes.append([x, pearson])

        similitudes.sort(key=lambda x: x[1], reverse=True)

def recomendaciones(vecinos):
    with open('./ml-latest-small/ratings.csv') as csvfile:
        ratingsReader = csv.reader(csvfile, delimiter=',')
        ratingsList = list(ratingsReader)
        ratingsList.pop(0)

        for vecino in vecinos:
            userRatings = []
            userRatings = [item for item in ratingsList if int(item[0])==vecino[0]]

            for rating in userRatings:
                if not any(movie[0] == rating[1] for movie in randomMovies):
                    recomendacionesID.append(rating[1])

def mostrarRecomendaciones():
    with open('./ml-latest-small/movies.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        movies = list(readCSV)
        movies.pop(0)

        print("**********//: RECOMENDACIONES ://*************")
        for id in recomendacionesID:
            movie = next(x for x in movies if x[0]==id)
            print("*******************************")
            print("Title: ", movie[1])
            print("Categories: ", movie[2])
            print("*******************************")
        print("Recomendaciones: ", len(recomendacionesID))

with open('./ml-latest-small/movies.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    csvList = list(readCSV)
    calification = 0
    sumatorio = 0

    for x in range(0,numberOfMovies):
        randomMovies.append(csvList[int(random()*len(csvList))])
        calification = input("Inserta una calificacion para " + randomMovies[x][1] + ": ")
        
        if(calification == ''):
            calification = -1
        else:
            calification = int(calification)

        while calification < 0 or calification > 5 or type(calification) != int:
            calification = input("Intentalo de nuevo. (0<x<5): ")
            if(calification == ''):
                calification = -1
            else:
                calification = int(calification)
            
        randomMoviesRatings.append([randomMovies[x][0], calification])
        sumatorio += calification
    
    mediaUsuarioActual = sumatorio/(numberOfMovies-1)

    # GENERAMOS LISTA DE VECINOS
    similitudUsuarios()

    # COGEMOS LOS 20 PRIMEROS O >0.5
    vecinosBuenos = [item for item in similitudes if float(item[1])>0.5]
    if len(vecinosBuenos) > 20:
        vecinosBuenos = vecinosBuenos[0:20]
    
    # GENERAR RECOMENDACIONES
    recomendaciones(vecinosBuenos)
    recomendacionesID = list(dict.fromkeys(recomendacionesID))

    # PRINT RECOMENDACIONES
    mostrarRecomendaciones()

