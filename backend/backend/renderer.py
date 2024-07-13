from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):

   def render(self, data, accepted_media_type=None, renderer_context=None):
       data = {
           "success": isinstance(data, dict) and data.get("success", True) or isinstance(data, list) and True or False,
           "message": isinstance(data, dict) and data.get("message", None) or None,
           "data": data
       }
       return super(CustomJSONRenderer, self).render(data, accepted_media_type, renderer_context)