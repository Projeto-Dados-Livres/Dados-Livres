#!/usr/bin/env python# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.form import EditProfileForm, EditPasswordForm, SourceForm, \
    EditSourceForm, SoftwareForm, EditSoftwareForm, SearchForm, \
    SourceTitlesForm, SoftwareTitlesForm
from app.models import User, Source, Software, Tag, Category
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased
from app.main import bp
from app.util.models import Query
from app.util.pagination import Page

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/_similar_sources', methods=['GET'])
def similar_sources():
    source_title = Source.query.all()
    sources = [r.as_dict() for r in source_title]
    return jsonify(sources)

@bp.route('/_similar_softwares', methods=['GET'])
def similar_softwares():
    software_title = Software.query.all()
    softwares = [r.as_dict() for r in software_title]
    return jsonify(softwares)

@bp.route('/_tag', methods=['GET'])
def tag():
    keyword = Tag.query.all()
    tags = [r.as_dict() for r in keyword]
    return jsonify(tags)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    sources = db.session.query(Source.title, Source.sphere, Category.category, Tag.keyword).filter(
            Category.source_id == Source.id, Source.tags).order_by(Source.timestamp.desc()).paginate(
                page=page, per_page=4, error_out=False)
    softwares = db.session.query(Software.title, Software.owner, Software.license, Category.category, Tag.keyword).filter(
            Category.software_id == Software.id, Software.tags).order_by(Software.timestamp.desc()).paginate(
                page=page, per_page=4, error_out=False)
    
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search.data
        return redirect(url_for('main.search', title=search_term))
    
    return render_template('index.html', title=_('Página Inicial'), sources=sources.items, 
                           softwares=softwares.items, form=form)

@bp.route('/search/<title>', methods=['GET', 'POST'])
def search(title):
    sources_page = request.args.get('sources_page', 1, type=int)
    softwares_page = request.args.get('softwares_page', 1, type=int)
    
    source_results = Query.search_paginate(Source, title, sources_page)
    software_results = Query.search_paginate(Software, title, softwares_page)
    
    if not source_results.items and not software_results.items:
        flash(_('Nenhum resultado encontrado para "%s"' % title))
        return redirect(url_for('main.index'))
    
    sources_next_url, sources_prev_url = Page.pagination_urls_sources(
        sources_page, 'main.search', source_results, title=title)
    softwares_next_url, softwares_prev_url = Page.pagination_urls_softwares(
        softwares_page, 'main.search', software_results, title=title)
    
    return render_template('search.html', title=_('Busca'), source_results=source_results, 
                           software_results=software_results, sources_next_url=sources_next_url, 
                           sources_prev_url=sources_prev_url, softwares_next_url=softwares_next_url, 
                           softwares_prev_url=softwares_prev_url)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/source', methods=['GET', 'POST'])
def source():
    return render_template('source.html', title=(_('Fontes')))

@bp.route('/software', methods=['GET', 'POST'])
def software():
    return render_template('software.html', title=(_('Aplicações')))

@bp.route('/register_source', methods=['GET', 'POST'])
@login_required
def register_source():
    form = SourceForm()
    if form.validate_on_submit():
        source = Source(title=form.title.data, city=form.city.data,
        state=form.state.data, country=form.country.data,
        description=form.description.data, sphere=form.sphere.data,
        officialLink=form.officialLink.data, 
        treatedLink=form.treatedLink.data, 
        author=current_user)
        db.session.add(source)
        db.session.flush()
        category = Category(category=form.category.data, source_id=source.id)
        db.session.add(category)
        db.session.flush()
        tag = Tag(keyword=form.keyword.data)
        db.session.add(tag)
        db.session.flush()
        source.tags.append(tag)
        db.session.commit()
        flash(_('A fonte "%s" foi registrada com sucesso.' % source.title))
        return redirect(url_for('main.source_profile', title=source.title))
    return render_template('register_source.html', title=(_('Cadastrar Fonte')),
        form=form)

