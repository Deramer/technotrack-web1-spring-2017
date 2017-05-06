from django.shortcuts import render
from django.views.generic import TemplateView

from quizlet.models import Translation, Word

import logging
from random import randint

# Create your views here.

class IndexView(TemplateView):
    template_name = 'quizlet/index.html'
    logger = logging.getLogger('debug')

    def create(self, *args, **kwargs):
        f = open('quizlet/words.txt', 'r')
        base_word = None
        trans = None
        syn = []
        for line in f:
            line = line[:-1]
            if base_word == None:
                line = line[1:].strip()
            try:
                int(line[0])
            except ValueError:
                if line[0] >= 'a' and line[0] <= 'z':
                    if base_word != None:
                        for i in range(0, len(syn)):
                            for j in range(i+1, len(syn)):
                                syn[i].synonims.add(syn[j])
                                syn[i].save()
                    base_word = line
                else:
                    trans = Translation(translation=line)
                    trans.save()
                    word = Word(set_num=1, word=base_word, translation = trans)
                    word.save()
                    syn = [word,]
            else:
                word = Word(set_num=1, word=line[2:].strip(), translation=trans)
                word.save()
                syn.append(word)
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class RefreshView(TemplateView):
    template_name = 'quizlet/ajax.html'
    logger = logging.getLogger('debug')

    def get_context_data(self, **kwargs):
        context = super(RefreshView, self).get_context_data(**kwargs)
        context['lang'] = self.request.GET['lang']
        context['set_num'] = self.request.GET['set_num']
        if self.request.GET.get('id', None) is None:
            if self.request.GET['lang'] == 'ru':
                trans = context['trans'] = Translation.objects.order_by('?')[0]
                context['words'] = trans.word_set.all()
        else:
            trans = Translation.objects.get(id=int(self.request.GET['id']))
            words_obj = trans.word_set.all()
            words = set(map(lambda x: x.word, trans.word_set.all()))
            self.logger.debug(self.request.GET.getlist('answer'))
            self.logger.debug(words)
            if (words == set(self.request.GET.getlist('answer'))):
                trans = context['trans'] = Translation.objects.all()[randint(0, Translation.objects.count()-1)]
                context['words'] = trans.word_set.all()
                return context
            else:
                context['trans'] = trans
                context['words'] = words_obj
                context['help'] = words_obj
        return context
