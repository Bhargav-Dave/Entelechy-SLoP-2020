import websiteLogin
from bs4 import BeautifulSoup
import requests


imagesUrl = []

# Author Name and Article Tag
def authorAndTag(soup):
    tags = soup.select(".post-meta a")
    Author = tags[0].text
    Tag = tags[1].text

# title image
def titleImage(soup,articleTitle):
    tag = soup.select(".single-post-thumb img")
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
    titleTag = soup.select("div.erm-title-wrapper")
    articleTitle = titleTag[0].text
    titleImage(soup,articleTitle)

# Like and Dislike of article
def articleLikeDislike(soup):
    tags = soup.select(".entry .ldc-ul_cont span")
    Like = tags[0].text
    DisLike = tags[1].text
    print(Like)
    print(DisLike)

def articleComments(soup):
    tags = soup.select("")


# Article data
def articleContent(soup):
    contentTag = soup.select(".erm-content-wrapper")
    for item in contentTag:
        content = item.text
        print(content)


# Handling Function to scrape Elements of Articles
def articleExtractor(pageSource):
    soup = BeautifulSoup(pageSource,'html.parser')
    # articleLikeDislike(soup)
    getTitleandImage(soup)




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
password = "Entelechy@123"
driver = websiteLogin.Login(username,password)
Edition = "http://entelechy.daiict.ac.in/public_html/entelechy_v2/?tag=edition93&category_name=&author="
getEdition(driver,Edition)

driver.quit()