@bp.route('/source_profile/<title>', methods=['GET', 'POST'])
def source_profile(title):
    source = Source.query.filter_by(title=title).first_or_404()
    sources_page = request.args.get('sources_page', 1, type=int)
    
    subquery = db.session.query(Category.category).filter(Category.source_id == source.id).subquery()
    SourceAlias = aliased(Source)
    
    similar_sources = db.session.query(SourceAlias.title, Category.category).filter(
        Category.source_id == SourceAlias.id, Category.category.in_(subquery), 
        SourceAlias.id != source.id).order_by(SourceAlias.timestamp.desc()).paginate(
            page=sources_page, per_page=4, error_out=False)
    
    sources_next_url, sources_prev_url = Page.pagination_urls_sources(
        sources_page, 'main.source_profile', similar_sources, title=title)
    
    form = SoftwareTitlesForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            return redirect(url_for('auth.login'))
        
        title_software = Software.query.filter_by(title=form.title.data).first()
        if title_software:
            if title_software not in source.similar:
                source.similar.append(title_software)
                db.session.add(title_software)
                db.session.commit()
                flash(_('A aplicação "%s" foi adicionada à fonte com sucesso.' % title_software.title))
            else:
                flash(_('A aplicação "%s" já está associada à fonte.' % title_software.title))
        else:
            flash(_('A aplicação "%s" não foi encontrada.' % form.title.data))
    
    softwares = source.similar
    
    return render_template('source_profile.html', title=(_('Perfil da Fonte')), source=source, 
                           similar_sources=similar_sources, sources_next_url=sources_next_url, 
                           sources_prev_url=sources_prev_url, form=form, softwares=softwares)

