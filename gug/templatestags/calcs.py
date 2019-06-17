#from django.template import Library
from django import template

register = template.Library()


def running_total(fine_list, column):

	total = 0
	for d in fine_list:
		total = total + d.get(column) 
	return total

register.filter('running_total', running_total)