from django.db import models
from django.contrib.auth.models import User
class category(models.Model):
    category_name = models.CharField(max_length=250)
    sub_cat = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    icon = models.CharField(max_length=250,blank=True)
    color = models.CharField(max_length=200,blank=True)
    create_date = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.category_name

class register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact = models.IntegerField(blank=True)
    profile_pic = models.ImageField(upload_to="register/%Y/%m/%d")
    registred_on_date = models.DateField(auto_now_add=True)
    registred_on_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class postadd(models.Model):
    user = models.ForeignKey(register,on_delete=models.CASCADE)
    category_name=models.CharField(max_length=250,blank=True)
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    description= models.TextField(blank=True)
    img1 = models.ImageField(upload_to="adds/%Y/%m/%d",blank=True,null=True)
    img2 = models.ImageField(upload_to="adds/%Y/%m/%d",blank=True,null=True)
    img3 = models.ImageField(upload_to="adds/%Y/%m/%d",blank=True,null=True)
    img4 = models.ImageField(upload_to="adds/%Y/%m/%d",blank=True,null=True)
    city = models.CharField(max_length=250,blank=True)
    status = models.BooleanField(default=True)
    views = models.IntegerField(null=True,default=0,blank=True)
    on_date = models.DateField(auto_now_add=True)
    on_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class contactus(models.Model):
    name = models.CharField(max_length=250,blank=True)
    email = models.EmailField(max_length=250,blank=True)
    contact = models.IntegerField()
    msz = models.TextField()
    on_date = models.DateField(auto_now_add=True)
    on_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
