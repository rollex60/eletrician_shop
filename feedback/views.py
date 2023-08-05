from django.shortcuts import redirect

from coolsite import settings
from .forms import FeedbackForm
from django.views.generic import View
from django.contrib import messages


class FeedbackView(View):
    # ----Feedback----------------------------------------------------------------------------
    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, settings.MY_INFO, 'We will call you right now')
        else:
            messages.add_message(request, settings.MY_INFO,'Fill in required fields')
        return redirect('/')
