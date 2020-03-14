from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML


class SubmitCancelFormHelper(FormHelper):
    """Custom FormHelper that appends to the layout cancel and submit
    buttons (works only with bootstrap crispy-forms pack). It expects a
    `cancel_href` attribute to be used as cancel button URL.

    Example::

        SubmitCancelFormHelper(self, cancel_href="/some/url/")
    """

    def __init__(self, *args, **kwargs):
        cancel_href = kwargs.pop('cancel_href', '#')
        super(SubmitCancelFormHelper, self).__init__(*args, **kwargs)
        self.layout.append(
            Layout(
                FormActions(
                    HTML("""<a role="button" class="btn btn-default mr4"
                            href="{0}">Cancel</a>""".format(cancel_href)),
                    Submit('save', 'Submit'),
                )
            )
        )


from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm


class ModelFormWithHelper(ModelForm):
    """Custom ModelForm that allows to attach a crispy-forms FormHelper class,
    that will modify in some way the rendering of the layout.

    Example::

        FooForm(ModelFormWithHelper):
            class Meta:
                model = FooModel
                helper_class = FooFormHelper
    """

    def __init__(self, *args, **kwargs):
        super(ModelFormWithHelper, self).__init__(*args, **kwargs)

        if hasattr(self.Meta, "helper_class"):
            helper_class = getattr(self.Meta, "helper_class")
            kwargs = self.get_helper_kwargs()
            self.helper = helper_class(self, **kwargs)
        else:
            raise ImproperlyConfigured(
                "{0} is missing a 'helper_class' meta attribute.".format(
                    self.__class__.__name__))

    def get_helper_kwargs(self):
        """Get all helper attributes from class Meta by stripping them of
        `helper_` part of attribute string

        :return: dict with helper kwargs
        """
        kwargs = {}
        for attr, value in self.Meta.__dict__.items():
            if attr.startswith("helper_") and attr != "helper_class":
                new_attr = attr.split("_", 1)[1]
                kwargs[new_attr] = value
        return kwargs
