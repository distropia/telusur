import pytz

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from polls.models import Question, Choice, Information
from posts.models import Post, Category, Tag, Attachment
from progressbar import ProgressBar, Percentage, Bar
from .parse import *


class Command(BaseCommand):
    help = 'Import wordpress data'

    authors = []
    categories = []
    tags = []
    posts = []
    polls = []
    attachments = []
    attachment_path = os.path.join('static/attachments/')
    default_password = 'telusur1234'

    def handle(self, *args, **options):
        try:
            self.authors = find_authors(tree)
            self.categories = find_categories(tree)
            self.tags = find_tags(tree)
            self.attachments = find_attachments(tree, False, self.attachment_path)
            self.posts = find_posts(tree)
            self.polls = find_polls(tree)
        except:
            self.stdout.write(self.style.ERROR(str(sys.exc_info())))
        
        self.import_authors()
        self.import_categories()
        self.import_tags()
        self.import_attachments()
        self.import_posts()
        self.import_polls()
        
        self.stdout.write(self.style.SUCCESS("Successfully import wordpress data."))


    def import_authors(self):        
        self.stdout.write(self.style.MIGRATE_LABEL("Importing Authors"))
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.authors)).start()
        for i, author in enumerate(self.authors):
            objAuthor = User(
                id=author.get('id'),
                username=author.get('login'),
                email=author.get('email'), 
                first_name=author.get('first_name'), 
                last_name=author.get('last_name')
                )
            objAuthor.set_password(self.default_password)
            objAuthor.save()
            progress.update(i)
        progress.finish()

    def import_categories(self):
        self.stdout.write(self.style.MIGRATE_LABEL("Importing Categories"))
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.categories) * 2).start()
        for i, category in enumerate(self.categories):
            objCategory = Category(
                id=category.get('id'),
                name=category.get('name'),
                slug=category.get('slug')
                )
            objCategory.save()
            progress.update(i)
        for i, category in enumerate(self.categories):
            objCategory = Category.objects.get(pk=category.get('id'))
            objCategory.parent = Category.objects.get(slug=category.get('parent')) if category.get('parent') else None
            objCategory.save()
            progress.update(i)        
        progress.finish()

    def import_tags(self):
        self.stdout.write(self.style.MIGRATE_LABEL("Importing Tags"))
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.tags)).start()
        for i, tag in enumerate(self.tags):
            objTag = Tag(
                id=tag.get('id'),
                name=tag.get('name'),
                slug=tag.get('slug')
                )
            objTag.save()
            progress.update(i)
        progress.finish()

    def import_attachments(self):
        self.stdout.write(self.style.MIGRATE_LABEL("Importing Attachments"))
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.attachments)).start()
        for i, attachment in enumerate(self.attachments):
            # attachment.adjust_path(self.attachment_path) 
            extension = attachment.url.split(".")[-1] 
            objAtt = Attachment( 
                id=attachment.id, 
                title=attachment.title, 
                path=self.attachment_path + attachment.title.replace(" ", "-") + "." + extension,
                attch_type = "featured_image"
                )
            objAtt.save()
            progress.update(i)
        progress.finish()

    def import_posts(self):
        self.stdout.write(self.style.MIGRATE_LABEL("Importing Posts"))
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.posts)).start()
        for i, post in enumerate(self.posts):
            # post.adjust_paths(attachments=self.attachments, prefix=self.attachment_path)
            post.adjust_urls()
            post.fix_paragraphs()
            post.fix_more()
            attachment = None
            if post.attachment_id:
                attachment = Attachment.objects.get(pk=post.attachment_id)
            objPost = Post(
                id=post.id,
                title=post.title,
                author=User.objects.get(username=post.creator),
                content=post.body,
                url=post.url,
                slug=post.slug,
                attachment=attachment,
                publish=True,
                pub_date=post.post_date
                )

            counter = 1
            result = None
            while result is None:
                try:
                    if counter > 1:
                        objPost.slug = post.slug + "-" + str(counter)
                    counter = counter + 1
                    objPost.save()
                    result = True
                except IntegrityError as e:
                    self.style.ERROR(str(e))
                
            tags = []
            for tag in post.tags:
                tag = Tag.objects.get(slug=tag)
                objPost.tags.add(tag)
                objPost.save()
            categories = []
            for category in post.categories:
                category = Category.objects.get(slug=category)
                objPost.categories.add(category)
                objPost.save()
            progress.update(i)
        progress.finish()

    def import_polls(self):
        self.stdout.write(self.style.MIGRATE_LABEL("Importing Polls"))
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.polls)).start()
        defect = 0
        for i, post in enumerate(self.polls):
            # post.adjust_paths(attachments=self.attachments, prefix=self.attachment_path)
            post.adjust_urls()
            post.fix_paragraphs()
            post.fix_more()
            attachment = None
            if post.attachment_id:
                attachment = Attachment.objects.get(pk=post.attachment_id)
            objPoll = Question(
                id=post.id,
                title=post.title,
                question_text=post.question_text,
                author=User.objects.get(username=post.creator),
                content=post.body,
                url=post.url,
                slug=post.slug,
                attachment=attachment,
                publish=True,
                pub_date=post.post_date,
                # votes=post.votes
                )
            objPoll.save()
            for choice in post.choices:
                attachment = None
                if choice.get('thumbnail_id'):
                    attachment = Attachment.objects.get(pk=choice.get('thumbnail_id'))
                objChoice = Choice(
                    question=objPoll,
                    choice_text=choice.get('label'),
                    attachment=attachment,
                    visible=choice.get('visible'),
                    # votes=choice.get('votes')
                    )
                objChoice.save()
            for answer in post.answers:
                try:
                    choice = Choice.objects.get(choice_text=answer.get('text'))
                    objAnswer = Information(
                        choice=choice,
                        ip_address=answer.get('ip'),
                        useragent=answer.get('useragent'),
                        created_at=datetime.datetime.fromtimestamp(answer.get('time'), tz=pytz.utc)
                        )
                    objPoll.votes = objPoll.votes + 1
                    choice.votes = choice.votes + 1
                    choice.save()
                    objAnswer.save()
                except:
                    defect = defect + 1
                    pass
            objPoll.save()
            tags = []
            for tag in post.tags:
                tag = Tag.objects.get(slug=tag)
                objPoll.tags.add(tag)
                objPoll.save()
            progress.update(i)
        progress.finish()
        self.stdout.write(self.style.ERROR("DEFECT answers: " + str(defect)))