comment_list=[

    {"nid":1,"content":"...","Pid":None},
    {"nid":2,"content":"...","Pid":None},
    {"nid":3,"content":"...","Pid":None},
    {"nid":4,"content":"...","Pid":1},
    {"nid":5,"content":"...","Pid":1,},
    {"nid":6,"content":"...","Pid":4,"children_comments":[]},
    {"nid":7,"content":"...","Pid":3,"children_comments":[]},
    {"nid":8,"content":"...","Pid":7,"children_comments":[]},
    {"nid":9,"content":"...","Pid":None,"children_comments":[]},

]

result={}


for comment in comment_list:
    comment['children_comments'] = {}
    if not comment['Pid']:
        result[comment['nid']]=comment
    else:
        for item in comment_list:
            if item['nid']==comment['Pid']:
                item['children_comments'][comment['nid']]=comment
                break



# print(result)




print(result,'\n',temporary)