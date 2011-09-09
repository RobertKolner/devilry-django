from django.http import HttpResponseBadRequest, HttpResponse

from ..simplified import PermissionDenied, SimplifiedException, InvalidUsername
from restview import RestfulView, extjswrap
from serializers import (serializers, SerializableResult,
                         ErrorMsgSerializableResult,
                         ForbiddenSerializableResult,
                         InvalidUsernameSerializableResult)
from readform import ReadForm



class HttpResponseCreated(HttpResponse):
    status_code = 201


class FormErrorSerializableResult(SerializableResult):
    def __init__(self, form, use_extjshacks):
        fielderrors = dict(form.errors)
        non_field_errors = list(form.non_field_errors())
        result = dict(fielderrors=fielderrors, errormessages=non_field_errors)
        result = extjswrap(result, use_extjshacks, success=False)
        super(FormErrorSerializableResult, self).__init__(result, httpresponsecls=HttpResponseBadRequest)


class ModelRestfulView(RestfulView):
    """
    :class:`ModelRestfulView` is used in conjunction with the
    :class:`restful_modelapi`-decorator to autogenerate a RESTful
    interface for a simplified class (see :ref:`simplified`).
    """
    @classmethod
    def filter_urlmap(cls, itemdct):
        if not hasattr(cls._meta, 'urlmap'):
            return itemdct
        for fieldname, mapping in cls._meta.urlmap.iteritems():
            url = mapping.restfulcls.get_rest_url(itemdct[mapping.idfield])
            itemdct[fieldname] = url
        return itemdct

    @classmethod
    def filter_resultitem(cls, itemdct):
        return cls.filter_urlmap(itemdct)

    def restultqry_to_list(self, qryresultwrapper):
        return [self.__class__.filter_resultitem(itemdct) \
                for itemdct in qryresultwrapper]

    def _create_or_replace(self, instance=None):
        data = serializers.deserialize(self.comformat, self.request.raw_post_data)
        form = self.__class__.EditForm(data, instance=instance)
        if form.is_valid():
            try:
                if instance == None:
                    id = self._meta.simplified.create(self.request.user, **form.cleaned_data)
                else:
                    id = self._meta.simplified.update(self.request.user, instance.pk, **form.cleaned_data)
            except PermissionDenied, e:
                return ForbiddenSerializableResult(e)
            except InvalidUsername, e:
                return InvalidUsernameSerializableResult(e.username)

            data['id'] = id
            result = self.extjswrapshortcut(data)
            if instance == None:
                return SerializableResult(result, httpresponsecls=HttpResponseCreated)
            else:
                return SerializableResult(result)
        else:
            return FormErrorSerializableResult(form, self.use_extjshacks)


    def _load_getdata(self):
        if 'getdata_in_qrystring' in self.request.GET: # NOTE: For easier ExtJS integration
            return True, self.request.GET
        else:
            try:
                return False, serializers.deserialize(self.comformat, self.request.raw_post_data)
            except ValueError, e:
                raise ValueError(('Bad request data: {0}. Perhaps you ment to'
                                  'send GET data as a querystring? In that case, add '
                                  'getdata_in_qrystring=1 to your querystring.'.format(e)))

    def _parse_extjs_sort(self, sortlist):
        orderby = []
        for sortitem in sortlist:
            fieldname = sortitem['property']
            if sortitem.get('direction', 'ASC') == 'DESC':
                fieldname = '-' + fieldname
            orderby.append(fieldname)
        return orderby

    def crud_search(self, request):
        """ Maps to the ``search`` method of the simplified class. """
        try:
            fromGET, getdata = self._load_getdata()
        except ValueError, e:
            return ErrorMsgSerializableResult(str(e),
                                              httpresponsecls=HttpResponseBadRequest)
        form = self.__class__.SearchForm(getdata)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if 'sort' in cleaned_data:
                sort = cleaned_data['sort']
                del cleaned_data['sort']
                if not cleaned_data.get('orderby'):
                    if sort and self.use_extjshacks:
                        orderby = self._parse_extjs_sort(sort)
                        cleaned_data['orderby'] = orderby

            try:
                qryresultwrapper = self._meta.simplified.search(self.request.user, **cleaned_data)
            except SimplifiedException, e:
                return ErrorMsgSerializableResult(str(e),
                                                  httpresponsecls=HttpResponseBadRequest)

            resultlist = self.restultqry_to_list(qryresultwrapper)
            result = self.extjswrapshortcut(resultlist, total=qryresultwrapper.total)
            return SerializableResult(result)
        else:
            return FormErrorSerializableResult(form, self.use_extjshacks)



    def crud_read(self, request, id):
        """ Maps to the ``read`` method of the simplified class. """
        try:
            fromGET, getdata = self._load_getdata()
        except ValueError, e:
            return ErrorMsgSerializableResult(str(e),
                                              httpresponsecls=HttpResponseBadRequest)
        form = ReadForm(getdata)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                data = self._meta.simplified.read(self.request.user, id, **cleaned_data)
            except PermissionDenied, e:
                return ForbiddenSerializableResult(e)
            data = self.extjswrapshortcut(data)
            return SerializableResult(data)
        else:
            return FormErrorSerializableResult(form, self.use_extjshacks)


    def crud_create(self, request):
        """ Maps to the ``create`` method of the simplified class. """
        return self._create_or_replace()

    def crud_update(self, request, id):
        """ Maps to the ``update`` method of the simplified class. """
        try:
            instance = self._meta.simplified._meta.model.objects.get(pk=id)
        except self._meta.simplified._meta.model.DoesNotExist, e:
            return ForbiddenSerializableResult(e)
        return self._create_or_replace(instance)

    def crud_delete(self, request, id):
        """ Maps to the ``delete`` method of the simplified class. """
        try:
            self._meta.simplified.delete(request.user, id)
        except PermissionDenied, e:
            return ForbiddenSerializableResult(e)
        else:
            data = self.extjswrapshortcut(dict(id=id))
            return SerializableResult(data)
