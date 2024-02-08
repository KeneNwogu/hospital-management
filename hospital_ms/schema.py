import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from hospitals.models import Hospital
from hospitals.serializers import HospitalSerializer
from hospital_ms.auth import require_authentication
from django.contrib.auth import get_user_model


class HospitalType(DjangoObjectType):
    class Meta:
        model = Hospital
        fields = "__all__"


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = "__all__"


# class for queries, can eventually inherit from multiple schema types in different apps
class Query(graphene.ObjectType):
    hospitals = graphene.List(HospitalType)
    get_hospital = graphene.Field(HospitalType, id=graphene.UUID(required=True))

    def resolve_hospitals(self, info):
        return Hospital.objects.all()

    def resolve_get_hospital(self, info, id):
        try:
            return Hospital.objects.get(id=id)
        except Hospital.DoesNotExist:
            return None


class HospitalMutation(SerializerMutation):

    class Meta:
        serializer_class = HospitalSerializer

    hospital = graphene.Field(HospitalType)

    @classmethod
    @require_authentication
    def mutate(cls, root, info, input):
        if Hospital.objects.filter(name=input.get('name')).exists():
            raise ValueError('Hospital with this name already exists')

        hospital = Hospital.objects.create(**input)
        return HospitalMutation(hospital=hospital)


# would be in user application, but for simplicity, it's here
class LoginMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    token = graphene.String()

    @classmethod
    def mutate(cls, root, info, username, password):
        from django.contrib.auth import authenticate
        from graphql import GraphQLError
        from hospital_ms import settings
        import datetime
        import jwt

        authenticated_user = authenticate(username=username, password=password)
        if not authenticated_user:
            raise GraphQLError('Invalid login details provided')

        user_token_payload = {
            "user_id": str(authenticated_user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=720),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(user_token_payload, settings.SECRET_KEY, settings.JWT_ENCRYPTION_METHOD)
        return LoginMutation(user=authenticated_user, token=token)


class Mutation(graphene.ObjectType):
    create_hospital = HospitalMutation.Field()
    login = LoginMutation.Field()


# root schema
schema = graphene.Schema(query=Query, mutation=Mutation)
