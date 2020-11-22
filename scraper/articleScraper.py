import websiteLogin
from bs4 import BeautifulSoup
import requests
import os

imagesUrl = []

# Author Name and Article Tag
def authorAndTag(soup):
    tags = soup.select(".content .post-meta a")
    Author = tags[0].text
    Tag = tags[1].text

# title image
def titleImage(soup,articleTitle):
    tag = soup.select(".content .single-post-thumb img")
    imageUrl = tag[0].get('src')
    if imageUrl == None:
        return
    imageName = articleTitle+'_title.jpeg'
    image = None
    for i in range(5):
        try:
            image = requests.get(imageUrl)
            break
        except:
            image = None
    
    if image == None:
        imagesUrl.append(imageUrl)
    
    open(imageName,'wb').write(image.content)

# Article Title
def getTitleandImage(soup):
    titleTag = soup.select(".content div.erm-title-wrapper")
    articleTitle = titleTag[0].text
    titleImage(soup,articleTitle)

def articleMedia(soup):
    images = soup.select(".content .entry .attachment-thumbnail")
    # print(images)
    os.mkdir('Images')
    i=0
    for image in images:
        i+=1
        link = image.get('src')
        if link == None:
            continue
        ima = None
        for j in range(5):
            try:
                ima = requests.get(link)
                break
            except:
                ima = None

        if ima == None:
            print(link)
            continue

        ## have to handle get error
        imageName = "image-"+str(i) + ".jpeg"
        open(os.path.join("Images",imageName),'wb').write(ima.content)

        
# Like and Dislike of article
def articleLikeDislike(soup):
    tags = soup.select(".content .entry .ldc-ul_cont span")
    Like = tags[0].text
    DisLike = tags[1].text
    print(Like)
    print(DisLike)

def articleComments(soup,):#query selector
    tags = soup.select(".content .commentlist .comment")
    for item in tags:
        author = item.select(".author-comment cite.fn")
        author = author[0].text
        date = item.select(".author-comment .comment-meta a")
        date = date[0].text
        content = item.select(".comment-content p")
        content = content[0].text
        ldl = item.select(".comment-content .ldc-cmt-box span.ldc-ul_cont span")
        like = ldl[0].text
        dislike = ldl[1].text
        print(author)
        print(date)
        print(content)
        print(like)
        print(dislike)
        # print(item)


# Article data
def articleContent(soup):
    contentTag = soup.select(".content .erm-content-wrapper")
    articleMedia(soup)
    for item in contentTag:
        content = item.text
        print(content)


# Handling Function to scrape Elements of Articles
def articleExtractor(pageSource):
    soup = BeautifulSoup(pageSource,'html.parser')
    # articleLikeDislike(soup)
    getTitleandImage(soup)
    # articleContent(soup)
    # articleMedia(soup)
    # articleComments(soup)




# Extract all the articles from Each edition
def getEdition(driver,Edition):
    driver.get(Edition)
    Element = driver.find_elements_by_css_selector("article > h2 > a")
    articleLink = [Element.get_attribute('href') for Element in Element]

    pages = driver.find_elements_by_css_selector(".page")
    pages = [pages.get_attribute('href') for pages in pages]

    for page in pages:
        driver.get(page)
        linkpage = driver.find_elements_by_css_selector("article > h2 >a")
        linkpage = [linkpage.get_attribute('href') for linkpage in linkpage]
        articleLink = articleLink+linkpage

    driver.get(articleLink[0])
    articleExtractor(driver.page_source)
    # for i in range(len(articleLink)):
    #     # print(articleLink[i])
    #     driver.get(articleLink[i])
    #     articleExtractor(driver.page_source)
    




username = "harsh8221"
password = ""
driver = websiteLogin.Login(username,password)
Edition = "http://entelechy.daiict.ac.in/public_html/entelechy_v2/?tag=edition93&category_name=&author="
getEdition(driver,Edition)

driver.quit()