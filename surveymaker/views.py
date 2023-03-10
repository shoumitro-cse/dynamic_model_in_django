from .models import Survey
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context import RequestContext


def all_survey_responses(request):
    template_name = "surveymaker/all.html"
    surveys = [(survey, survey.Response.objects.all()) for survey in Survey.objects.all()]
    return render(request, template_name, {'surveys': surveys})


def get_response_form(response):
    class FormMeta:
        model = response
    return type('ResponseForm', (forms.ModelForm,), {'Meta': FormMeta})


def survey_form(request, survey_slug):
    template_name = "surveymaker/survey_form.html"
    survey = get_object_or_404(Survey, slug=survey_slug)
    Response = survey.Response
    ResponseForm = get_response_form(Response)

    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('surveymaker_index')
    else:
        form = ResponseForm()
    return render(template_name, {'form': form, 'survey': survey},
                  context_instance=RequestContext(request))

