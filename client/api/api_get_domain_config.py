from .imports import *


def api_get_domain_config(request, domain):
    context = {}
    if usetting.objects.filter(domain__exact=domain).exists():
        config = usetting.objects.get(domain=domain)
        context['domain'] = config.domain
        context['org_color'] = config.org_color
        context['sub_color'] = config.sub_color
        context['contact_phone'] = config.contact_phone
        context['instagram'] = config.instagram
        context['twitter'] = config.twitter
        context['aparat'] = config.aparat
        context['facebook'] = config.facebook
        context['youtube'] = config.youtube
        context['slogan'] = config.slogan
        context['short_title'] = config.short_title
        context['android_version'] = ''
        context['ios_version'] = ''
        context['pwa_version'] = ''
        if config.image_tag:
            if config.image_tag.android_version and config.image_tag.android_version and config.image_tag.pwa_version:
                context['android'] = config.image_tag.android_version
                context['android'] = config.image_tag.ios_version
        if config.splashscreen:
            context['splashscreen'] = request.build_absolute_uri() + config.splashscreen.url.split('/')[-1]
        if config.company_logo:
            context['company_logo'] = request.build_absolute_uri() + config.company_logo.url.split('/')[-1]
        if config.favicon:
            context['favicon'] = request.build_absolute_uri() + config.favicon.url.split('/')[-1]
        return JsonResponse(context, status=200)
    return JsonResponse({}, status=200)
