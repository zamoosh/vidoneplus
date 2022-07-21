from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from order.models import *
from client.models import User
from library.decorators import is_superuser
import os, mimetypes, datetime, math
