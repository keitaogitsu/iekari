from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from iekari.models import GENDER_LIST, Profile

class RegisterForm(UserCreationForm):
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=GENDER_LIST, required=True)
    household_num = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','age','gender','household_num']
        labels = {
            'username': 'ユーザー名',
            'password1': 'パスワード',
            'password2': 'パスワード確認',
            'age': '年齢',
            'gender': '性別',
            'household_num': '世帯人数',
        }

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError('Cannot create User and Profile without database save')
        
        user = super().save()

        try:
            max_id = Profile.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'B00000'

        prof_id = 'B'+(str(int(max_id[1:])+1).zfill(5))

        age = self.cleaned_data['age']
        gender = self.cleaned_data['gender']
        household_num = self.cleaned_data['household_num']

        profile = Profile(id=prof_id,age=age,gender=gender,household_num=household_num,user_id=user.id)
        profile.save()

        return user