# -*- coding: utf-8 -*-
# corksponge 
#
# Copyright: 2011 Sergey Pisarenko (drseergio@gmail.com)
# Licensed under AGPL 3.0
from django.db import models


class Board(models.Model):
  created_date = models.DateField()
  modified_date = models.DateField()
  z_index = models.PositiveIntegerField(default=0)


class Image(models.Model):
  url = models.URLField()
  board = models.ForeignKey(Board)
  created_date = models.DateField()
  note = models.TextField(blank=True)
  x = models.PositiveIntegerField()
  y = models.PositiveIntegerField()
  z_index = models.IntegerField()
  height = models.PositiveIntegerField()
  width = models.PositiveIntegerField()
