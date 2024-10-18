from django.urls import path, re_path, include
from django.contrib import admin
from django.http import (
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponse,
)
from django.views.decorators.cache import never_cache
from django.conf import settings
import django_sql_dashboard
import djp
from blog import views as blog_views
from blog import search as search_views
from blog import tag_views
from blog import feeds
from feedstats.utils import count_subscribers
import os
import importlib.metadata
import json
from proxy.views import proxy_view


handler404 = "blog.views.custom_404"


def wellknown_webfinger(request):
    remote_url = (
        "https://fedi.net/.well-known/webfinger?"
        + request.META["QUERY_STRING"]
    )
    return proxy_view(request, remote_url)


def wellknown_hostmeta(request):
    remote_url = (
        "https://fedi.net/.well-known/host-meta?"
        + request.META["QUERY_STRING"]
    )
    return proxy_view(request, remote_url)


def wellknown_nodeinfo(request):
    remote_url = "https://fedi.net/.well-known/nodeinfo"
    return proxy_view(request, remote_url)


def username_redirect(request):
    return HttpResponseRedirect("https://fedi.net/@simon")


def newsletter_redirect(request):
    return HttpResponseRedirect("https://.substack.com/")


def projects_redirect(request):
    return HttpResponseRedirect(
        "https://github.com/simonw/simonw/blob/main/releases.md"
    )


FAVICON = open(os.path.join(settings.BASE_DIR, "static/favicon.png"), "rb").read()


def static_redirect(request):
    return HttpResponsePermanentRedirect(
        "https://keithschacht.com%s" % request.get_full_path()
    )


def tag_redirect(request, tag):
    return HttpResponsePermanentRedirect("/tags/{}/".format(tag))


STAGING_ROBOTS_TXT = """
User-agent: Twitterbot
Disallow:

User-agent: *
Disallow: /
"""

PRODUCTION_ROBOTS_TXT = """
User-agent: ChatGPT-User
Disallow:

User-agent: *
Disallow: /admin/
Disallow: /search/

Sitemap: https://keithschacht.com/sitemap.xml
"""


def robots_txt(request):
    if settings.STAGING:
        txt = STAGING_ROBOTS_TXT
    else:
        txt = PRODUCTION_ROBOTS_TXT
    return HttpResponse(txt, content_type="text/plain")


def favicon_ico(request):
    return HttpResponse(FAVICON, content_type="image/x-icon")


@never_cache
def versions(request):
    installed_packages = [
        (dist.metadata["Name"], dist.version)
        for dist in sorted(
            importlib.metadata.distributions(), key=lambda d: d.metadata["Name"].lower()
        )
    ]
    return HttpResponse(
        json.dumps(installed_packages, indent=4), content_type="text/plain"
    )


urlpatterns = [
    re_path(r"^$", blog_views.index),
    re_path(r"^(\d{4})/$", blog_views.archive_year),
    re_path(r"^(\d{4})/(\w{3})/$", blog_views.archive_month),
    re_path(r"^(\d{4})/(\w{3})/(\d{1,2})/$", blog_views.archive_day),
    re_path(r"^(\d{4})/(\w{3})/(\d{1,2})/([\-\w]+)/$", blog_views.archive_item),
    re_path(r"^updates/(\d+)/$", blog_views.entry_updates),
    re_path(r"^updates/(\d+)\.json$", blog_views.entry_updates_json),
    # Redirects for entries, blogmarks, quotations by ID
    re_path(r"^e/(\d+)/?$", blog_views.redirect_entry),
    re_path(r"^b/(\d+)/?$", blog_views.redirect_blogmark),
    re_path(r"^q/(\d+)/?$", blog_views.redirect_quotation),
    # Ancient URL pattern still getting hits
    re_path(r"^/?archive/(\d{4})/(\d{2})/(\d{2})/$", blog_views.archive_day_redirect),
    re_path(
        r"^/?archive/(\d{4})/(\d{2})/(\d{2})/([\-\w]+)/?$",
        blog_views.archive_item_redirect,
    ),
    # Fediverse
    path(".well-known/webfinger", wellknown_webfinger),
    path(".well-known/host-meta", wellknown_hostmeta),
    path(".well-known/nodeinfo", wellknown_nodeinfo),
    path("@keithschacht", username_redirect),
    re_path(r"^newsletter/?$", newsletter_redirect),
    re_path(r"^projects/?$", projects_redirect),
    re_path(r"^versions/$", versions),
    re_path(r"^robots\.txt$", robots_txt),
    re_path(r"^favicon\.ico$", favicon_ico),
    re_path(r"^search/$", search_views.search),
    re_path(r"^about/$", blog_views.about),
    re_path(r"^tags/$", blog_views.tag_index),
    re_path(r"^tags/(.*?)/$", blog_views.archive_tag),
    re_path(r"^tags/(.*?).atom$", blog_views.archive_tag_atom),
    re_path(r"^tag/([a-zA-Z0-9_-]+)/$", tag_redirect),
    re_path(r"^series/$", blog_views.series_index),
    re_path(r"^series/(.*?)/$", blog_views.archive_series),
    re_path(r"^series/(.*?).atom$", blog_views.archive_series_atom),
    re_path(r"^atom/entries/$", count_subscribers(feeds.Entries().__call__)),
    re_path(r"^atom/links/$", count_subscribers(feeds.Blogmarks().__call__)),
    re_path(r"^atom/everything/$", count_subscribers(feeds.Everything().__call__)),
    re_path(r"^sitemap\.xml$", feeds.sitemap),
    path("tools/", blog_views.tools),
    path("tools/extract-title/", blog_views.tools_extract_title),
    re_path(r"^tools/search-tags/$", search_views.tools_search_tags),
    re_path(r"^write/$", blog_views.write),
    #  (r'^about/$', blog_views.about),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^static/", static_redirect),
    path("dashboard/", include(django_sql_dashboard.urls)),
    path("user-from-cookies/", blog_views.user_from_cookies),
    path("tags-autocomplete/", tag_views.tags_autocomplete),
    re_path(
        r'^article/using-hotwire-it-was-simple-to-build-inline-title-editing-10$',
        lambda r: HttpResponsePermanentRedirect('/2024/May/17/using-hotwire-it-was-simple-to-build-inline-title-editing/')
    ),
    re_path(
        r'^article/im-loving-rails-stimulus-check-out-this-example-9$',
        lambda r: HttpResponsePermanentRedirect('/2024/Oct/16/im-loving-rails-stimulus-check-out-this-example/')
    ),
] + djp.urlpatterns()
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            re_path(r"^__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns
    except ImportError:
        pass
