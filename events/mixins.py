from django import forms


class TailwindFormMixin:
    """Mixin to apply Tailwind CSS styles to form fields dynamically."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

    def apply_styled_widgets(self):
        """Apply Tailwind styles dynamically based on field types."""
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):  # CharField
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.Textarea):  # TextField
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'rows': 4,
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.DateInput):  # DateField
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'type': 'date',
                })
            elif isinstance(field.widget, forms.TimeInput):  # TimeField
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'type': 'time',
                })
            elif isinstance(field.widget, forms.Select):  # ForeignKey (dropdown)
                field.widget.attrs.update({
                    'class': self.default_classes,
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):  # ManyToManyField
                field.widget.attrs.update({
                    'class': "border border-gray-300 rounded p-2 w-full",
                })
            elif isinstance(field.widget, forms.EmailInput):  # EmailField
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                })
