from bs4 import BeautifulSoup


def filter_xss(html_str):
    valid_tag_list=["p", "div", "a", "img", "html", "body", "br", "strong", "b",'h1','h2','h3','h4','h5','span','hr']


    valid_dict={'p':['id','class']}




    soup=BeautifulSoup(html_str,'html.parser')

    for ele in soup.find_all():
        if ele.name not in valid_tag_list:
            ele.decompose()
        else:
            attrs=ele.attrs
            l=[]
            for k  in attrs:
                if k not  in valid_dict[ele.name]:
                    l.append(k)
                for i in l:
                    del attrs[i]

    return soup.decode()