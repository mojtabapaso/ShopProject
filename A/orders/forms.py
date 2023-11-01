from django import forms


class ApplyCouponForm(forms.Form):
    coupon = forms.CharField(label="کد تخفیف", required=False,
                             widget=forms.TextInput(attrs={'class': 'class-alert alert col-md-2'}))

