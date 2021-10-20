import MySQLdb
from client.models import *

class Convert:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "123"
        name = "vidone"
        db = MySQLdb.connect(host, user, password, name, charset='utf8', use_unicode=True)
        self.cursor = db.cursor()
        # host = "cpanel.vidone.org"
        # user = "niasar_vidone"
        # password = "4gNmSiSjT"
        # name = "niasar_vidone"
        # db = MySQLdb.connect(host, user, password, name, charset='utf8', use_unicode=True)
        # self.cursor = db.cursor()
        # self.add_users()
        # self.add_teacher()
        # self.add_course()
        # self.add_banner()
        # self.add_zone()
        # self.add_lesson()
        # self.add_lesson_media()
        # self.add_lp_main()
        # self.add_lp_group()
        # self.add_lp_maincontent()

    def add_course(self):
        self.cursor.execute("SELECT * FROM courses")
        for item in self.cursor.fetchall():
            course = CourseVitrin()
            course.title = item[1]
            course.description = item[10]
            course.lesson_count = item[22]
            course.price = item[13]
            course.price_with_discount = item[14]
            course.teacher = item[7]
            course.save()