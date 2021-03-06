# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from cms.extensions import PageExtensionAdmin
from cmsplugin_cascade.fields import PartialFormField
from cmsplugin_cascade.widgets import JSONMultiWidget
from cmsplugin_cascade.utils import rectify_partial_form_field
from .models import RevealExtension


@admin.register(RevealExtension)
class RevealExtensionAdmin(PageExtensionAdmin):
    TRANSITIONS = (('none', "None"), ('fade', "Fade"), ('slide', "Slide"), ('convex', "Convey"),
        ('concave', "Concave"), ('zoom', "Zoom"))

    option_fields = ((
        PartialFormField('controls',
            widgets.CheckboxInput(),
            label=_("Controls"),
            initial=True,
            help_text=_("Displays control arrows in the bottom right corner."),
        ),
        PartialFormField('progress',
            widgets.CheckboxInput(),
            label=_("Progress"),
            initial=True,
            help_text=_("Display a presentation progress bar on the bottom."),
        ),
        PartialFormField('history',
            widgets.CheckboxInput(),
            label=_("History"),
            initial=True,
            help_text=_("Push each slide change to the browser history."),
        ),
        PartialFormField('center',
            widgets.CheckboxInput(),
            label=_("Center"),
            initial=True,
            help_text=_("Vertical centering of slides."),
        ),
        PartialFormField('transition',
            widgets.Select(choices=TRANSITIONS),
            label=_("Transition"),
            help_text=_("Transitions style for changing slides."),
        ),
        PartialFormField('width',
            widgets.TextInput(),
            label=_("Width"),
            initial='960px',
            help_text=_("Slide width"),
        ),
        PartialFormField('height',
            widgets.TextInput(),
            label=_("Height"),
            initial='700px',
            help_text=_("Slide height"),
        ),
        PartialFormField('margin',
            widgets.NumberInput(attrs={'step': 0.02}),
            label=_("Margin"),
            initial=0.1,
            help_text=_("Slide's margin"),
        ),
        PartialFormField('minScale',
            widgets.NumberInput(attrs={'step': 0.1}),
            label=_("Min Scale"),
            initial=0.2,
        ),
        PartialFormField('maxScale',
            widgets.NumberInput(attrs={'step': 0.1}),
            label=_("Max Scale"),
            initial=1.5,
        ),
    ),)

    class Media:
        css = {'all': ('cascade/css/admin/partialfields.css',)}

    def get_form(self, request, obj=None, **kwargs):
        """
        Build the form used for changing the model.
        """
        kwargs.update(widgets={
            'options': JSONMultiWidget(self.option_fields),
        })
        form = super(RevealExtensionAdmin, self).get_form(request, obj, **kwargs)
        rectify_partial_form_field(form.base_fields['options'], self.option_fields)
        form.option_fields = self.option_fields
        return form
