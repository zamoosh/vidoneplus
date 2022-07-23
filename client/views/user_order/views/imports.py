from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from client.models import *
from order.models import *
from django.core.paginator import Paginator
