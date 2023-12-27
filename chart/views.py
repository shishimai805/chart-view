from django.shortcuts import render
from django.http import HttpResponse

from .models import Code
from .application import stuck_graph

import glob
import os
from chartview.settings import BASE_DIR

codes_gr = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Golden_cross/継続"))
codes_gr.sort()
codes_gc = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Golden_cross/転換"))
codes_gc.sort()
codes_dr = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Dead_cross/継続"))
codes_dr.sort()
codes_dc = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Dead_cross/転換"))
codes_dc.sort()

# Create your views here.
def home(request):
    global codes_gr,codes_gc,codes_dr,codes_dc
    codes_gr = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Golden_cross/継続"))
    codes_gr.sort()
    codes_gc = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Golden_cross/転換"))
    codes_gc.sort()
    codes_dr = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Dead_cross/継続"))
    codes_dr.sort()
    codes_dc = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Dead_cross/転換"))
    codes_dc.sort()
    #for code in codes:
        #post = Code.objects.create(num=code.replace(".png",""), image=f"static/images/chart_graph/Golden_cross/転換/{code}")
    context = {}
    return render(request, 'chart/home.html', context)

def golden_row(request,index):
    #Code.objects.all().delete()  
    context = {
        "code":codes_gr[index-1],
        "f_code":codes_gr[0],
        "l_code":codes_gr[-1],
        "index":index,
    }
    return render(request, 'chart/golden_row.html', context)

def golden_chenge(request,index):
    context = {
        "code":codes_gc[index-1],
        "f_code":codes_gc[0],
        "l_code":codes_gc[-1],
        "index":index,
    }
    return render(request, 'chart/golden_chenge.html', context)

def dead_row(request,index):
    context = {
        "code":codes_dr[index-1],
        "f_code":codes_dr[0],
        "l_code":codes_dr[-1],
        "index":index,
    }
    return render(request, 'chart/dead_row.html', context)

def dead_chenge(request,index):
    context = {
        "code":codes_dc[index-1],
        "f_code":codes_dc[0],
        "l_code":codes_dc[-1],
        "index":index,
    }
    return render(request, 'chart/dead_chenge.html', context)

def do_graph(request):
    if request.method == 'GET':
        global codes_gr,codes_gc,codes_dr,codes_dc
        codes_gr = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Golden_cross/継続"))
        codes_gr.sort()
        codes_gc = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Golden_cross/転換"))
        codes_gc.sort()
        codes_dr = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Dead_cross/継続"))
        codes_dr.sort()
        codes_dc = os.listdir(os.path.join(BASE_DIR,"static/images/chart_graph/Dead_cross/転換"))
        codes_dc.sort()
        context = {}
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        stuck_graph.do_graph()
        return render(request, 'chart/home.html', context)