@bp.route('/edit_source/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_source(id):
    source = Source.query.get_or_404(id)
    tag = Tag.query.filter(Source.tags, Source.id == id).first_or_404()
    category = Category.query.filter(
        Category.source_id == Source.id, Source.id == id).first_or_404()
    form = EditSourceForm()
    if form.validate_on_submit():
        source.title = Source.title
        tag.keyword = form.keyword.data
        category.category = form.category.data
        source.officialLink = form.officialLink.data
        source.treatedLink = form.treatedLink.data
        source.sphere = form.sphere.data
        source.city = form.city.data
        source.state = form.state.data
        source.country = form.country.data
        source.description = form.description.data
        db.session.add(source)
        db.session.flush()
        db.session.add(tag)
        db.session.flush()
        db.session.add(category)
        db.session.flush()
        db.session.commit()
        flash(_('A fonte "%s" foi editada com sucesso.' % source.title))
        return redirect(url_for('main.source_profile', title=source.title))
    form.title.data = source.title
    form.keyword.data = tag.keyword
    form.category.data = category.category
    form.officialLink.data = source.officialLink
    form.treatedLink.data = source.treatedLink
    form.sphere.data = source.sphere
    form.city.data = source.city
    form.state.data = source.state
    form.country.data = source.country
    form.description.data = source.description
    return render_template('edit_source.html', title=(_('Editar Fonte')),
            form=form, source=source, tag=tag, category=category)

@bp.route("/deletar_source/<int:id>")
@login_required
def deletar_source(id):
    source = Source.query.filter_by(id=id).first()
    category = Category.query.filter(
        Category.source_id == Source.id, Source.id == id).first_or_404()
    db.session.delete(source)
    db.session.flush()
    db.session.delete(category)
    db.session.flush()
    db.session.commit()
    flash(_('A fonte "%s" foi apagada com sucesso.' % source.title))
    return redirect(url_for("main.index"))

@bp.route('/register_software', methods=['GET', 'POST'])
@login_required
def register_software():
    form = SoftwareForm()
    if form.validate_on_submit():
        software = Software(title=form.title.data,
        description=form.description.data, officialLink=form.officialLink.data,
        license=form.license.data, owner=form.owner.data,
        dateCreation=form.dateCreation.data, author=current_user)
        db.session.add(software)
        db.session.flush()
        category = Category(category=form.category.data, software_id=software.id)
        db.session.add(category)
        db.session.flush()
        tag = Tag(keyword=form.keyword.data)
        db.session.add(tag)
        db.session.flush()
        software.tags.append(tag)
        db.session.commit()
        flash('A aplicação "%s" foi registrada com sucesso.' % software.title)
        return redirect(url_for('main.software_profile', title=software.title))
    return render_template('register_software.html', title=(_('Cadastrar Aplicação')),
        form=form)

@bp.route('/software_profile/<title>', methods=['GET', 'POST'])
def software_profile(title):
    software = Software.query.filter_by(title=title).first_or_404()
    softwares_page = request.args.get('softwares_page', 1, type=int)
    
    subquery = db.session.query(Category.category).filter(Category.software_id == software.id).subquery()
    SoftwareAlias = aliased(Software)
    
    similar_softwares = db.session.query(SoftwareAlias.title, Category.category).filter(
        Category.software_id == SoftwareAlias.id, Category.category.in_(subquery), 
        SoftwareAlias.id != software.id).order_by(SoftwareAlias.timestamp.desc()).paginate(
            page=softwares_page, per_page=4, error_out=False)
    
    softwares_next_url, softwares_prev_url = Page.pagination_urls_softwares(
        softwares_page, 'main.software_profile', similar_softwares, title=title)
    
    form = SourceTitlesForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            return redirect(url_for('auth.login'))
        
        title_source = Source.query.filter_by(title=form.title.data).first()
        if title_source:
            if title_source not in software.similar:
                software.similar.append(title_source)
                db.session.add(title_source)
                db.session.commit()
                flash(_('A fonte "%s" foi adicionada à aplicação com sucesso.' % title_source.title))
            else:
                flash(_('A fonte "%s" já está associada à aplicação.' % title_source.title))
        else:
            flash(_('A fonte "%s" não foi encontrada.' % form.title.data))
    
    sources = software.similar
    
    return render_template('software_profile.html', title=(_('Perfil da Aplicação')), software=software, 
                           similar_softwares=similar_softwares, softwares_next_url=softwares_next_url, 
                           softwares_prev_url=softwares_prev_url, form=form, sources=sources)

@bp.route('/edit_software/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_software(id):
    software = Software.query.get_or_404(id)
    tag = Tag.query.filter(Software.tags, Software.id == id).first_or_404()
    category = Category.query.filter(
        Category.software_id == Software.id, Software.id == id).first_or_404()
    form = EditSoftwareForm()
    if form.validate_on_submit():
        software.title = Software.title
        tag.keyword = form.keyword.data
        category.category = form.category.data
        software.officialLink = form.officialLink.data
        software.owner = form.owner.data
        software.dateCreation = form.dateCreation.data
        software.license = form.license.data
        software.description = form.description.data
        db.session.add(software)
        db.session.flush()
        db.session.add(tag)
        db.session.flush()
        db.session.add(category)
        db.session.flush()
        db.session.commit()
        flash(_('A aplicação "%s" foi editada com sucesso.' % software.title))
        return redirect(url_for('main.software_profile', title=software.title))
    form.title.data = software.title
    form.keyword.data = tag.keyword
    form.category.data = category.category
    form.officialLink.data = software.officialLink
    form.owner.data = software.owner
    form.dateCreation.data = software.dateCreation
    form.license.data = software.license
    form.description.data = software.description
    return render_template('edit_software.html', title=(_('Editar Aplicação')),
        form=form, software=software, tag=tag, category=category)

@bp.route("/deletar_software/<int:id>")
@login_required
def deletar_software(id):
    software = Software.query.filter_by(id=id).first()
    category = Category.query.filter(
        Category.software_id == Software.id, Software.id == id).first_or_404()
    db.session.delete(software)
    db.session.flush()
    db.session.delete(category)
    db.session.flush()
    db.session.commit()
    flash(_('A aplicação "%s" foi apagada com sucesso.' % software.title))
    return redirect(url_for("main.index"))

@bp.route('/user/<nickname>', methods=['GET', 'POST'])
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first_or_404()
    sources_page = request.args.get('sources_page', 1, type=int)
    softwares_page = request.args.get('softwares_page', 1, type=int)
    
    sources = db.session.query(Source.title, Source.sphere, Category.category, Tag.keyword).filter(
        Category.source_id == Source.id, Source.tags, Source.user_id == user.id).order_by(
            Source.timestamp.desc()).paginate(page=sources_page, per_page=4, error_out=False)
    softwares = db.session.query(Software.title, Software.owner, Software.license, Category.category, Tag.keyword).filter(
        Category.software_id == Software.id, Software.tags, Software.user_id == user.id).order_by(
            Software.timestamp.desc()).paginate(page=softwares_page, per_page=4, error_out=False)
    
    sources_next_url, sources_prev_url = Page.pagination_urls_sources(sources_page, 'main.user', sources, nickname=nickname)
    softwares_next_url, softwares_prev_url = Page.pagination_urls_softwares(softwares_page, 'main.user', softwares, nickname=nickname)
    
    return render_template('user.html', title=_('Perfil do Usuário'), user=user, sources=sources, softwares=softwares, 
                           sources_next_url=sources_next_url, sources_prev_url=sources_prev_url, 
                           softwares_next_url=softwares_next_url, softwares_prev_url=softwares_prev_url)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.nickname)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Suas alterações foram salvas'))
        return redirect(url_for('main.user', nickname=current_user.nickname))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=(_('Editar Perfil')),
                           form=form)

