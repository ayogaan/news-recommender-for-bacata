from flask import Flask, request, jsonify, render_template
import pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from flask import jsonify
import pandas as pd
import numpy as np
app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fanfanfan'
app.config['MYSQL_DB'] = 'berita'
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tes', methods=['POST'])
def tes():
    return "asu"


"""@app.route('/predict', methods=['POST'])
def predict():
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
    stopw = open("stopword.txt", "r")
    listofword = []
    for line in stopw:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        listofword.append(line_list)
    stopw.close()

    message = request.json['message']
    inform = message
    
    for i in listofword:
        inform = inform.replace(' '+i[0]+' ', ' ')
        inform = inform.replace("  ", ' ')
    
    q =stemmer.stem(inform)
    
    toStore = "["
    for i in symbols:
         q = q.replace(i, '')
    berita = q.split()       
    
    for y in berita:
        toStore+="'"+y+"',"
    l = len(toStore)
    toStore = toStore[:l-1]
    toStore+="]"

    anjai = [toStore]
    
    vectorizer = CountVectorizer(max_features=1000)
 #   X = vectorizer.fit_transform(anjai).toarray()
#   tfidfconverter = TfidfTransformer()
#    X = tfidfconverter.fit_transform(X).toarray()
#    tf_vectorizer = CountVectorizer()
#    X = tf_vectorizer.fit_transform(anjai).toarray()
#    my_prediction = model.predict(X)
 

    X = vectorizer.fit_transform(anjai).toarray()
    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()
    print(len(X[0]))
    for i in range((1000-len(X[0]))):
        X = np.append(X, 0)


    my_prediction = model.predict([
        X])
    return jsonify(
        response_code=200,
        category=my_prediction[0]
    )
    """

@app.route('/preprocess', methods=['POST'])
def preprocess():
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~1234567890\n"
    stopw = open("stopword.txt", "r")
    listofword = []
    for line in stopw:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        listofword.append(line_list)
    stopw.close()

    message = request.json['message']
         
    inform = message
    
    for i in listofword:
        inform = inform.replace(' '+i[0]+' ', ' ')
        inform = inform.replace("  ", ' ')
    
    q =stemmer.stem(inform)
    
    toStore = "["
    for i in symbols:
         q = q.replace(i, '')
    berita = q.split()       
    
    for y in berita:
        toStore+="'"+y+"',"
    l = len(toStore)

    toStore = toStore[:l-1]
    toStore+="]"
    print(toStore)
    data = {
        "text" : toStore
    }
    return jsonify(data)

@app.route('/suggest', methods=["POST"])
def suggest():
    #user_id = request.json['user_id']
    latest = request.json['latest']
    print("latest : ")
    print(latest)
    news = []
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM vocabs")
    words = cur.fetchall()
    for x in words:
        
        news.append(x[2])
    
   
    #get latest position
    latest_pos = []
    print(latest)
    for i in latest:
        query = "SELECT * FROM vocabs where article_id ="+str(i[0])
        print(query)
        cur.execute(query)
        x = cur.fetchall()
        print(words.index(x[0]))
        latest_pos.append(words.index(x[0]))
       
        
        
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer()
    tfidf_movieid = tfidf.fit_transform((news))
    from sklearn.metrics.pairwise import cosine_similarity
    cos_sim= cosine_similarity(tfidf_movieid, tfidf_movieid)


    recommended_movies = []
    top_10_movies = []
    for i in latest_pos:
        similarity_scores = pd.Series(cos_sim[i]).sort_values(ascending = False)
        top_10_movies += list(similarity_scores.iloc[0:3].index)
        print(top_10_movies)
    recommended = list( dict.fromkeys(top_10_movies)) 
    recommended_news = []

    for i in recommended:
        recommended_news.append(words[i][1])
    #for i in recommended:
    #    cur.execute("INSERT INTO recommended(user_id, article_id) VALUES (%s, %s)", (user_id, words[i][1]))
    #    mysql.connection.commit()   
#insert
    print(recommended_news)
    data = {
        "recommended_news" : recommended_news
    }
    return jsonify(data)
app.run(host='0.0.0.0', port=5000)

