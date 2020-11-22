import os
import json
from bs4 import BeautifulSoup

with open('entelechy2014.xml', 'r',encoding="utf8") as f: 
    data = f.read() 
# print(data)
data  = BeautifulSoup(data,'lxml')

users = data.find_all(attrs={'name':'yqpg_users'})

# Users
userDict = []
for user in users[1:]:
    uDict = {
        'ID':user.find(attrs={'name':'ID'}).text,
        'user_login':user.find(attrs={'name':'user_login'}).text,
        'user_email':user.find(attrs={'name':'user_email'}).text,
        'display_name':user.find(attrs={'name':'display_name'}).text
    }
    userDict.append(uDict)


# Posts and Pages
articles = data.find_all(attrs={'name':'yqpg_posts'})

articlesDict = []

for article in articles[1:]:
    artDict = {
        'ID': article.find(attrs={'name':'ID'}).text,
        'post_author':article.find(attrs={'name':'post_author'}).text,
        'post_date_gmt':article.find(attrs={'name':'post_date_gmt'}).text,
        'post_content':article.find(attrs={'name':'post_content'}).text,
        'post_title':article.find(attrs={'name':'post_title'}).text,
        'post_excerpt':article.find(attrs={'name':'post_excerpt'}).text,
        'post_status':article.find(attrs={'name':'post_status'}).text,
        'comment_status':article.find(attrs={'name':'comment_status'}).text,
        'post_name':article.find(attrs={'name':'post_name'}).text,
        'post_modified_gmt':article.find(attrs={'name':'post_modified_gmt'}).text,
        'post_parent':article.find(attrs={'name':'post_parent'}).text,
        'guid':article.find(attrs={'name':'guid'}).text,
        'post_type':article.find(attrs={'name':'post_type'}).text,
        'post_mime_type':article.find(attrs={'name':'post_mime_type'}).text,
        'comment_count':article.find(attrs={'name':'comment_count'}).text,
        'like':"",
        'dislike':""
    }
    if artDict['post_parent']=='0':
        artDict['revision'] = []
        artDict['attachment'] = []
        artDict['other']=[]
        articlesDict.append(artDict)
    else:
        for i in range(len(articlesDict)):
            if articlesDict[i]['ID']==artDict['post_parent']:
                if artDict['post_type']=='attachment':
                    articlesDict[i]['attachment'].append(artDict)
                elif artDict['post_type']=='revision':
                    articlesDict[i]['revision'].append(artDict)
                else:
                    articlesDict[i]['other'].append(artDict)


likeDislikes = data.find_all(attrs={'name':'yqpg_like_dislike_counters'})
for likeDislike in likeDislikes[1:]:
    ldlDict = {
        'id':likeDislike.find(attrs={'name':'id'}).text,
        'post_id':likeDislike.find(attrs={'name':'post_id'}).text,
        'ul_key':likeDislike.find(attrs={'name':'ul_key'}).text,
        'ul_value':likeDislike.find(attrs={'name':'ul_value'}).text
    }
    i=0
    for ar in articlesDict:
        if ar['ID'] == ldlDict['post_id']:
            if ldlDict['ul_key']=='like' or ldlDict['ul_key']=='c_like':
                articlesDict[i]['like']=ldlDict['ul_value']
            elif ldlDict['ul_key']=='dislike' or ldlDict['ul_key']=='c_dislike':
                articlesDict[i]['dislike']=ldlDict['ul_value']
            break

parentDirArt = "ArticlesFolder"
try:
    os.mkdir(parentDirArt)
except:
    print("Folder creation error")

parentDirPage = "PagesFolder"
try:
    os.mkdir(parentDirPage)
except:
    print("Pages Folder creation error")

for article in articlesDict:
    if article['post_type']=='post':
        path = os.path.join(parentDirArt,article['ID'])
        try:
            os.mkdir(path)
            with open(os.path.join(path,f"{article['ID']}.json"),"w",encoding='utf-8') as f:
                json.dump(article,f, indent = 5, sort_keys=True,ensure_ascii=False)
        except:
            print(f"Error in folder creation {article['ID']}")
    
    elif article['post_type']=='page':
        path = os.path.join(parentDirPage,article['ID'])
        try:
            os.mkdir(path)
            with open(os.path.join(path,f"{article['ID']}.json"),"w",encoding='utf-8') as f:
                json.dump(article,f, indent = 5, sort_keys=True,ensure_ascii=False)
        except:
            print(f"Error in folder creation {article['ID']}")

# Comments
comments = data.find_all(attrs={'name':'yqpg_comments'})

commentsDict = []

# approved comments
for comment in comments[1:]:
    comDict = {
        'comment_ID':comment.find(attrs={'name':'comment_ID'}).text,
        'comment_post_ID':comment.find(attrs={'name':'comment_post_ID'}).text,
        'comment_date_gmt':comment.find(attrs={'name':'comment_date_gmt'}).text,
        'comment_content':comment.find(attrs={'name':'comment_content'}).text,
        'comment_karma':comment.find(attrs={'name':'commnent_karma'}),
        'comment_parent':comment.find(attrs={'name':'comment_parent'}).text,
        'user_id':comment.find(attrs={'name':'user_id'}).text   
    }
    commentsDict.append(comDict)

