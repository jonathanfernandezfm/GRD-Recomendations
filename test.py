import csv
from random import seed
from random import random

seed(1)
numberOfMovies = 5
randomMovies = []
randomMoviesRatings = []
mediaUsuarioActual = 0

similitudes = []

def similitudUsuarios(usuario1, usuario2):
    with open('./ml-latest-small/ratings.csv') as csvfile:
        ratingsReader = csv.reader(csvfile, delimiter=',')
        ratingsList = list(ratingsReader)
        ratingsList.pop(0)
        #maxValueUsers = int(max(ratingsList, key=lambda row: int(row[1]))[0])
        maxValueUsers = 2

        for x in range(1, maxValueUsers):
            userRatings = []
            userRatings = [item for item in ratingsList if int(item[0])==x]
            sumatorioUser = 0.0
            mediaUser = 0

            for rating in userRatings:
                sumatorioUser += float(rating[2])
            
            mediaUser = sumatorioUser/len(userRatings)
            numerador = 0

            for index, movie in enumerate(randomMovies):
                ratingPeliculaUserActual = randomMoviesRatings[index][1];
                ratingPeliculaUser = 






with open('./ml-latest-small/movies.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    csvList = list(readCSV)
    calification = 0
    sumatorio = 0

    for x in range(1,numberOfMovies):
        randomMovies.append(csvList[int(random()*len(csvList))])
        calification = int(input("Inserta una calificacion para " + randomMovies[x-1][1] + ": "))
        while calification < 0 or calification > 5:
            calification = int(input("Inserta una calificacion para " + randomMovies[x-1][1] + ": "))
            
        randomMoviesRatings.append([randomMovies[x-1][0], calification])
        sumatorio += calification
    
    mediaUsuarioActual = sumatorio/numberOfMovies

    similitudUsuarios(1, 1)

