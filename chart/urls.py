from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="Home"),
	path('golden_row/<int:index>', views.golden_row, name="Golden_row"),
	path('golden_chenge/<int:index>', views.golden_chenge, name="Golden_chenge"),
    path('dead_row/<int:index>', views.dead_row, name="Dead_row"),
	path('dead_chenge/<int:index>', views.dead_chenge, name="Dead_chenge"),
    path('home', views.do_graph, name="graph"),
]