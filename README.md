# trip_destinations_ranking

This is a small project that I did when I was bored. 
I was on a trip with my friend and we were extremely bored in a train trip. We were talking about our next vacation and try to decide were to go. We went through list of all countries in Wikipedia page and we ranked each country with score between 1-10. We thought this would be a good method to determine where to go next.
To make it a little more relevant I wrote this code to scrap data from Wikipedia and try to estimate how expensive each trip would be, based on GDP per capita (we were students back then and we could afford fancy trips).

Logic of code:
1. Reads list of countries with two scores (1 to 10) from csv file.
2. Scrap data of GDP per capita for each country from Wikipedia page and assign some score, the cheaper the better (0 to 5 point to get).
3. Sum the point and sort countries based on summary score.

In recent update I added additional factor - disntace, the futher the location form users origin the less points it gets. 

