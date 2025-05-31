from django.shortcuts import render
from mysite.models import category, register, postadd, contactus
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm

all_categories = category.objects.all().order_by('category_name')

recent_adds = postadd.objects.all().order_by('-id')
first = postadd.objects.all().order_by('id')[:4]
all_adds = postadd.objects.all().order_by('-id')
data = ''
def index(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            data = register.objects.get(user__username=request.user.username)
            return render(request,'index.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'profile':data})
    return render(request,'index.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first})

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        em = request.POST['email']
        pas = request.POST['password']
        con = request.POST['contact']

        check = User.objects.filter(username=name)
        if len(check)>=1:
            return render(request,'register.html',{'status':'A User with this name Already exists!!!'})
        else:
            user = User.objects.create_user(em,em,pas)
            user.first_name = name
            user.save()

            profile = register(user=user,contact=con)
            profile.save()
            if 'profile_pic' in request.FILES:
                pp = request.FILES['profile_pic']
                profile.profile_pic = pp
                profile.save()
            return render(request,'register.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'status':'Account created Successfully, Thanks for registration'})
    return render(request,'register.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first})

def uservalid(request):
    if request.method=='GET':
        if 'username' in request.GET:
            un = request.GET['username']
            check = User.objects.filter(username=un)
            if(len(check)>0):
                return HttpResponse('A user with this name already exists')
            else:
                return HttpResponse('Success')

def signin(request):
    if "st" in request.GET:
        return render(request,'login.html',{'st':'You Need To Login First','cat':all_categories,'recents':recent_adds[:4],'first':first})
    
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                res = HttpResponseRedirect('/')
                if 'remember' in request.POST:
                    res.set_cookie('userid',user.id)
                return res
            return render(request,'login.html',{'status':'Sorry you are not allowed','cat':all_categories,'recents':recent_adds[:4],'first':first})
        else:
            return render(request,'login.html',{'status':'Invalid Login Details','cat':all_categories,'recents':recent_adds[:4],'first':first})
    return render(request,'login.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first})

def post_add(request):
    profile = register.objects.get(user__username=request.user.username)
    if profile.user.is_superuser:
        return render(request,'post-ad.html',{'cat':all_categories,'profile':profile,'admin':'You are not allowed here!!'})
    if request.method=="POST":
        cat = request.POST['category']
        tit = request.POST['title']
        desc = request.POST['desc']
        name = request.POST['name']
        cont = request.POST['contact']
        city = request.POST['city']
        price = request.POST['price']
        img1 = request.FILES['image1']
        img2 = request.FILES['image2']
        img3 = request.FILES['image3']
        img4 = request.FILES['image4']

        add = postadd(user=profile,category_name=cat,title=tit,description=desc,city=city,price=price,img1=img1,img2=img2,img3=img3,img4=img4)
        add.save()
        id = add.id

        profile.user.first_name=name
        profile.contact = cont
        profile.save()
        return render(request,'post-ad.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'profile':profile,'status':'Add Posted Successfully','sid':id})
    return render(request,'post-ad.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'profile':profile})

def single_product(request):
    id = request.GET['id']
    pp = postadd.objects.get(pk=id)
    pp.views = pp.views+1
    pp.save()
    product= {
        'id':pp.id,
        'title':pp.title,
        'cat':pp.category_name,
        'desc':pp.description.split('@'),
        'price':pp.price,
        'img1':pp.img1,
        'img2':pp.img2,
        'img3':pp.img3,
        'img4':pp.img4,
        'city':pp.city,
        'status':pp.status,
        'date':pp.on_date,
        'time':pp.on_time,
        'user':pp.user,
        'views':pp.views,
    }
    return render(request,'single.html',{'product':product,'cat':all_categories,'recents':recent_adds[:4],'first':first})

def categories(request):
    return render(request,'categories.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'adds':all_adds})

def all_classifieds(request):
    total=len(all_adds)
    if 'keyword' in request.GET:
        t = request.GET['keyword']
        data = postadd.objects.filter(title__contains=t)|postadd.objects.filter(city__contains=t)|postadd.objects.filter(category_name__contains=t)
        total = len(data)
        return render(request,'all-classifieds.html',{'cat':all_categories,'adds':data,'featured':recent_adds[:3],'total':total})

    return render(request,'all-classifieds.html',{'cat':all_categories,'adds':all_adds,'featured':recent_adds[:3]})

def products(request):
    name = request.GET['name']
    total = len(postadd.objects.filter(category_name=name))
    return HttpResponse(total)
def contact(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            data = register.objects.get(user__username=request.user.username)
            madds = postadd.objects.filter(user__user__username=request.user.username)
            return render(request,'myadds.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'profile':data})
    if request.method == "POST":
        name = request.POST['name']
        em = request.POST['email']
        con = request.POST['contact']
        msg = request.POST['msg']

        data = contactus(name=name,email=em,contact=con,msz=msg)
        data.save()
        return render(request,'contact.html',{'status':'Thanks for your feedback!!!','cat':all_categories,'recents':recent_adds[:4],'first':first})
    return render(request,'contact.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first})

def uslogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def myadds(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            data = register.objects.get(user__username=request.user.username)
            madds = postadd.objects.filter(user__user__username=request.user.username).order_by('-id')
            return render(request,'myadds.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first,'profile':data,'adds':madds})
    return render(request,'myadds.html',{'cat':all_categories,'recents':recent_adds[:4],'first':first})

def delete_add(request):
    if "id" in request.GET:
        id = request.GET['id']
        add = postadd.objects.get(id=id)
        add.delete()
        return HttpResponseRedirect('/  mysite/myadds')
    
def my_profile_view(request):
    profile = ProfileForm.objects.get(user=request.user)
    return render(request, 'my_profile.html', {'profile': profile})


from django.shortcuts import render, redirect
# from .form import ProfileForm

def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'mysite/update_profile.html', {'form': form})