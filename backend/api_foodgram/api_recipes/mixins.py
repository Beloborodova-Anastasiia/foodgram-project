from rest_framework import mixins, viewsets


class RetriveListCreateDeleteUpdateViewSet(mixins.RetrieveModelMixin,
                                           mixins.ListModelMixin,
                                           mixins.CreateModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.DestroyModelMixin,
                                           viewsets.GenericViewSet):
    pass
