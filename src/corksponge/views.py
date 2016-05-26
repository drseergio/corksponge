# -*- coding: utf-8 -*-
# corksponge 
#
# Copyright: 2011 Sergey Pisarenko (drseergio@gmail.com)
# Licensed under AGPL 3.0
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.http import require_POST
from corksponge.models import Board
from corksponge.models import Image
from corksponge.shortener import code_to_id
from corksponge.shortener import id_to_code
from settings import MAX_X
from settings import MAX_Y


SAVE_PARAMS = ['x', 'y', 'height', 'width', 'url', 'board']


class CorkspongeError(Exception):
  pass


def index(request):
  now = datetime.now()
  board = Board(created_date=now, modified_date=now)
  board.save()
  return HttpResponseRedirect(id_to_code(board.id))


def display(request, code):
  board_id = code_to_id(code)
  try:
    board = Board.objects.get(id=board_id)
  except ObjectDoesNotExist:
    return HttpResponseRedirect('/')

  return render_to_response(
      'noticeboard.html',
      {'board': code,
       'max_x': MAX_X,
       'max_y': MAX_Y},
      context_instance=RequestContext(request))


@require_POST
def save(request):
  for param in SAVE_PARAMS:
    if param not in request.POST:
      return HttpResponse('Parameter \'%s\' is required' % (param), status=400)

  try:
    board = Board.objects.get(id=code_to_id(request.POST['board']))
    image = Image(
      url=request.POST['url'],
      board=board,
      created_date=datetime.now(),
      x=request.POST['x'],
      y=request.POST['y'],
      z_index=board.z_index,
      height=request.POST['height'],
      width=request.POST['width'])
    board.z_index += 1
    board.save()
    image.save()
    return HttpResponse(status=200, content=image.id)
  except Exception, e:
    return HttpResponse('%s' % e, status=400)


def get(request, code):
  board_id = code_to_id(code)
  try:
    board = Board.objects.get(id=board_id)
  except ObjectDoesNotExist:
    return HttpResponse(status=400)

  image_envelopes = []
  images = Image.objects.filter(board=board)
  images = sorted(images, key=lambda image: image.z_index)

  for image in images:
    image_envelopes.append({
      'id': image.id,
      'x': image.x,
      'y': image.y,
      'note': image.note,
      'url': image.url,
      'height': image.height,
      'width': image.width})
  return HttpResponse(simplejson.dumps(image_envelopes))


@require_POST
def update(request):
  try:
    image = _get_image(request.POST)
    if 'note' in request.POST:
      image.note = request.POST['note']
    if 'x' in request.POST and 'y' in request.POST:
      x = request.POST['x'];
      y = request.POST['y'];
      if int(x) < MAX_X and int(y) < MAX_Y:
        image.x = request.POST['x'];
        image.y = request.POST['y'];
    if 'width' in request.POST and 'height' in request.POST:
      width = request.POST['width'];
      height = request.POST['height'];
      if int(width) < 500 and int(height) < 500:
        image.width = request.POST['width'];
        image.height = request.POST['height'];
    image.save()
    return HttpResponse(status=200)
  except CorkspongeError, e:
    return HttpResponse(status=400, content='%s' % e)


@require_POST
def click(request):
  try:
    image = _get_image(request.POST)
    image.board.z_index += 1
    image.z_index = image.board.z_index
    image.board.save()
    image.save()
    return HttpResponse(status=200)
  except CorkspongeError, e:
    return HttpResponse(status=400, content='%s' % e)


@require_POST
def delete(request):
  try:
    image = _get_image(request.POST)
    image.delete()
    return HttpResponse(status=200)
  except CorkspongeError, e:
    return HttpResponse(status=400, content='%s' % e)


def _get_image(parameters):
  if 'board' not in parameters:
    raise CorkspongeError('\'board\' is a required parameter')
  if 'id' not in parameters:
    raise CorkspongeError('\'id\' is a required parameter')
  
  try:
    board = Board.objects.get(id=code_to_id(parameters['board']))
    image = Image.objects.get(id=parameters['id'])

    if image.board == board:
      return image
    else:
      raise CorkspongeError('no matching board/image found')
  except Exception, e:
    raise CorkspongeError(e)
