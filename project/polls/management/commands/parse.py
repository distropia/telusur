from lxml import etree
from progressbar import ProgressBar, Percentage, Bar
from dateutil import parser, tz
from collections import OrderedDict
from phpserialize import loads, dumps, phpobject, unserialize, serialize
from django.utils.text import slugify

import re
import unidecode
import datetime
import pytz
import requests
import os
import time
import codecs
import json
import sys


DEBUG = False
FILENAME = 'telusur.wordpress.2018-09-29.xml'

tree = etree.parse(FILENAME)
namespaces = tree.getroot().nsmap

class PostWP:
    """ Ommitted from the XML standard:
            pubDate
            guid
            excerpt:encoded
            post_date_gmt
            post_type
            post_password
            is_sticky
    """
    def __init__(self, id=None, title=None):
        self.id = id
        self.title = title
        self.description = None
        self.creator = None
        self.body = None
        self.url = None
        self.post_date = datetime.datetime.now()
        self.comment_status = "open"
        self.ping_status = "open"
        self.slug = slugify(title)
        self.status = "publish"
        self.parent = None
        self.menu_order = 0
        self.tags = []
        self.categories = []
        self.comments = []
        self.choices = []
        self.answers = []
        self.attachment_id = None
        self.question_text = None
        self.votes = 0

    def adjust_paths(self, attachments=None, prefix=''):
        if prefix is not '' and not prefix.endswith('/'):
            print("[ERRR] Your attachment prefix does not end in a trailing slash")
            return False
        if self.body is not None and attachments is not None:
            for attachment in attachments:
                if attachment.url in self.body:
                    new_url = prefix + attachment.url.split('/')[-1]
                    self.body = self.body.replace(attachment.url, new_url)
                    if DEBUG:
                        print("[DEBG] Replaced " + attachment.url + " with " + new_url)

    def adjust_urls(self):
        new_url = self.url.replace('https://telusur.co.id', '')
        self.url = new_url

    def fix_paragraphs(self):
        fixed = self.body.replace('\n', '</p><p>')
        fixed = '<p>' + fixed + '</p>'
        fixed = fixed.replace('</p><p></p><p>', '</p><p>')
        self.body = fixed

    def fix_more(self):
        fixed = self.body.replace('<!--more-->', '[[MORE]]')
        self.body = fixed

    def show(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            creatior=self.creator,
            body=self.body,
            url=self.url,
            post_date=self.post_date,
            comment_status=self.comment_status,
            ping_status=self.ping_status,
            slug=self.slug,
            status=self.status,
            parent=self.parent,
            menu_order=self.menu_order,
            tags=self.tags,
            categories=self.categories,
            comments=self.comments,
            choices=self.choices,
            answers=self.answers,
            attachment_id=self.attachment_id,
            question_text=self.question_text,
            votes=self.votes
            )


class AttachmentWP:
    def __init__(self, id=None, title=None, url=None):
        self.id = id
        self.title = title
        self.url = url

    def download(self, path='attachments'):
        if self.url is not None:
            title = self.url.split('/')[-1]
            attachment = requests.get(self.url)
            if attachment.status_code == requests.codes.ok:
                try:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    f = open(os.path.join(path, title), 'wb')
                    f.write(attachment.content)
                    f.close()
                except:
                    print(sys.exc_info())
            else:
                attachment.raise_for_status()

    def adjust_path(self, prefix=''):
        new_url = prefix + self.url.replace('https://telusur.co.id/wp-content/uploads', '')
        self.url = new_url


def find_blog(tree):
    if tree.find(".//title") is not None:
        title = tree.find(".//title").text
        url = tree.find(".//link").text
        description = tree.find(".//description").text
        exported = tree.find(".//pubDate").text
        language = tree.find(".//language").text
        print("Found %s" % title)


def find_authors(tree):
    author_elems = tree.findall(".//wp:author", namespaces=namespaces)
    authors = []
    for author_elem in author_elems:
        user_id = author_elem.find("./wp:author_id", namespaces=namespaces).text
        login = author_elem.find("./wp:author_login", namespaces=namespaces).text
        email = author_elem.find("./wp:author_email", namespaces=namespaces).text
        username = author_elem.find("./wp:author_display_name", namespaces=namespaces).text
        first_name = author_elem.find("./wp:author_first_name", namespaces=namespaces).text
        last_name = author_elem.find("./wp:author_last_name", namespaces=namespaces).text
        authors.append({
            'id': user_id,
            'login': login,
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        })
    if len(authors) > 0:
        print("Found %i authors" % len(authors))
        return authors
    else:
        print("[WARN] Found no authors!")
        return False

