from django.shortcuts import render,HttpResponse

# Create your views here.
def test(request):

    return render(request,'test.html')



def moupsum(request):
    itms=request.GET
    print(itms.get('x1'))
    data=int(itms.get('x1'))+int(itms.get('x2'))
    return HttpResponse(data)



def getsome(request):
    a=request.POST


    return HttpResponse('OK')


def filetest(request):
    if request.method=='GET':
        return render(request,'filestest.html')
    print('POST',request.POST)
    print('FILES',request.FILES)
    file_obj=request.FILES.get('icon')
    with open(file_obj.name,'wb') as f:
        for i in file_obj:
            f.write(i)
    return HttpResponse('上次成功')



def upload(request):
    pass