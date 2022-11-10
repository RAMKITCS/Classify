import time,os,sys,re,io
import numpy as np
import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer,word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score
import joblib
stop = stopwords.words('english')
def clean(text):
    word_lem=WordNetLemmatizer()
    tokens=word_tokenize(text)
    lower=[word.lower() for word in tokens if len(word)>2 and word.isalpha() and word not in stop]
    lemmatized_text=[word_lem.lemmatize(word) for word in lower]
    return lemmatized_text
def vectorize(data,tfidf_vect_fit):
    x_tfidf=tfidf_vect_fit.transform(data)
    x_tfidf_df=pd.DataFrame(x_tfidf.todense(),columns=tfidf_vect_fit.get_feature_names())
    return x_tfidf_df
def Predict(path):
    st=time.time()
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('stopwords')
    try:
        from gcsconnect import read_file_io,write_file_io,write_file
        df=pd.read_excel(read_file_io("Classification/Dataset/data.xlsx"),dtype=str)
        df=df.append(df)
        df=df.append(df)
        df.dropna(subset=["data","label"],inplace=True)
        X_train,X_test,Y_train,Y_test=train_test_split(df["data"],df["label"],test_size=0.01)
        tfidf_vect=TfidfVectorizer(analyzer=clean,use_idf=True,max_features=1000)
        tfidf_vect_fit=tfidf_vect.fit(X_train.values.astype('U'))
        tfidf_byt=io.BytesIO()
        joblib.dump(tfidf_vect_fit,tfidf_byt)
        tfidf_byt.seek(0)
        write_file_io("Classification/Models/tfidf.pkl",tfidf_byt)
        del tfidf_byt
        X_train=vectorize(X_train.values.astype('U'),tfidf_vect_fit)
        model=RandomForestClassifier(n_jobs=-1,n_estimators=100)
        model.fit(X_train,Y_train)
        model_byte=io.BytesIO()
        joblib.dump(model,model_byte,compress=3)
        model_byte.seek(0)
        write_file_io("Classification/Models/model.pkl",model_byte)
        del model_byte
        y_pred=model.predict(vectorize(X_test,tfidf_vect_fit))
        print("Accuracy",round(accuracy_score(Y_test,y_pred),3))
        print(time.time()-st)
        write_file("Classification/Models/status.txt","1")
        print(Y_test)
        a=[]
        b=[]
        df=pd.read_excel("newdata2.xlsx",dtype=str)
        #model=dtree
        for i in range(len(df["data"])):
            ocr_data=df["data"][i]
            df2=pd.DataFrame({"data":[ocr_data]},dtype=str)
            pred_value=model.predict(vectorize(df2["data"].values.astype('U'),tfidf_vect_fit))
            pred_prob=model.predict_proba(vectorize(df2["data"].values.astype('U'),tfidf_vect_fit))
            a.append(pred_value[0])
            b.append(pred_prob[0].max())
        print(a,b)
        return "Completed"
    except Exception as e:
        print("Model Train error:",str(e))
        return str(e)
#Predict("")