def find_categories(tree):
    category_elems = tree.findall(".//wp:category", namespaces=namespaces)
    categories = []
    for category_elem in category_elems:
        term_id = category_elem.find("./wp:term_id", namespaces=namespaces).text
        parent = category_elem.find("./wp:category_parent", namespaces=namespaces).text
        slug = category_elem.find("./wp:category_nicename", namespaces=namespaces).text
        name = category_elem.find("./wp:cat_name", namespaces=namespaces).text
        categories.append({
            'id': term_id,
            'parent': parent,
            'slug': slug,
            'name': name
        })
    if len(categories) > 0:
        print("Found %i categories" % len(categories))
        return categories
    else:
        print("[WARN] Found no categories!")
        return False


def find_tags(tree):
    tag_elems = tree.findall(".//wp:tag", namespaces=namespaces)
    tags = []
    for tag_elem in tag_elems:
        term_id = tag_elem.find("./wp:term_id", namespaces=namespaces).text
        slug = tag_elem.find("./wp:tag_slug", namespaces=namespaces).text
        name = tag_elem.find("./wp:tag_name", namespaces=namespaces).text
        tags.append({
            'id': term_id,
            'slug': slug,
            'name': name
        })
    if len(tags) > 0:
        print("Found %i tags" % len(tags))
        return tags
    else:
        print("[WARN] Found no tags!")
        return False

def find_posts(tree, published=True):
    if published:
        xpath = ".//item[wp:post_type='post' and wp:status='publish']"
        item_elems = tree.xpath(xpath, namespaces=namespaces)
    else:
        item_elems = tree.findall(".//item[wp:post_type='post']", namespaces=namespaces)
    posts = []
    for post_elem in item_elems:
        post = PostWP(str(post_elem.find("./wp:post_id", namespaces=namespaces).text), str(post_elem.find("./title").text))
        post.creator = post_elem.find("./dc:creator", namespaces=namespaces).text
        post.url = str(post_elem.find("./link").text)
        post.body = str(post_elem.find("./content:encoded", namespaces=namespaces).text)
        post_stamp = parser.parse(post_elem.find("./wp:post_date", namespaces=namespaces).text)
        local = pytz.timezone("America/Chicago")
        local_stamp = local.localize(post_stamp, is_dst=None)
        utc_stamp = local_stamp.astimezone(pytz.utc)
        post.post_date = utc_stamp
        category_elems = post_elem.xpath("./category[@domain='category']")
        categories = []
        if category_elems is not None:
            for category in category_elems:
                categories.append(category.get('nicename'))
        post.categories = categories
        tag_elems = post_elem.xpath("./category[@domain='post_tag']")
        tags = []
        if tag_elems is not None:
            for tag in tag_elems:
                tags.append(tag.get('nicename'))
        post.tags = tags
        postmeta_elems = post_elem.xpath("./wp:postmeta", namespaces=namespaces)
        for postmeta in postmeta_elems:
            data_key = postmeta.find("./wp:meta_key", namespaces=namespaces).text
            if re.match('\_thumbnail\_id+', data_key):
                post.attachment_id = postmeta.find("./wp:meta_value", namespaces=namespaces).text
        comment_elems = post_elem.xpath("./wp:comment", namespaces=namespaces)
        comments = []
        for comment in comment_elems:
            content = comment.find("./wp:comment_content", namespaces=namespaces).text
            if content:
                comments.append(content)
        post.comments = comments
        posts.append(post)

    if len(posts) > 0:
        print("Found %i posts" % len(posts))
        return posts
    else:
        print("[WARN] Found no posts!")
        return False


