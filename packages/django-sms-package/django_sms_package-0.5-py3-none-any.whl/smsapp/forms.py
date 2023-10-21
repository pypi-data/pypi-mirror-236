from django import forms
from bootstrap_daterangepicker import widgets, fields
class FilterForm(forms.Form):
    date_range = fields.DateRangeField(
        input_formats=['MMMM D, YYYY', ""],
        widget=widgets.DateRangeWidget(
            format = 'MMMM D, YYYY',
            
        ),
        required=False
    )

