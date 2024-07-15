#!/usr/bin/env python -*- coding: utf-8 -*-
from flask import render_template
from flask_babel import _
from app import db
from app.category import bp
from app.models import Source, Software, Tag, Category

def fetch_and_render(template, category, model, model_id_attr):
    if model == Source:
        items = db.session.query(
            model.title, model.sphere, Category.category, Tag.keyword).filter(
                Category.category == category, getattr(
                Category, model_id_attr) == model.id, model.tags).order_by(
                    model.timestamp.desc()).all()
    elif model == Software:
        items = db.session.query(
            model.title, model.owner, model.license, Category.category, 
            Tag.keyword).filter(Category.category == category,
            getattr(Category, model_id_attr) == model.id, model.tags).order_by(
            model.timestamp.desc()).all()
    return render_template(template, title=_(category), items=items)
 
@bp.route('/covid19_source', methods=['GET', 'POST'])
def covid19_source():
    return fetch_and_render('category/covid19_source.html', 'Covid-19', Source, 'source_id')

@bp.route('/covid19_software', methods=['GET', 'POST'])
def covid19_software():
    return fetch_and_render('category/covid19_software.html', 'Covid-19', Software, 'software_id')

@bp.route('/cinema_source', methods=['GET', 'POST'])
def cinema_source():
    return fetch_and_render('category/cinema_source.html', 'Cinema', Source, 'source_id')

@bp.route('/cinema_software', methods=['GET', 'POST'])
def cinema_software():
    return fetch_and_render('category/cinema_software.html', 'Cinema', Software, 'software_id')

@bp.route('/science_technology_source', methods=['GET', 'POST'])
def science_technology_source():
    return fetch_and_render('category/science_technology_source.html', 'Ciência e Tecnologia', Source, 'source_id')

@bp.route('/science_technology_software', methods=['GET', 'POST'])
def science_technology_software():
    return fetch_and_render('category/science_technology_software.html', 'Ciência e Tecnologia', Software, 'software_id')

@bp.route('/health_source', methods=['GET', 'POST'])
def health_source():
    return fetch_and_render('category/health_source.html', 'Saúde', Source, 'source_id')

@bp.route('/health_software', methods=['GET', 'POST'])
def health_software():
    return fetch_and_render('category/health_software.html', 'Saúde', Software, 'software_id')

@bp.route('/oil_gas_source', methods=['GET', 'POST'])
def oil_gas_source():
    return fetch_and_render('category/oil_gas_source.html', 'Petróleo e Gás', Source, 'source_id')

@bp.route('/oil_gas_software', methods=['GET', 'POST'])
def oil_gas_software():
    return fetch_and_render('category/oil_gas_software.html', 'Petróleo e Gás', Software, 'software_id')

@bp.route('/public_safety_source', methods=['GET', 'POST'])
def public_safety_source():
    return fetch_and_render('category/public_safety_source.html', 'Segurança Pública', Source, 'source_id')

@bp.route('/public_safety_software', methods=['GET', 'POST'])
def public_safety_software():
    return fetch_and_render('category/public_safety_software.html', 'Segurança Pública', Software, 'software_id')

@bp.route('/education_source', methods=['GET', 'POST'])
def education_source():
    return fetch_and_render('category/education_source.html', 'Educação', Source, 'source_id')

@bp.route('/education_software', methods=['GET', 'POST'])
def education_software():
    return fetch_and_render('category/education_software.html', 'Educação', Software, 'software_id')

@bp.route('/statistics_source', methods=['GET', 'POST'])
def statistics_source():
    return fetch_and_render('category/statistics_source.html', 'Estatística', Source, 'source_id')

@bp.route('/statistics_software', methods=['GET', 'POST'])
def statistics_software():
    return fetch_and_render('category/statistics_software.html', 'Estatística', Software, 'software_id')

@bp.route('/environment_source', methods=['GET', 'POST'])
def environment_source():
    return fetch_and_render('category/environment_source.html', 'Meio Ambiente', Source, 'source_id')

@bp.route('/environment_software', methods=['GET', 'POST'])
def environment_software():
    return fetch_and_render('category/environment_software.html', 'Meio Ambiente', Software, 'software_id')

@bp.route('/culture_source', methods=['GET', 'POST'])
def culture_source():
    return fetch_and_render('category/culture_source.html', 'Cultura', Source, 'source_id')

@bp.route('/culture_software', methods=['GET', 'POST'])
def culture_software():
    return fetch_and_render('category/culture_software.html', 'Cultura', Software, 'software_id')

@bp.route('/geography_source', methods=['GET', 'POST'])
def geography_source():
    return fetch_and_render('category/geography_source.html', 'Geografia', Source, 'source_id')

@bp.route('/geography_software', methods=['GET', 'POST'])
def geography_software():
    return fetch_and_render('category/geography_software.html', 'Geografia', Software, 'software_id')

@bp.route('/economy_finance_source', methods=['GET', 'POST'])
def economy_finance_source():
    return fetch_and_render('category/economy_finance_source.html', 'Economia e Finanças', Source, 'source_id')

@bp.route('/economy_finance_software', methods=['GET', 'POST'])
def economy_finance_software():
    return fetch_and_render('category/economy_finance_software.html', 'Economia e Finanças', Software, 'software_id')

@bp.route('/climate_source', methods=['GET', 'POST'])
def climate_source():
    return fetch_and_render('category/climate_source.html', 'Clima', Source, 'source_id')

@bp.route('/climate_software', methods=['GET', 'POST'])
def climate_software():
    return fetch_and_render('category/climate_software.html', 'Clima', Software, 'software_id')

@bp.route('/sports_leisure_source', methods=['GET', 'POST'])
def sports_leisure_source():
    return fetch_and_render('category/sports_leisure_source.html', 'Esporte e Lazer', Source, 'source_id')

@bp.route('/sports_leisure_software', methods=['GET', 'POST'])
def sports_leisure_software():
    return fetch_and_render('category/sports_leisure_software.html', 'Esporte e Lazer', Software, 'software_id')

@bp.route('/transportation_source', methods=['GET', 'POST'])
def transportation_source():
    return fetch_and_render('category/transportation_source.html', 'Transporte', Source, 'source_id')

@bp.route('/transportation_software', methods=['GET', 'POST'])
def transportation_software():
    return fetch_and_render('category/transportation_software.html', 'Transporte', Software, 'software_id')
