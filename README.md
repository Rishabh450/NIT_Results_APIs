# NIT_JSR_Result_Portal
Tools used:
## Python: Language
## BeautifulSoup : for web scrapping
## Docker : to create image of api
## heroku: for deploying the image
## flask : Rest API

A Restful api build in flask. Just enter your roll and get your result
This api is developed to fetch results of NIT JSR Students.

How to use the api :
routes.
All the routes are POST type.

1) https://nit-jsr-results.herokuapp.com/api/profile 
   example :
   {
      "roll":"2018ugcs021"
   }
   
2) https://nit-jsr-results.herokuapp.com/api/cgpa 
   example :
   {
      "roll":"2018ugcs021"
   }
   
3)  https://nit-jsr-results.herokuapp.com/api/results
   example :
   {
      "roll":"2018ugcs021"
   } 

4)  https://nit-jsr-results.herokuapp.com/api/rank
   example :
   {
      "roll":"2018ugcs021",
      "semester":"2",
      "method":"sgpa",
   }     
   
   
