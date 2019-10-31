from django.test import TestCase

# Create your tests here.
import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BBS.settings")
    import django

    django.setup()

    from blog import models

    # #####################基于对象查询(子查询)##############################
    #                按字段（publish）
    # 一对多   book  ----------------->  publish
    #               <----------------
    #                 book_set.all()

    # 正向查询按字段：

    # 查询python这本书籍的出版社的邮箱

    # python=models.Book.objects.filter(title="python").first()
    # print(python.publish.email)

    # 反向查询按     表名小写_set.all()

    # 苹果出版社出版的书籍名称

    # publish_obj=models.Publish.objects.filter(name="苹果出版社").first()
    # for obj in publish_obj.book_set.all():
    #     print(obj.title)

    #                按字段（authors.all()）
    # 多对多   book  ----------------------->  author
    #               <----------------
    #                  book_set.all()

    # 查询python作者的年龄
    # python = models.Book.objects.filter(title="python").first()
    # for author in python.authors.all():
    #     print(author.name ,author.age)

    # 查询alex出版过的书籍名称

    # alex=models.Author.objects.filter(name="alex").first()
    # for book in alex.book_set.all():
    #     print(book.title)

    #                  按字段 authorDetail
    # 一对一   author  ----------------------->  authordetail
    #                <----------------
    #                  按表名  author

    # 查询alex的手机号
    # alex=models.Author.objects.filter(name='alex').first()
    # print(alex.authorDetail.telephone)

    # 查询家在山东的作者名字

    # ad_list=models.AuthorDetail.objects.filter(addr="shandong")
    #
    # for ad in ad_list:
    #     print(ad.author.name)

    '''
    对应sql:

       select publish_id from Book where title="python"
       select email from Publish where nid =   1


    '''

    # #####################基于queryset和__查询（join查询）############################

    # 正向查询：按字段  反向查询：表名小写

    # 查询python这本书籍的出版社的邮箱
    # ret=models.Book.objects.filter(title="python").values("publish__email")
    # print(ret.query)

    '''
    select publish.email from Book 
    left join Publish on book.publish_id=publish.nid 
    where book.title="python"
    '''

    # 苹果出版社出版的书籍名称
    # 方式1：
    ret1 = models.Publish.objects.filter(name="苹果出版社").values("book__title")
    print("111111111====>", ret1.query)
    # 方式2：
    ret2 = models.Book.objects.filter(publish__name="苹果出版社").values("title")
    print("2222222222====>", ret2.query)

    # 查询alex的手机号
    # 方式1：
    ret = models.Author.objects.filter(name="alex").values("authorDetail__telephone")

    # 方式2：
    models.AuthorDetail.objects.filter(author__name="alex").values("telephone")

    # 查询手机号以151开头的作者出版过的书籍名称以及书籍对应的出版社名称

    ret = models.Book.objects.filter(authors__authorDetail__telephone__startswith="151").values('title',
                                                                                                "publish__name")
    print(ret.query)
