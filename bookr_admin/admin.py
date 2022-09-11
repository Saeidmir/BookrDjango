from django.contrib import admin
# Register your models here.
from django.template.response import TemplateResponse
from django.urls import path


class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Adminstration"
    site_title = "Bookr Created by Saeid"
    index_title = "Bookr Admin Panel"
    logout_template = 'admin/logout.html'
    # overriding the each_context to add username to it
    # def each_context(self, request):
    #     context = super().each_context(request)
    #     context['username'] = request.user.username
    #     return context


    def profile_view(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

    def get_urls(self):
        urls = super().get_urls() # Get the set of existing urls
        # Define our custome url pattern for custome views
        url_patterns = [path("admin-profile", self.admin_view(self.profile_view))]
        url_patterns += urls
        return url_patterns


# admin_site = BookrAdmin(name="bookr_admin")



