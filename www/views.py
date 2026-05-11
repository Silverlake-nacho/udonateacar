from __future__ import annotations

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.decorators.csrf import ensure_csrf_cookie

from toolkit import generate_pagination_context
from www.forms import ContactForm
from www.models import Barometer, CustomPage, Faq, Lead, News, Review


@ensure_csrf_cookie
def index(request: HttpRequest) -> HttpResponse:
    try:
        total_raised = Barometer.objects.get(name="Charity").value
    except Barometer.DoesNotExist:
        total_raised = 0

    context = {
        "reviews": Review.get_active(),
        "js_context": {
            "total_raised": total_raised,
        },
    }

    return render(request, "www/index.html", context=context)


def charities(request: HttpRequest) -> HttpResponse:
    context = {
        "reviews": Review.get_active(),
    }

    return render(request, "www/charities.html", context=context)


def faqs(request: HttpRequest) -> HttpResponse:
    raw_faqs = Faq.get_active()
    faqs_formatted = []

    for _index, faq in enumerate(raw_faqs):
        faqs_formatted.append(
            {
                "faq": faq,
                "modulo": _index % 2,
            }
        )

    context = {
        "faqs": faqs_formatted,
        "reviews": Review.get_active(),
    }

    return render(request, "www/faqs.html", context=context)


def news(request: HttpRequest) -> HttpResponse:
    featured = News.get_featured()
    stories = News.get_active()

    if featured:
        stories = stories.exclude(id=featured.id)

    context = generate_pagination_context(stories, request)
    context["featured"] = featured

    return render(request, "www/news.html", context=context)


def news_single(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(News, pk=pk)
    related = (
        News.objects.filter(category=post.category).exclude(pk=pk).order_by("-id")[:3]
    )

    context = {
        "post": post,
        "related": related,
    }

    return render(request, "www/news_single.html", context=context)


def testimonials(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "www/testimonials.html",
        context=generate_pagination_context(Review.get_active_video(), request),
    )


def vre_awards(request: HttpRequest) -> HttpResponse:
    return custom_awards_page(request, "vreawards")


def contact(request: HttpRequest) -> HttpResponse:
    message_sent = False

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            content = f"""
                Name: {form.cleaned_data['name']}
                Email: {form.cleaned_data['from_email']}
                Subject: {form.cleaned_data['subject']}
                Phone: {form.cleaned_data['phone']}
                Message: {form.cleaned_data['message']}
            """

            msg = EmailMultiAlternatives(
                f"UDAC contact form: {form.cleaned_data['from_email']}",
                content,
                "server@udonateacar.com",
                [settings.SUPPORT_EMAIL],
                reply_to=[form.cleaned_data["from_email"]],
            )

            msg.send()
            message_sent = True
        else:
            for error in form.errors.values():
                messages.error(request, ", ".join(error))
    else:
        form = ContactForm()

    context = {
        "form": form,
        "reviews": Review.get_active(),
        "message_sent": message_sent,
    }

    return render(request, "www/contact.html", context=context)


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "www/privacy.html")


def capture(request: HttpRequest, step: str) -> HttpResponse:
    template_path = f"www/capture/{step}.html"

    try:
        template = get_template(template_path)
    except TemplateDoesNotExist:
        return HttpResponseNotFound()

    try:
        lead = Lead.objects.get(id=request.session["lead_id"])
    except (KeyError, Lead.DoesNotExist):
        return redirect("www:index")

    context = {
        "lead": lead,
    }

    return HttpResponse(template.render(context, request))


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "faqs": Faq.get_active(),
        "reviews": Review.get_active(),
    }

    return render(request, "www/about.html", context=context)


def how_it_works(request: HttpRequest) -> HttpResponse:
    context = {
        "faqs": Faq.get_active(),
        "reviews": Review.get_active(),
    }

    return render(request, "www/how-it-works.html", context=context)


def custom_awards_page(request: HttpRequest, slug: str) -> HttpResponse:
    page = CustomPage.objects.filter(active=True, slug=slug).last()

    if not page:
        return HttpResponseNotFound()

    return render(
        request,
        "www/custom-awards-page.html",
        context={
            "page": page,
        },
    )
