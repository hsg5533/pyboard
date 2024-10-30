from django.shortcuts import render,redirect
from board.models import Board, Comment, Movie
from django.views.decorators.csrf import csrf_exempt
import os
import math
from django.db.models import Q
#from django.utils.http import urlquote
from django.http.response import HttpResponse, HttpResponseRedirect
from board import BigdataPro
from django.db.models.aggregates import Avg
import pandas as pd
import numpy as np
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
UPLOAD_DIR='c:/pgm/upload/'

# def list(request):
#     boardCount=Board.objects.count()
#     boardList=Board.objects.all().order_by("-idx")
#     return render(request,'board/list.html',
#                   {'boardList':boardList,'boardCount':boardCount})
def home(request):
    return render(request,'main.html')

def signup_form(request):
    return render(request,'user/signup.html')

@csrf_exempt
def signup(request):
    if request.method=='POST':
      if request.POST['password']==request.POST['password2']:
            username=request.POST['username']
            password=request.POST['password']
            email=request.POST['email']
            user=User.objects.create_user(username,email,password)
            return redirect('/login_form/')
    return render(request,'user/signup.html')

def login_form(request):
    return render(request, 'user/login.html')

@csrf_exempt
def login(request):
    if request.method == "POST":
        un = request.POST['username']
        pw = request.POST['password']
        #auth.authenticate 라는 말은 DB에서 방금전에 입력한 이 내용이 우리한테 있는 회원명단이 맞는지 확인시켜주는 함수
        user = auth.authenticate(request, username=un, password=pw)
        print("aaa11111111111111111",user)
        
        if user is not None:    # is not None = None이 아니라면 = 회원이라면
            print('aaaaaaaaaaaaaaaaaa')
            auth.login(request,user)
            return redirect('/list/')
        else:
            print('bbbbbbbbbbbbbbb')
            return render(request, 'user/login.html', {'error': 'username or password is incorrect'})
            
            
            
    else:
        print('ccccccccccccccccc')
        return render(request, 'user/login.html') 
    
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    return render(request,'user/login.html')
   

def movie_save(request):
    data=[]
    BigdataPro.movie_crawling(data)
    for row in data:
        dto=Movie(title=row[0],point=row[1],content=row[2])
        dto.save()
    return redirect('/')

def chart(request):
    data=Movie.objects.values('title').annotate(point_avg=Avg('point')).order_by('point_avg')[50:60]
    df=pd.DataFrame(data)
    BigdataPro.makeGraph(df.title, df.point_avg)
    return render(request,'bigdata_pro/chart.html',{'data':data})

def wordcloud(request):
    content=Movie.objects.values('content')
    df=pd.DataFrame(content)
    BigdataPro.makeWordCloud(df.content)
    return render(request,'bigdata_pro/wordcloud.html',{'content':df.content})

def cctv_map(request):
    BigdataPro.cctv_map()
    return render(request,'map/map01.html')

