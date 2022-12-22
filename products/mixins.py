from rest_framework import mixins


class GetMethodListOrDetail(mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    This mixins returns a list if a pk or id is not
    passed to the url, else it returns the detail of
    the id passed. this works on only get method.
    """

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)