from georemindme.models import *
from google.appengine.ext import db
from georoute.models import *

u = User.objects.get_by_email('a@a.com')
print u
point = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.32323,1.12345))
point.put()
point1 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.32323,1.12345))
point1.put()
point2 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.322,1.12345))
point2.put()
point3 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.321,1.12345))
point3.put()
point4 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.325,1.12345))
point4.put()

p = RoutePoint.objects.get_point(db.GeoPt(12.323,1.123))
for ass in p.users:
    print ass.email
realPoints = RoutePoint.objects.get_points([db.GeoPt(12.321,1.123)], keys_only=True)
print realPoints.count()
s = u.routeuserpoint_set.filter('point =', realPoints.get())
for sa in s:
    print sa.point
    
from georemindme.models import *
from google.appengine.ext import db
from georoute.models import *

u = User.objects.get_by_email('a@a.com')
print u
point = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.32323,1.12345))
point.put()
point1 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.32323,1.12345))
point1.put()
point2 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.322,1.12345))
point2.put()
point3 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.321,1.12345))
point3.put()
point4 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.325,1.12345))
point4.put()

l = [db.GqlQuery('SELECT __key__ FROM RoutePoint WHERE point = :1', db.GeoPt(round(p.lat, PRECISION), round(p.lon, PRECISION))).get() for p in [db.GeoPt(12.321,1.123),db.GeoPt(12.325,1.12345)]]
realPoints = RoutePoint.objects.get_points([db.GeoPt(12.321,1.123),db.GeoPt(12.325,1.12345)])
print realPoints

print RouteUserPoint.objects.get_points(u, [db.GeoPt(12.322,1.12345),db.GeoPt(12.322,1.12345),db.GeoPt(12.322,1.12345),db.GeoPt(12.322,1.12345),db.GeoPt(12.32323,1.12345),db.GeoPt(12.321,1.123),db.GeoPt(12.325,1.12345)])

    
from georemindme.models import *
from google.appengine.ext import db
from georoute.models import *

u = User.objects.get_by_email('a@a.com')
point = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.32323,1.12345))
point.put()
point1 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.32323,1.12345))
point1.put()
point2 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.322,1.12345))
point2.put()
point3 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.321,1.12345))
point3.put()
point4 = RouteUserPoint.objects.get_or_insert(u, db.GeoPt(12.325,1.12345))
point4.put()

a = RouteUserPath.objects.get_or_insert(u, [point2,point3,point4])
a = RouteUserPath.objects.get_or_insert(u, [point1,point4])

p = RouteUserPath.objects.get_possible_paths(u, points=[point1, point2, point3])
p = RoutePath.objects.get_possible_paths(points=[point1.point, point2.point, point3.point], possiblePaths=p)
p = RoutePath.objects.get_possible_paths(points=[point4.point], possiblePaths=p)
