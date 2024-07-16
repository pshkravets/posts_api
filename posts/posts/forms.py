from django import forms


class ReplyCommentsSettings(forms.Form):
    reply_enabled = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'type': 'checkbox',
            'role': 'switch',
            'id': 'flexSwitchCheckDefault'
        })
    )

    reply_hours = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'role': 'switch',
            'type': 'text',
            'id': 'validationTooltip01'
        }
        )
    )

    reply_minutes = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'role': 'switch',
            'type': 'text',
            'id': 'validationTooltip02'
        }
        )
    )

    reply_seconds = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'role': 'switch',
            'type': 'text',
            'id': 'validationTooltip03'
        }
        )
    )