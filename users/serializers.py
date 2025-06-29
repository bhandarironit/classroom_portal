from rest_framework import serializers
from .models import CustomUser, StudentProfile, TeacherProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=[("student", "Student"), ("teacher", "Teacher")])


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        role = validated_data.pop("role")
        user = CustomUser.objects.create_user(**validated_data)
        user.role = role
        user.save()

        if role == "student":
            StudentProfile.objects.create(user=user)
        elif role == "teacher":
            TeacherProfile.objects.create(user=user)

        return user
    
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["name", "age", "grade", "enrollment_number", "roll_number"]


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ["name", "age", "department", "employee_id"]

# -----------------------------
# Login Serializer (Custom JWT Login with Email)
# -----------------------------
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
