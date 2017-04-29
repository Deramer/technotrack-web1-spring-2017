from django.shortcuts import render
from django.views.generic import TemplateView
import psycopg2
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Create your views here.

class IndexView(TemplateView):
    template_name='sberhack/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        conn = psycopg2.connect('dbname=sber_hackathon user=sber_hackathon_role host=localhost password=hackathon')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Turnovers WHERE turnover != 0::money ORDER BY id')
        context['table'] = cur.fetchall()
        cur.execute("SELECT calculate_sum_with_mask_and_certification('2017-04-22', '2017-04-24', true, false, '%');")
        context['corrected_not_cert'] = cur.fetchone()[0]
        cur.execute("SELECT calculate_sum_for_period('2017-04-22', '2017-04-24', true);")
        context['general'] = cur.fetchone()[0]
        cur.execute("SELECT calculate_sum_with_mask_and_certification('2017-04-22', '2017-04-24', true, true, '%');")
        context['corrected_cert'] = cur.fetchone()[0]
        cur.execute("SELECT calculate_sum_with_mask_and_certification('2017-04-22', '2017-04-24', false, true, '%');")
        context['not_corrected_cert'] = cur.fetchone()[0]
        cur.close()
        conn.close()
        return context

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
            conn = psycopg2.connect('dbname=sber_hackathon user=sber_hackathon_role host=localhost password=hackathon')
            cur = conn.cursor()
            for key in request.POST:
                if key == 'csrfmiddlewaretoken':
                    continue
                t, i = key.split('-')
                if request.POST[key] == '':
                    continue
                if t == 'change':
                    cur.execute('SELECT correct_turnover_by_id(%s, %s::money);', (i, request.POST[key]))
                if t == 'certify':
                    cur.execute('SELECT certify_turnover_by_id(%s::bigint);', (i,))
            conn.commit()
            cur.close()
            conn.close()
            return HttpResponseRedirect('/sberhack/')
