from __future__ import annotations

from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Barometer, CustomPage, Faq, Lead, News, Review


class BarometerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class CustomPageAdmin(admin.ModelAdmin):
    list_display = ("id", "slug")


class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "question")


class LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "registration")


class NewsAdmin(SummernoteModelAdmin):
    list_display = ("id", "title")
    summernote_fields = ("pre_content", "content")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Barometer, BarometerAdmin)
admin.site.register(CustomPage, CustomPageAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Review, ReviewAdmin)

admin.site.site_header = "udonateacar Admin"
