# from django import forms
# from django.contrib import admin
# from .models import Header, Navigation, IntroSection, AboutUs

# # Define admin forms for your models
# class HeaderAdminForm(forms.ModelForm):
#     class Meta:
#         model = Header
#         fields = ['title','logo']

# class NavigationAdminForm(forms.ModelForm):
#     class Meta:
#         model = Navigation
#         fields = ['title', 'link']

# class IntroSectionAdminForm(forms.ModelForm):
#     class Meta:
#         model = IntroSection
#         fields = ['intro_text', 'background_image']

# class AboutUsAdminForm(forms.ModelForm):
#     class Meta:
#         model = AboutUs
#         fields = ['title', 'text', 'image']

# # Register your models with the admin panel
# @admin.register(Header)
# class HeaderAdmin(admin.ModelAdmin):
#     form = HeaderAdminForm

# @admin.register(Navigation)
# class NavigationAdmin(admin.ModelAdmin):
#     form = NavigationAdminForm

# @admin.register(IntroSection)
# class IntroSectionAdmin(admin.ModelAdmin):
#     form = IntroSectionAdminForm

# @admin.register(AboutUs)
# class AboutUsAdmin(admin.ModelAdmin):
#     form = AboutUsAdminForm
