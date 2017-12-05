import re


keywords=input('请输入：')
keywords='>{0}<'.format(keywords)

with open('G:\PythonS6\project1\PyPIMirror.html','r',encoding='utf-8') as f:
    for i in f:
        print('行',i)
        cache=re.findall(keywords,i)
        # print('cache',cache)
        if cache:
            with open('sb','a',encoding='utf-8')as wf:
                wf.write(i)

    print('over')
