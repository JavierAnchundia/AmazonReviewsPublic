from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework.views import APIView
from .models import  *
from .serializers import *
from rest_framework.response import Response
from django.db import connection
from django.http import JsonResponse

from amazonreviewsapp.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


"""with open('C:/Users/javie/Downloads/archive/movies.txt', encoding="latin-1") as file:
        data = file.readlines()
        data.append("\n")
        completeLineOfData = []

        productIdStr = "product/productId: "
        userIdStr = "review/userId: "
        profileNameStr = "review/profileName: "
        helpfulnessStr = "review/helpfulness: "
        scoreStr = "review/score: "
        timeStr = "review/time: "
        summaryStr = "review/summary: "
        textStr = "review/text: "
        for line in data:






            try:
                if line != '\n':
                    completeLineOfData.append(line.strip())

                if line == '\n' and  completeLineOfData:

                    helpfullnessValues = str(completeLineOfData[3][len(helpfulnessStr):]).split("/")
                    helpfullnessFinalValue = 0
                    if int(helpfullnessValues[1]) == 0:
                        helpfullnessFinalValue = 0
                    else:
                        helpfullnessFinalValue = int(helpfullnessValues[0]) / int(helpfullnessValues[1])

                    Review.objects.create(productId=completeLineOfData[0][len(productIdStr):],
                                          userId=completeLineOfData[1][len(userIdStr):],
                                          profileName=completeLineOfData[2][len(profileNameStr):],
                                          helpfulness=helpfullnessFinalValue,
                                          score=int(float(completeLineOfData[4][len(scoreStr):])),
                                          time=make_aware(
                                              datetime.fromtimestamp(int(completeLineOfData[5][len(timeStr):]))),
                                          summary=completeLineOfData[6][len(summaryStr):],
                                          text=completeLineOfData[7][len(textStr):]

                                          )

                    completeLineOfData.clear()
                    helpfullnessFinalValue = 0
                    helpfullnessValues = []
            except:

                print("Error")
                pass

    """


