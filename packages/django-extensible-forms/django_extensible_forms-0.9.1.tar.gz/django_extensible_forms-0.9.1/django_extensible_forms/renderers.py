from django.forms.renderers import TemplatesSetting as DjangoTemplatesSetting


class TemplatesSetting(DjangoTemplatesSetting):
	form_template_name = "django_extensible_forms/forms/div.html"
	formset_template_name = "django/forms/formsets/div.html"
