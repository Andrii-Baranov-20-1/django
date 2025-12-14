from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Category, Types, EducationalInstitution, EducationalInstitutionPhoto, Rating, RatingStar, Reviews, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)

class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(EducationalInstitution)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "url", "draft", "get_mainPhoto")
    #readonly_fields = ("get_mainPhoto",)
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    inlines = [ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]

    def get_mainPhoto(self, obj):
        return mark_safe(f'<img src={obj.mainPhoto.url} width="110", height="70"')

    get_mainPhoto.short_description = "Photo"

    def unpublish(self, request, queryset):
        """Remove publication"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 publish updated"
        else:
            message_bit = f"{row_update} publishes updated"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Make publication"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 publish updated"
        else:
            message_bit = f"{row_update} publishes updated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Make publication"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Remove publication"
    unpublish.allowed_permissions = ('change',)

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "institution", "id")
    readonly_fields = ("name", "email")

# admin.site.register(Category, CategoryAdmin)
admin.site.register(Types)
# admin.site.register(Restaurants)
admin.site.register(EducationalInstitutionPhoto)
admin.site.register(Rating)
admin.site.register(RatingStar)
#admin.site.register(Reviews)

admin.site.site_title = "Django Restaurants"
admin.site.site_header = "Django Restaurants"