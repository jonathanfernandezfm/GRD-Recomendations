import csv
import math
from random import seed
from random import random

numberOfMovies = 20
randomMovies = []
randomMoviesRatings = []
mediaUsuarioActual = 0
similitudes = []
peliculasAEvaluar = []
prediccionesRating = []

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
                similitudes.append([x, round(pearson,1)])
            else:
                similitudes.append([x, 0])

        similitudes.sort(key=lambda x: x[1], reverse=True)

def predicciones(vecinos):
    with open('./ml-latest-small/ratings.csv') as csvfile:
        ratingsReader = csv.reader(csvfile, delimiter=',')
        ratingsList = list(ratingsReader)
        ratingsList.pop(0)
        peliculasAEvaluar = []
        contador = 0

        for vecino in vecinos:
            userRatings = []
            userRatings = [item for item in ratingsList if int(item[0])==vecino[0]]

            for rating in userRatings:
                if not any(movie[0] == rating[1] for movie in randomMovies):
                    peliculasAEvaluar.append(rating[1])

        peliculasAEvaluar = list(dict.fromkeys(peliculasAEvaluar))

        for movieId in peliculasAEvaluar:
            contador += 1
            numerador = 0
            denominador = 0

            movieRatings = [item for item in ratingsList if movieId==item[1]]
            for rating in movieRatings:
                vecinoExists = [item for item in vecinos if int(rating[0])==item[0]]

                if len(vecinoExists):
                    #print(vecinoExists, rating)
                    numerador += float(vecinoExists[0][1]) * float(rating[2])
                    denominador += float(vecinoExists[0][1])

            if denominador != 0 and numerador != 0:
                prediccionesRating.append([movieId, numerador/denominador])
                #print(numerador, denominador, numerador/denominador)
            
            print(contador, "de", len(peliculasAEvaluar), "Pelicula:", movieId,"Valoracion", numerador/denominador)

def mostrarRecomendaciones():
    with open('./ml-latest-small/movies.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        movies = list(readCSV)
        movies.pop(0)

        peliculasRecomendadas = [item for item in prediccionesRating if item[1] >4.9]

        print(peliculasRecomendadas)

        print("**********//: RECOMENDACIONES ://*************")
        for movie in peliculasRecomendadas:
            movieToPrint = next(x for x in movies if x[0]==movie[0])
            print("*******************************")
            print("Title: ", movieToPrint[1])
            print("Categories: ", movieToPrint[2])
            print("*******************************")
        print("Recomendaciones: ", len(peliculasRecomendadas))

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
    
    mediaUsuarioActual = sumatorio/(numberOfMovies)

    # GENERAMOS LISTA DE VECINOS
    similitudUsuarios()

    # COGEMOS LOS 20 PRIMEROS O >0.5
    vecinosBuenos = similitudes[0:20]
    
    # GENERAR RECOMENDACIONES
    predicciones(vecinosBuenos)
    print(len(prediccionesRating))

    # PRINT RECOMENDACIONES
    mostrarRecomendaciones()

