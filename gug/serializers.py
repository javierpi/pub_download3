from rest_framework import serializers, viewsets
from gug.models import Google_service, Period, Publication, Stats, Dspace, Service_type


class StatsSerializer3(serializers.ModelSerializer):
    non_model_field = serializers.CharField()

    class Meta:
        model = Stats
        fields = '__all__'
        # fields = ('non_model_field', 'cuantity')


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ('google_service', 'period', 'id_dspace', 'publication', 'cuantity')

# Serializers define the API representation.


class StatsSerializer2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stats
        fields = ('cuantity',)
        #fields = ('publication', 'cuantity')
        # extra_kwargs = {
        #     'publication': {'lookup_field': 'pk'}
        # }
        # 'publication': {'view_name': 'publication_detail', 'lookup_field': 'pk'}
        # fields = ('id_dspace__id_dspace', 'cuantity')


class DspaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dspace
        fields = ('id_dspace', 'title', 'post_title1', 'post_title2')


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication
        fields = ('id_dspace', 'tfile',)


class Service_typeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service_type
        fields = ('service',)


class Google_serviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Google_service
        fields = ('name', 'scope', 'discovery', 'secret_json', 'client_secret_path', 'service', 'version', 'view_id', 'active', 'report')


class PeriodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Period
        fields = ('start_date', 'end_date', 'active')


# ------- View Sets
class PeriodosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Period
        fields = ('start_date', 'end_date', 'active')


class PeriodosViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodosSerializer


class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer


class DspaceViewSet(viewsets.ModelViewSet):
    queryset = Dspace.objects.all()
    serializer_class = DspaceSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class Service_typeViewSet(viewsets.ModelViewSet):
    queryset = Service_type.objects.all()
    serializer_class = Service_typeSerializer


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


class Google_serviceViewSet(viewsets.ModelViewSet):
    queryset = Google_service.objects.all()
    serializer_class = Google_serviceSerializer
