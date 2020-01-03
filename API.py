from flask import Flask , jsonify
from flask_restful import reqparse, abort, Api, Resource
import os ,json
import numpy as np 
import keras

app = Flask(__name__)
api = Api(app)

file_path  = "hotels_noindex.csv"

class job_function_predictor(Resource):
    #same row embedding function used for the dataset
    
    def embed_title(embedding_dict, job_title):
        title_vectors =np.zeros(shape=(10,300))
        if job_title is not None: 
            title_parts = job_title.split()
            print("job_title parts :",title_parts)
            for i , word  in enumerate(title_parts) :
            try:
                temp = list(embedding_dict[word])
                if temp == []:
                try :
                    # value used before , check backup
                    temp = self.backup_dict[word]
                    title_vectors[i] = temp
                except Exception as e:
                    # not used but not in the dictionary ,will stay as a zero vector 
                    print (i," skipped : ",word ," Reason:" ,e )
                else: 
                # first usage , add to backup 
                backup_dict[word] = temp 
                title_vectors[i] = temp 
            except Exception as e:
                print("no embedding for : ",e)    
        
        else: 
            print("title is null", job_title)   
        return title_vectors , backup_dict

    def character_removal(text):
        charlist = "|&()[],\'\"-=+@/\\"
        for c in charlist : 
            text = text.replace(c,' ')
        return text      

    def func_numto_jobFun(rev_funcdict ,jobFunctions_numbers):
        function_names = []
        for fun_number in jobFunctions_numbers: 
            function_names.append(rev_funcdict[fun_number])
        return function_names    

    def get(self, job_title):
        job_title = self.character_removal(job_title)
        X, self.backup_dict = self.embed_title(embedding_dict, job_title, self.backup_dict)
        X = X.reshape(shape=(1,10,300))
        result = model.predict(X)
        jobFunctions = self.func_numto_jobFun(rev_funcdict,result[0])
        print ("not emplemented") , 500
    


def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data


def load_models():
    rev_funcdict = np.load("rev_dictFun.npy")
    model = keras.models.load("model_1.h5") 
    backup_dict = {}
    # this line will take a minute an will fill a lot of memory as the vectors file is really big 
    embedding_dict = load_vectors("wiki-news-300d-1M-subword.vec") 

    return embedding_dict, rev_funcdict, model , backup_dict

URLs_job_function_predictor= "/predictor/<job_title>"
api.add_resource(job_function_predictor,URLs_job_function_predictor)


if __name__ == '__main__':
    # load model ,rev dict, load fastText vectors
    embedding_dict , rev_funcdict, model , backup_dict = load_models()
    
    app.run(debug=True)   # change before final upload 