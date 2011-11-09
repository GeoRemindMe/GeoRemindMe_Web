# coding=utf-8

# from watchers import create_user_profile

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _

from guardian.decorators import permission_required_or_403
from userena.decorators import secure_required
from userena.utils import signin_redirect, get_profile_model
from userena.forms import EditProfileForm
import userena.views as userena_views
from userena import settings as userena_settings


old_profile_edit = userena_views.profile_edit
@secure_required
@permission_required_or_403('change_profile', (get_profile_model(), 'user__username', 'username'))
def monkey_profile_edit(request, username, edit_profile_form=EditProfileForm,
                 template_name='userena/profile_form.html', success_url=None,
                 extra_context=None):
    """
    Edit profile.

    Edits a profile selected by the supplied username. First checks
    permissions if the user is allowed to edit this profile, if denied will
    show a 404. When the profile is succesfully edited will redirect to
    ``success_url``.

    :param username:
        Username of the user which profile should be edited.

    :param edit_profile_form:

        Form that is used to edit the profile. The :func:`EditProfileForm.save`
        method of this form will be called when the form
        :func:`EditProfileForm.is_valid`.  Defaults to :class:`EditProfileForm`
        from userena.

    :param template_name:
        String of the template that is used to render this view. Defaults to
        ``userena/edit_profile_form.html``.

    :param success_url:
        Named URL which be passed on to a django ``reverse`` function after the
        form is successfully saved. Defaults to the ``userena_detail`` url.

    :param extra_context:
        Dictionary containing variables that are passed on to the
        ``template_name`` template.  ``form`` key will always be the form used
        to edit the profile, and the ``profile`` key is always the edited
        profile.

    **Context**

    ``form``
        Form that is used to alter the profile.

    ``profile``
        Instance of the ``Profile`` that is edited.

    """
    user = get_object_or_404(User,
                             username__iexact=username)

    profile = user.get_profile()

    user_initial = {
                    'username': user.username,
                    }

    form = edit_profile_form(instance=profile, initial=user_initial)

    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                 initial=user_initial)

        if form.is_valid():
            profile = form.save()

            if userena_settings.USERENA_USE_MESSAGES:
                messages.success(request, _('Your profile has been updated.'),
                                 fail_silently=True)

            if success_url: redirect_to = success_url
            else: redirect_to = reverse('userena_profile_detail', kwargs={'username': user.username})
            return redirect(redirect_to)

    if not extra_context: extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = profile
    return direct_to_template(request,
                              template_name,
                              extra_context=extra_context)
userena_views.profile_edit = monkey_profile_edit