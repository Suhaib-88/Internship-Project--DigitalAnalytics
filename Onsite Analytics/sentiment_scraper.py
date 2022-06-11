import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

class Sentiment:
    def __init__(self,df_recommendations):
        self.df_recommendations=df_recommendations
        

    def resp(self,url):
        response=requests.get(url).content
        souper=BeautifulSoup(response,'html.parser')
        return souper


    def get_sentiments_data(self,data):
        comment=[]
        names=[]
        review=[]
        dates=[]
        prod_id=[]
        description=[]
        n_comments=[]
        for i in range(len(data.index)):
            try:

                soups=self.resp(data['product_link'][i])
                number=soups.find_all(class_="comment_container")
                n_comments.append(len(number))
                
                for i in soups.find_all(class_="description"):
                    if i.has_attr( "class" ):
                        if len( i['class'] ) != 2:
                            description.append(i.text)     #review description
                
                
                for tag in soups.find_all(class_="comment_container"):              #comment ids
                    comment.append(tag.get('id'))
                            
                names_list=soups.find_all(class_="woocommerce-review__author")           # names of user
                for i in range(len(names_list)):
                    names.append(names_list[i].text)
                
                reviews_list=soups.find_all("div",{"class":"comment-text"})             #ratings
                for i in range(len(reviews_list)):
                    review.append(reviews_list[i].text[:18])

                dates_list=soups.find_all("time",{"class":"woocommerce-review__published-date"})      #date
                for i in range(len(dates_list)):
                    dates.append(dates_list[i].text)
                
                
            except:
                print(i)

        d=pd.DataFrame({"ReviewDate":dates,"Comment_id":comment,"ReviewDesc":description,"ReviewerName":names,"Rating":review})
        senti=d.to_csv('sentiment.csv',index=False)
        return data, senti


    #forgot to append product ids and product name now going to add them to our data 
    def prod_name_data(self,senti):
        prod_names=self.df_recommendations.product_name * senti['comments_no.']
        prod_names=prod_names.to_frame()
        prod_names=prod_names[prod_names[0]!=''].reset_index(drop=True)
        return prod_names

    def prod_id_data(self,senti):
        prod_ids=self.df_recommendations.product_ids * senti['comments_no.']
        prod_ids=prod_ids.to_frame()
        prod_ids=prod_ids[prod_ids[0]!=''].reset_index(drop=True)
        return prod_ids


    def get_product_names_ids(self,prod_ids,prod_names,senti):
        product_id=[]
        product_name=[]
        def splitstring(string):
            match= re.match(r'(.*?)(?:\1)*$', string)
            word= match.group(1)
            return [word] * (len(string)//len(word))

        try:
            
            for i in range(len(prod_ids.index)):
                product_id.extend(splitstring(prod_ids.loc[i,0]))
            
            for i in range(len(prod_names.index)):
                product_name.extend(splitstring(prod_names.loc[i,0]))
            
            senti['Product_ids']=product_id
            senti['product_name']=product_name

        except:
            print(i)
            pass
        
    
