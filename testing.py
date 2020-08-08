from flask import Flask, Response, request
from flask_ngrok import run_with_ngrok
import pymongo

client=pymongo.MongoClient()
mydb=client['mydb']

app=Flask(__name__)
run_with_ngrok(app)




@app.route('/webhook',methods=['POST'])
def webhook():
    req=request.get_json(silent=True,force=True)
    coll=mydb[req['session']]
    user=req['queryResult']['queryText']
    bot=req['queryResult']['fulfillmentText']
    data={
    "User":user,
    "Bot":bot,
    }
    coll.insert(data,check_keys=False)
    return Response(status=200)

if __name__=="__main__":
    app.run()