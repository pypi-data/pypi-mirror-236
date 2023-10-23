from unittest import TestCase

import fields
from django.forms.fields import Field

from .forms import Form

TestFormClass = type(
	"TestForm",
	(Form,),
	{
		name: getattr(fields, name)()
		for name in fields.__all__
		if isinstance(getattr(fields, name), Field)
	},
)


class FormTests(TestCase):
	def test_form_rendition(self):
		form = TestFormClass()
		self.assertIsInstance(str(form), str)
