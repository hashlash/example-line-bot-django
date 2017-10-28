from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def index(request):
  if request.method == 'POST':
      signature = request.META['HTTP_X_LINE_SIGNATURE']
      body = request.body.decode('utf-8')

      try:
          events = parser.parse(body, signature)
      except InvalidSignatureError:
          return HttpResponseForbidden()
      except LineBotApiError:
          return HttpResponseBadRequest()

      for event in events:
          if isinstance(event, MessageEvent):
              if isinstance(event.message, TextMessage):
                  try:
                      line_bot_api.reply_message(
                          event.reply_token,
                          TextSendMessage(text=event.message.text)
                      )
                  except LineBotApiError as e:
                      print(e.status_code)
                      print(e.error.message)
                      print(e.error.details)

      return HttpResponse()
  else:
      return HttpResponseBadRequest()