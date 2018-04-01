# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Restaurant(models.Model):
    m_name = models.CharField(max_length=100)
    m_address = models.CharField(max_length=100)
    m_score = models.IntegerField(default = 0)
    def __str__(self):
        return self.m_name

class Route(models.Model):
    m_time = models.IntegerField(default = 0)
    def __str__(self):
        return self.m_time
    
class Way(models.Model):
    m_route = models.ForeignKey(Route, on_delete=models.CASCADE)
    m_path = models.CharField(max_length = 500)
    def __str__(self):
        return self.m_path
    
class use(models.Model):
    m_loc = models.CharField(max_length = 500)
    m_dis = models.IntegerField(default = 0)
    def __str__(self):
        return self.m_loc