@csrf_exempt
def list(request):
    try:
        search_option=request.POST['search_option']
    except:
        search_option=''
        
    try:
        search=request.POST['search']
    except:
        search=''
        
    if search_option=='all':
        boardCount=Board.objects.filter(Q(writer__contains=search)
                                        |Q(title__contains=search)
                                        |Q(content__contains=search)).count()
    elif search_option=='writer':
        boardCount=Board.objects.filter(Q(writer__contains=search)).count()
        
    elif search_option=='title':
        boardCount=Board.objects.filter(Q(title__contains=search)).count()
    elif search_option=='cotent':
        boardCount=Board.objects.filter(Q(content__contains=search)).count()    
    else:   
        boardCount=Board.objects.count()
        
    try:
        start=int(request.GET['start'])
    except:
        start=0
    
    page_size=5
    block_size=5
    
    end=start+page_size
    
    total_page=math.ceil(boardCount/page_size)
    current_page=math.ceil((start+1)/page_size)
    start_page=math.floor((current_page-1)/block_size)*block_size+1
    end_page=start_page+block_size-1
    
    print('total_page:',total_page)
    print('current:',current_page)
    print('start_page:',start_page)
    print('end_page:',end_page)
    
    if end_page > total_page:
        end_page=total_page
        
    if start_page >= block_size:
        prev_list=(start_page-2)*page_size
    else:
        prev_list=0
    
    if end_page <total_page:
        next_list=end_page*page_size
    else:
        next_list=0
    
    if search_option=='all':
        boardList=Board.objects.filter(Q(writer__contains=search)
                                        |Q(title__contains=search)
                                        |Q(content__contains=search)).order_by("-idx")[start:end]
    elif search_option=='writer':
        boardList=Board.objects.filter(Q(writer__contains=search)).order_by("-idx")[start:end]
    elif search_option=='title':
        boardList=Board.objects.filter(Q(title__contains=search)).order_by("-idx")[start:end]
    elif search_option=='content':
        boardList=Board.objects.filter(Q(content__contains=search)).order_by("-idx")[start:end]
    else:    
        boardList=Board.objects.all().order_by("-idx")[start:end]
        
    links=[]
    for i in range(start_page, end_page+1):
        page_start=(i-1)*page_size
        links.append("<a href='/list/?start="+str(page_start)+"'>"+str(i)+"</a>")
           
    return render(request,'board/list.html',
                  {'boardList':boardList,
                   'boardCount':boardCount,
                   "search_option":search_option,
                   "search":search,
                   "range":range(start_page-1, end_page),
                   "start_page":start_page,
                   "end_page":end_page,
                   "block_size":block_size,
                   "total_page":total_page,
                   "prev_list":prev_list,
                   "next_list":next_list,
                   "links":links
                   })
    

@login_required
def write(request):
    return render(request, 'board/write.html')

@csrf_exempt
def insert(request):
    fname=''
    fsize=0
    
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fsize=file.size
        print(fsize)
        
        fp=open("%s%s"%(UPLOAD_DIR, fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    w=request.POST['writer']
    t=request.POST['title']
    c=request.POST['content']
   
    dto=Board(writer=w, title=t, content=c, filename=fname,filesize=fsize)
    dto.save()
    return redirect('/list/')

def download(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    path=UPLOAD_DIR+dto.filename
    filename=os.path.basename(path)
    #filename=urlquote(filename)
    with open(path,'rb') as file:
        response=HttpResponse(file.read(),content_type='application/octet-stream')
        response['Content-Disposition']="attachment;filename*=UTF-8''{0}".format(filename)
        
        dto.down_up()
        dto.save()
        return response
    
def detail(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    commentList=Comment.objects.filter(board_idx=id).order_by('idx')
    filesize="%.2f" %(dto.filesize)
    return render(request,"board/detail.html",
                  {'dto':dto,
                   'filesize':filesize,
                   'commentList':commentList})
        
@csrf_exempt                          
def update(request):
    id=request.POST['idx']
    dto_src=Board.objects.get(idx=id)
    fname=dto_src.filename
    fsize=dto_src.filesize
    
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fp=open('%s%s' %(UPLOAD_DIR,fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        fsize=os.path.getsize(UPLOAD_DIR+fname)
    dto_new=Board(idx=id,
                  writer=request.POST['writer'],
                  title=request.POST['title'],
                  content=request.POST['content'],
                  filename=fname, filesize=fsize)
    dto_new.save()
    return redirect("/list/")

@csrf_exempt
def delete(request):
    id=request.POST['idx']
    Board.objects.get(idx=id).delete()
    return redirect("/list/")

@csrf_exempt
def reply_insert(request):
    id=request.POST['idx']
    dto=Comment(board_idx=id,
               writer=request.POST['writer'],
               content=request.POST['content'])
    dto.save()
    return HttpResponseRedirect("/detail?idx="+id)
    
    





