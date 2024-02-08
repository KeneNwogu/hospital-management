import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from hospitals.models import Hospital
from hospitals.serializers import HospitalSerializer


class HospitalType(DjangoObjectType):
    class Meta:
        model = Hospital
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


# class HospitalMutation(SerializerMutation):
#     class Meta:
#         serializer_class = HospitalSerializer
#
#     hospital = graphene.Field(HospitalType)
#
#     @classmethod
#     def mutate(cls, root, info, input):
#         hospital = Hospital.objects.create(**input)
#         return HospitalMutation(hospital=hospital)
#
#
# class Mutation(graphene.ObjectType):
#     create_hospital = HospitalMutation.Field()


# root schema
schema = graphene.Schema(query=Query)
