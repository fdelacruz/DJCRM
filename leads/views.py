from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganizerAndLoginRequiredMixin
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"  # default configuration: object_list


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@they.com",
            recipient_list=["test@me.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')