class ReviewView(APIView):



    def post(self, request, format=None):
            

        mainSQLQuery = "SELECT * FROM amazonreviewsapp_review "
        countUsersQuery = "SELECT COUNT(DISTINCT userId)  FROM (SELECT * FROM amazonreviewsapp_review "
        maxScoreQuery = "SELECT MAX(score) FROM (SELECT * FROM amazonreviewsapp_review "
        minScoreQuery = "SELECT MIN(score)  FROM (SELECT * FROM amazonreviewsapp_review "
        promScoreQuery = "SELECT AVG(score)  FROM (SELECT * FROM amazonreviewsapp_review "
        dateTimeScoreQuery = "SELECT cast( UNIX_TIMESTAMP(time)*1000 as decimal(14,0)),score  FROM  (SELECT * FROM amazonreviewsapp_review "
        dateTimeHelpFullnessQuery = "SELECT  cast( UNIX_TIMESTAMP(time)*1000 as decimal(14,0)), helpfulness  FROM (SELECT * FROM amazonreviewsapp_review "

        conditionsQuery = ""



        #Primera condicion para ver si se hizo uso de algun filtro
        if (request.data.get("dateFilterOn") == "True" or request.data.get("movieCodeFilterOn") == "True" or request.data.get("userNameFilterOn") == "True"):
            conditionsQuery += "WHERE "
        # Filtro de fechas
        if (request.data.get("date_start") and request.data.get("date_end")
                and request.data.get("dateFilterOn") == "True") :
            conditionsQuery += "time between '{}' and '{}'".format(request.data.get("date_start"),
                                                            request.data.get("date_end"))


            # Si hay otros filtros agregar un "and"
            if (request.data.get("movieCodeFilterOn") == "True"
                    or request.data.get("userNameFilterOn") == "True"):
                conditionsQuery += "and "

        #Filtro de codigo de pelicula
        if  request.data.get("movieCode") and request.data.get("movieCodeFilterOn") == "True" :
            conditionsQuery += "productId =  '{}'".format(request.data.get("movieCode"))
            if request.data.get("userNameFilterOn") == "True":
                conditionsQuery += " and "

        #Filtro de nombres de usuarios
        if request.data.get("userNameList") and request.data.get("userNameFilterOn") == "True":
            conditionsQuery += "profileName IN  {}".format(tuple(request.data.get("userNameList").split(",")))

        #Agrego al Query principal cualquier condicion

        if (request.data.get("mainQueryOn") == "True"):
            mainSQLQuery += conditionsQuery + " LIMIT 200"
            countUsersQuery += conditionsQuery + " LIMIT 200) AS a"
            maxScoreQuery += conditionsQuery + " LIMIT 200) AS a"
            minScoreQuery += conditionsQuery + " LIMIT 200) AS a"
            promScoreQuery += conditionsQuery + " LIMIT 200) AS a"
            dateTimeScoreQuery += conditionsQuery + " GROUP BY time LIMIT 200) AS a"
            dateTimeHelpFullnessQuery += conditionsQuery + " GROUP BY time LIMIT 200) AS a"

        else:
            if (request.data.get("Top10WorstScoreOn") == "True"):
                mainSQLQuery += conditionsQuery + " ORDER BY score ASC LIMIT 10"
                countUsersQuery += conditionsQuery + " ORDER BY score ASC LIMIT 10) AS a"
                maxScoreQuery += conditionsQuery + " ORDER BY score ASC LIMIT 10) AS a"
                minScoreQuery += conditionsQuery + " ORDER BY score ASC LIMIT 10) AS a"
                promScoreQuery += conditionsQuery + " ORDER BY score ASC LIMIT 10) AS a"
                dateTimeScoreQuery += conditionsQuery + " GROUP BY time ORDER BY score ASC LIMIT 10) AS a"
                dateTimeHelpFullnessQuery += conditionsQuery + " GROUP BY time ORDER BY score ASC LIMIT 10) AS a"

            else:
                if (request.data.get("Top10BestScoreOn") == "True"):
                    mainSQLQuery += conditionsQuery + " ORDER BY score DESC LIMIT 10"
                    countUsersQuery += conditionsQuery + " ORDER BY score DESC LIMIT 10) AS a"
                    maxScoreQuery += conditionsQuery + " ORDER BY score DESC LIMIT 10) AS a"
                    minScoreQuery += conditionsQuery + " ORDER BY score DESC LIMIT 10) AS a"
                    promScoreQuery += conditionsQuery + " ORDER BY score DESC LIMIT 10) AS a"
                    dateTimeScoreQuery += conditionsQuery + " GROUP BY time ORDER BY score DESC LIMIT 10) AS a"
                    dateTimeHelpFullnessQuery += conditionsQuery + " GROUP BY time ORDER BY score DESC LIMIT 10) AS a"

        with connection.cursor() as cursor:
            cursor.execute(mainSQLQuery)
            columns = [col[0] for col in cursor.description]
            dataList = [dict(zip(columns, row)) for row in cursor.fetchall()]

            cursor.execute(countUsersQuery)
            numberOfUsers = cursor.fetchone()

            cursor.execute(maxScoreQuery)
            maxScore = cursor.fetchone()

            cursor.execute(minScoreQuery)
            minScore = cursor.fetchone()

            cursor.execute(promScoreQuery)
            promScore = cursor.fetchone()

            cursor.execute(dateTimeScoreQuery)
            timeScore = cursor.fetchall()

            cursor.execute(dateTimeHelpFullnessQuery)
            timeHelpFullNess = cursor.fetchall()

            data = {"mainInfo":dataList, "numberOfUsers":numberOfUsers, "maxScore":maxScore ,
                    "minScore":minScore, "promScore":promScore, "timeScore":timeScore ,"timeHelpFullNess":timeHelpFullNess}


        return JsonResponse(data)

