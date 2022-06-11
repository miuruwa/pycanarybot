import wikipedia
from googletrans import Translator
class Search:
    def __init__(self):
        wikipedia.set_lang("ru")

    def request(self, request):
        try:
            return "{}\nИсточник {}".format(wikipedia.summary(request, sentences=5), wikipedia.page(request).url)
        except:
            return "Ничего не найдено, возможно произошла ошибка, повторите позже."

    def translate(self, request, to='en'):
        try:
            return Translator().translate(request, dest=to).text
        except:
            return 'Такого языка не существует.'
