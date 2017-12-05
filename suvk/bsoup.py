import re,time

from bs4 import BeautifulSoup
import requests
j=40
for num in range(30):
    j+=num
    try:
        htmls = requests.get(url='http://www.jjxsw.com/txt/Kongbu/index_' + str(j) + '.html')

    except Exception:
        continue

    Soup=BeautifulSoup(htmls.text,'html.parser')





    af=Soup.select('#catalog > div > a')

    txtdow='#mainstory > ul > li > a'
    for i in af:
        with open('down', 'a',encoding='utf-8') as tf:
            print(i.get('href'))
            try:
                html = requests.get('http://www.jjxsw.com'+i.get('href'))



                Soup1 = BeautifulSoup(html.text, 'html.parser')
                txta = Soup1.select(txtdow)[0]

                print('txta',txta)
                html2 = requests.get(url='http://www.jjxsw.com' + txta.get('href'))
                print('html2','http://www.jjxsw.com' + txta.get('href'))
                Soup2=BeautifulSoup(html2.text, 'html.parser')
                list1 = Soup2.find_all('a')
            except Exception:
                break
            for i in list1:

                if re.search(r'http://.*\.txt', i.get('href')):
                    tf.write(i.get('href')+'\n')
                    # print('等待1s')
                    # time.sleep(1)



#
'''
313

8
'''