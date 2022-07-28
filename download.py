from bs4 import BeautifulSoup
import requests


domain = 'https://nasagrace.unl.edu'

url = 'https://nasagrace.unl.edu/globaldata/'



page  = requests.get(url)

soup = BeautifulSoup(page.text,'lxml')

adata =  soup.find_all('a')

#print(adata)

for link in adata:
    
    ncurl = domain + link.get('href')
    
    if "/globaldata/20" in ncurl:
        ncurl_ID = ncurl.split('/')[4][0:4]
        
        
        if ncurl_ID >= '2015':
            
            #print(ncurl_ID)
            
            ncurl_data = domain + link.get('href')
            
            ncpage = requests.get(ncurl_data)
            
            ncsoup = BeautifulSoup(ncpage.text,"html.parser")
            
            for directory in ncsoup.find_all('a'):
                final_url = directory.get('href')
                
                if ".nc4" in final_url:
                    print(final_url)
                    
                    filename = final_url.split("/GRACE",1)[1]
                    
                    with open(filename, 'wb') as file:
                        response = requests.get(domain + final_url)
                        file.write(response.content)
                    
                    
                else:
                    continue
 
        else:
            continue
            
            
            
    else:
        continue

    


    
    
   
    
    


            