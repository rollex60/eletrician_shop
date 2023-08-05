from django import forms
from django.contrib.auth import get_user_model
from django.forms import Textarea

from shop.models import Comments, Order, Shop, Provider, Notification

User = get_user_model()


class CommentForm(forms.ModelForm):
    # ----Comment Form----------------------------------------------------------------------------------------
    
    class Meta:
        model = Comments
        fields = ('text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows':5})



class OrderForm(forms.ModelForm):
    # ----Order Form----------------------------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Date of receipt of the order'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class LoginForm(forms.ModelForm):
    # ----Login Form----------------------------------------------------------------------------------------

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'User with login {username} not found in the system')
        if not user.check_password(password):
            raise forms.ValidationError('Invalid password')
        return self.cleaned_data
        
        
class RegistrationUserForm(forms.ModelForm):
    # ----Registration User--------------------------------------------------------------------------------------------------

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm password'
        self.fields['phone'].label = 'Phone'
        self.fields['address'].label = 'Address'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net', 'xyz']:
            raise forms.ValidationError(f'Registration for a domain {domain} impossible')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This mailing address is already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Name {username} busy. Try something else.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']


class RegistrationForm(forms.ModelForm):
    # ----Registration Form----------------------------------------------------------------------------------------

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    nif = forms.CharField()
    address = forms.CharField(required=False)
    firm = forms.CharField(required=False)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['nif'].label = 'NIF'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm the password'
        self.fields['phone'].label = 'Phone number'
        self.fields['address'].label = 'Address'
        self.fields['email'].label = 'Email'
        self.fields['firm'].label = 'Firm'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net', 'xyz']:
            raise forms.ValidationError(f'Registration for a domain {domain} impossible')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This mailing address is already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Name {username} занято. Try something else.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'firm', 'nif', 'address', 'phone', 'email']
        
        
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'text']
        
        
class ProductForm(forms.ModelForm):
    # ProductForm--------------------------------------------------------------------------------------------------
    
    class Meta:
        model = Provider
        fields = ['firm', 'nif', 'phone', 'address', 'name', 'shop', 'stock', 'price', 'discount', 'iva']


class ProductEditForm(forms.ModelForm):
    # ProductEditForm----------------------------------------------------------------------------------------------

    class Meta:
        model = Provider
        fields = ['firm', 'nif', 'phone', 'address', 'name', 'shop', 'stock', 'price', 'discount', 'iva']
        
        
        
        