# nested comments
def nestedComment(comment,path):
    try:
        direc = os.listdir(path)
    except:
        return False
    for list in direc:
        if list == "comment.json":
            continue
        elif list == comment['comment_parent']:
            # print(f"{comment['comment_ID']} + {list}")
            path1 = os.path.join(path,list)
            path1 = os.path.join(path1,f"{comment['comment_ID']}")
            # print(path1)
            try:
                os.mkdir(path1)
                with open(os.path.join(path1,"comment.json"),"w",encoding='utf-8') as f:
                    json.dump(comment,f, indent = 5, sort_keys=True,ensure_ascii=False)
                return True
            except:
                print(f"Error in folder creation {comment['comment_ID']}")
        else:
            path2 = os.path.join(path,list)
            flag = nestedComment(comment,path2)
            if flag==True:
                return True

    return False


# Filling up comments
for comment in commentsDict:
    if comment['comment_parent']=="0":
        path = os.path.join(parentDirArt,comment['comment_post_ID'])
        path = os.path.join(path,f"{comment['comment_ID']}")
        try:
            os.mkdir(path)
            with open(os.path.join(path,"comment.json"),"w",encoding='utf-8') as f:
                json.dump(comment,f, indent = 5, sort_keys=True,ensure_ascii=False)
        except:
            try:
                path = os.path.join(parentDirPage,comment['comment_post_ID'])
                path = os.path.join(path,f"{comment['comment_ID']}")
                os.mkdir(path)
                with open(os.path.join(path,"comment.json"),"w",encoding='utf-8') as f:
                    json.dump(comment,f, indent = 5, sort_keys=True,ensure_ascii=False)
            except:
                print(f"{comment['comment_ID']} has trouble")

    else:
        path = os.path.join(parentDirArt,comment['comment_post_ID'])
        flag = nestedComment(comment,path)
        if flag==False:
            path = os.path.join(parentDirPage,comment['comment_post_ID'])
            flag = nestedComment(comment,path)


# tags and their relations
terms = data.find_all(attrs={'name':'yqpg_terms'})

termsDict = []

for term in terms[1:]:
    tDict = {
        'term_id': term.find(attrs={'name':'term_id'}).text,
        'name': term.find(attrs={'name':'term_id'}).text,
        'slug':term.find(attrs={'name':'slug'}).text
    }
    termsDict.append(tDict)

termsTaxonomy = data.find_all(attrs={'name':'yqpg_term_taxonomy'})

termsTaxonomyDict = []
categories = []
posttags = []
authors = []
for termTax in termsTaxonomy[1:]:

    ttDict = {
        'term_taxonomy_id' : termTax.find(attrs={'name':'term_taxonomy_id'}).text,
        'term_id' : termTax.find(attrs={'name':'term_id'}).text,
        'taxonomy': termTax.find(attrs={'name':'taxonomy'}).text,
        'description': termTax.find(attrs={'name':'description'}).text,
        'parent': termTax.find(attrs={'name':'parent'}).text,
        'count': termTax.find(attrs={'name':'count'}).text,
        'posts': []
    }
    for tr in termsDict:
        if tr['term_id']==ttDict['term_id']:
            ttDict['name'] = tr['name']
            ttDict['slug'] = tr['slug']
            break

    if ttDict['taxonomy']=='author':
        authors.append(ttDict)
    elif ttDict['taxonomy']=='post_tag':
        posttags.append(ttDict)
    elif ttDict['taxonomy']=='category':
        categories.append(ttDict)
    else:
        termsTaxonomyDict.append(ttDict)

termsRelation = data.find_all(attrs={'name':'yqpg_term_relationships'})

termsRelationDict = []

for termRel in termsRelation[1:]:
    terRel = {
        'object_id':termRel.find(attrs={'name':'object_id'}).text,
        'term_taxonomy_id':termRel.find(attrs={'name':'term_taxonomy_id'}).text
    }
    termsRelationDict.append(terRel)
    flag = False
    i=0
    for ca in categories:
        if ca['term_taxonomy_id']==terRel['term_taxonomy_id']:
            flag = True
            categories[i]['posts'].append(terRel['object_id'])
            break
        i+=1
    if flag==True:
        continue
    i=0
    for ca in posttags:
        if ca['term_taxonomy_id']==terRel['term_taxonomy_id']:
            flag = True
            posttags[i]['posts'].append(terRel['object_id'])
            break
        i+=1

    if flag==True:
        continue
    
    i=0
    for ca in authors:
        if ca['term_taxonomy_id']==terRel['term_taxonomy_id']:
            flag = True
            authors[i]['posts'].append(terRel['object_id'])
            break
        i+=1

os.mkdir('Config')
with open(os.path.join("Config","categories.json"),"w") as f:
    json.dump(categories,f, indent = 5, sort_keys=True,ensure_ascii=False)
with open(os.path.join("Config","postTags.json"),"w") as f:
    json.dump(posttags,f, indent = 5, sort_keys=True,ensure_ascii=False)

os.mkdir('Edition')
for pt in posttags:
    if pt['slug'][:7]=='edition':
        with open(os.path.join("Edition",f"{pt['name']}.json"),"w") as f:
            json.dump(pt,f, indent = 5, sort_keys=True,ensure_ascii=False)

for au in authors:
    s = au['description'].split(' ')
    for us in userDict:
        if us['ID']==s[len(s)-2]:
            us['description']=au['description']
            us['count']=au['count']
            us['name']=au['name']
            us['slug']=au['slug']
            break

with open(os.path.join("Config","users.json"),"w") as f:
    json.dump(userDict,f, indent = 5, sort_keys=True)