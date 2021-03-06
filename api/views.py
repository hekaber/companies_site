from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions

from companies.models import Company
from .serializers import CompanySerializer, UserSerializer


class CompaniesList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Returns the companies list
        :param request:
        :param format:
        :return:
        """
        companies = Company.objects.filter(owner__exact=request.user).order_by('-creation_date')
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Creates a new company
        :param request:
        :param format:
        :return:
        """
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Get a company details
        :param request:
        :param pk:
        :param format:
        :return:
        """
        company = self.get_object(pk)
        if company.owner != request.user:
            return Response({'error': 'Only owner is allowed to read'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Updates a company
        :param request:
        :param pk:
        :param format:
        :return:
        """
        company = self.get_object(pk)
        if company.owner != request.user:
            return Response({'error': 'Only owner is allowed to edit'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes a company
        :param request:
        :param pk:
        :param format:
        :return:
        """
        company = self.get_object(pk)
        if company.owner != request.user:
            return Response({'error': 'Only owner is allowed to delete'},
                            status=status.HTTP_403_FORBIDDEN)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    """
    Gets a users list
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Gets details for a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
