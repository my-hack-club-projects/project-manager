from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):

   def render(self, data, accepted_media_type=None, renderer_context=None):
       data = {
           "success": True,
           "data": data
       }
       return super(CustomJSONRenderer, self).render(data, accepted_media_type, renderer_context)