def find_polls(tree, published=True):
    if published:
        xpath = ".//item[wp:post_type='poll' and wp:status='publish']"
        item_elems = tree.xpath(xpath, namespaces=namespaces)
    else:
        item_elems = tree.findall(".//item[wp:post_type='poll']", namespaces=namespaces)
    posts = []
    for post_elem in item_elems:
        post = PostWP(str(post_elem.find("./wp:post_id", namespaces=namespaces).text), str(post_elem.find("./title").text))
        post.creator = post_elem.find("./dc:creator", namespaces=namespaces).text
        post.url = str(post_elem.find("./link").text)
        post.body = str(post_elem.find("./content:encoded", namespaces=namespaces).text)
        post_stamp = parser.parse(post_elem.find("./wp:post_date", namespaces=namespaces).text)
        local = pytz.timezone("America/Chicago")
        local_stamp = local.localize(post_stamp, is_dst=None)
        utc_stamp = local_stamp.astimezone(pytz.utc)
        post.post_date = utc_stamp
        tag_elems = post_elem.xpath("./category[@domain='post_tag']")
        tags = []
        if tag_elems is not None:
            for tag in tag_elems:
                tags.append(tag.get('nicename'))
        post.tags = tags
        choices = []
        answers = []
        postmeta_elems = post_elem.xpath("./wp:postmeta", namespaces=namespaces)
        for postmeta in postmeta_elems:
            data_key = postmeta.find("./wp:meta_key", namespaces=namespaces).text
            data = postmeta.find("./wp:meta_value", namespaces=namespaces).text.encode('utf-8')
            try:
                a = loads(data, object_hook=phpobject, decode_strings=True)
                if re.match('question+', data_key):
                    post.question_text = data
                if re.match('votes+', data_key):
                    post.votes = data
                if re.match('\_thumbnail\_id+', data_key):
                    post.attachment_id = postmeta.find("./wp:meta_value", namespaces=namespaces).text
                if re.match('choice\_[0-9]{1,2}\_content+', data_key):
                    choices.append(dict(
                        label=a.get('label'),
                        visible=a.get('visible'),
                        thumbnail_id=int(a.get('thumbnail').get('id'))
                        ))
                if a.get('choices'):
                    answers.append(dict(
                        text=a.get('choices')[0],
                        ip=a.get('ip'),
                        useragent=a.get('useragent'),
                        time=a.get('time')
                        ))
            except:
                pass
        post.choices = choices
        post.answers = answers
        comment_elems = post_elem.xpath("./wp:comment", namespaces=namespaces)
        comments = []
        for comment in comment_elems:
            content = comment.xpath("./wp:comment_content", namespaces=namespaces)
            if content:
                comments.append(content)
        post.comments = comments
        posts.append(post)

    if len(posts) > 0:
        print("Found %i polls" % len(posts))
        return posts
    else:
        print("[WARN] Found no polls!")
        return False


def find_attachments(tree, download=True, path='attachments'):
    xpath = ".//item[wp:post_type='attachment']"
    attachment_elems = tree.xpath(xpath, namespaces=namespaces)
    attachments = []
    for attachment_elem in attachment_elems:
        attachment = AttachmentWP(attachment_elem.find("./wp:post_id", namespaces=namespaces).text, str(attachment_elem.find("./title").text), attachment_elem.find("./wp:attachment_url", namespaces=namespaces).text)
        attachments.append(attachment)

    published = True
    if published:
        xpath = ".//item[wp:post_type='poll' and wp:status='publish']"
        item_elems = tree.xpath(xpath, namespaces=namespaces)
    else:
        item_elems = tree.findall(".//item[wp:post_type='poll']", namespaces=namespaces)
    posts = []
    for post_elem in item_elems:
        postmeta_elems = post_elem.xpath("./wp:postmeta", namespaces=namespaces)
        for postmeta in postmeta_elems:
            data_key = postmeta.find("./wp:meta_key", namespaces=namespaces).text
            data = postmeta.find("./wp:meta_value", namespaces=namespaces).text.encode('utf-8')
            try:
                a = loads(data, object_hook=phpobject, decode_strings=True)
                if re.match('choice\_[0-9]{1,2}\_content+', data_key):
                    attachment = AttachmentWP(a.get('thumbnail').get('id'), a.get('label'), a.get('thumbnail').get('url'))
                    attachments.append(attachment)
            except:
                pass


    if len(attachments) > 0:
        print("Found %i attachments" % len(attachments))
        if download:
            print("Downloading %i attachments" % len(attachments))
            progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(attachments)).start()
            for i, attachment in enumerate(attachments):
                try:
                    attachment.download(path)
                except:
                    print(sys.exc_info())
                progress.update(i)
            progress.finish()
            print("Downloaded %i attachments" % len(attachments))
        return attachments
    else:
        print("[WARN] Found no attachments!")
        return False 