@bp.route('/deletar_user/<int:id>')
@login_required
def deletar_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    flash(_('O usuário "%s" foi excluído.' % user.username))
    return redirect(url_for("main.index"))

@bp.route('/edit_password', methods=["GET", "POST"])
@login_required
def edit_password():
    form = EditPasswordForm(current_user.username)
    if form.validate_on_submit():
        current_user.password_hash = form.senha
        db.session.commit()
        flash(_('Sua nova senha foi salva'))
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.senha = current_user.password_hash
    return render_template('edit_password.html', title=(_('Editar Senha')), form=form)

@bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title=(_('Sobre')))

@bp.route('/how_to_contribute', methods=['GET', 'POST'])
def how_to_contribute():
    return render_template('how_to_contribute.html', title=(_('Como contribuir')))

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', title=(_('Contato')))

"""@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    while current_user.is_authenticated:
        if form.validate_on_submit():
            current_user.username = form.username.data
        elif request.method == 'GET':
            form.username.data = current_user.username
        if request.method == 'POST':
            msg = Message(form.username.data, sender='dadoslivres.testes@gmail.com',
            recipients=['m.carolina.soares1@gmail.com'])
            msg.body = "Enviado por: %s E-mail: %s Assunto: %s Mensagem: %s" % 
            (form.username.data, form.email.data, form.subject.data, form.message.data)
            mail.send(msg)
            flash(_('Seu e-mail foi enviado, agradecemos pelo contato'))
            return render_template('contact.html', title=(_('Contato')), form=form)
        elif request.method == 'GET':
            return render_template('contact.html', title=(_('Contato')), form=form)

    if request.method == 'POST':
        msg = Message(form.username.data, sender='dadoslivres.testes@gmail.com',
        recipients=['m.carolina.soares1@gmail.com'])
        msg.body = "Enviado por: %s E-mail: %s Assunto: %s Mensagem: %s" % 
        (form.username.data, form.email.data, form.subject.data, form.message.data)
        mail.send(msg)
        flash(_('Seu e-mail foi enviado, agradecemos pelo contato'))
        return render_template('contact.html', title=(_('Contato')), form=form)
    elif request.method == 'GET':
        return render_template('contact.html', title=(_('Contato')), form=form)"""

@bp.route('/ranking', methods=['GET', 'POST'])
def ranking():
    sources_user = db.session.query(User).join(
        User.sources).group_by(User).order_by(
        desc(func.count(Source.user_id))).limit(15)
    softwares_user = db.session.query(User).join(
        User.softwares).group_by(User).order_by(
        desc(func.count(Software.user_id))).limit(15)
    return render_template('ranking.html', sources_user=sources_user,
        softwares_user=softwares_user, title=(_('Ranking de Colaboração')))

@bp.route('/terms', methods=['GET', 'POST'])
def terms():
    return render_template('terms.html', title=(_('Termos e Condições')))

@bp.route('/common_questions', methods=['GET', 'POST'])
def common_questions():
    return render_template('common_questions.html', title=(_('Perguntas Frequentes')))

@bp.route('/privacy_policy', methods=['GET', 'POST'])
def privacy_policy():
    return render_template('privacy_policy.html', title=(_('Política de Privacidade')))

@bp.route('/about_us_and_contributors', methods=['GET', 'POST'])
def about_us_and_contributors():
    return render_template('about_us_and_contributors.html', 
                           title=(_('Saiba mais sobre nós e nossos contribuidores')))
