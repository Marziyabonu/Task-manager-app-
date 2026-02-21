from django import forms
from django.contrib.auth.models import User

class SimplestUserCreationForm(forms.ModelForm):
    """
    Parolni bir marta kiritishni talab qiladigan eng sodda forma.
    Parol sifati bo'yicha cheklovlar o'chirilgan.
    """
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Parol')
    
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def save(self, commit=True):
        """
        Foydalanuvchini yaratadi va parolni xavfsiz saqlaydi.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user