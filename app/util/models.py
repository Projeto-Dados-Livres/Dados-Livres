#!/usr/bin/env python# -*- coding: utf-8 -*-


class Query():
    def search_paginate(model, search_term, page, per_page=12):
        return model.query.filter(model.title.like(f'%{search_term}%')).order_by(
            model.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)