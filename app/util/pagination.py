#!/usr/bin/env python# -*- coding: utf-8 -*-
from flask import url_for


class Page():
    
    @staticmethod
    def pagination_urls_sources(sources_page, url, source, **kwargs):
        next_url = url_for(url, **kwargs, sources_page=source.next_num) if source.has_next else None
        prev_url = url_for(url, **kwargs, sources_page=source.prev_num) if source.has_prev else None
        return next_url, prev_url
    
    @staticmethod
    def pagination_urls_softwares(softwares_page, url, software, **kwargs):
        next_url = url_for(url, **kwargs, softwares_page=software.next_num) if software.has_next else None
        prev_url = url_for(url, **kwargs, softwares_page=software.prev_num) if software.has_prev else None
        return next_url, prev_url