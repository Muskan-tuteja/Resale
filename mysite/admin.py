from django.contrib import admin


from mysite.models import category, register, postadd, contactus

class categoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','sub_cat','icon','color','create_date']

class registerAdmin(admin.ModelAdmin):
    list_display = ['user','contact','registred_on_date']

class postaddAdmin(admin.ModelAdmin):
    list_display = ['user','category_name','title','description','city','on_date','on_time']

class contactusAdmin(admin.ModelAdmin):
    list_display = ['name','email','contact','msz','on_date','on_time']
admin.site.register(category,categoryAdmin)
admin.site.register(register,registerAdmin)
admin.site.register(postadd,postaddAdmin)
admin.site.register(contactus,contactusAdmin)


