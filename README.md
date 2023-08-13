# trip_destinations_ranking

This is a small project that I did when I was bored. 
I was on a trip with my friend and we were extremely bored in a train trip. We were talking about our next vacation and try to decide were to go. We went through list of all countries in Wikipedia page and we ranked each country with score between 1-10. We thought this would be a good method to determine where to go next.
To make it a little more relevant I wrote this code to scrap data from Wikipedia and try to estimate how expensive each trip would be, based on GDP per capita (we were students back then and we could afford fancy trips).

Logic of code:
-reads list of countries with two scores (1~10) from csv file, uploaded file has all scores set to 5 :),
-scrap data of GDP per capita for each country from Wikipedia page and assign some score, the cheaper the better (0~5 point to get),
-sum the point and sort countries based on summary score.

In future I think to add new parameter that estimates distance of the trip.

