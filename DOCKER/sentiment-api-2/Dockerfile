


########################## INITIALIZATION ############################
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
########################## INITIALIZATION ############################

COPY vectorizer.pkl . 
COPY sentimental_model.pkl . 


COPY . . 


EXPOSE 4000
CMD [ "uvicorn", "app:app" ,"--port" , "4000" ,  "--host", "0.0.0.0"   ]





# EXPOSE PORT









#             Push 
#              |                           <-------( Github webhook  )
#              V                                          |
# [  Sentiment-Api , Dockerfile   ] -> git                |
#               ^                                         |
#               |                                         |
#               +------------[ JENKINS ] -----------------+     
#                    -> JSON
#                    {
#                     VM [  ]
#                    }     

