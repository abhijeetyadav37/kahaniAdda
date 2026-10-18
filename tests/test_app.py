import os,tempfile,unittest
from app import app,db,Story,Admin,Submission
from werkzeug.security import generate_password_hash
class AppTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.NamedTemporaryFile(suffix='.db',delete=False);self.tmp.close();app.config.update(TESTING=True,WTF_CSRF_ENABLED=False,SQLALCHEMY_DATABASE_URI='sqlite:///'+self.tmp.name,SECRET_KEY='test-secret');self.client=app.test_client()
  with app.app_context():db.drop_all();db.create_all();db.session.add(Admin(username='tester',password_hash=generate_password_hash('long-test-password')));db.session.add(Story(title='Test Story',slug='test-story',author='A Reader',genre='Romance',language='English',content='A sample story for public rendering and reading.',status='published'));db.session.commit()
 def tearDown(self):
  with app.app_context():db.session.remove();db.drop_all()
  try:os.unlink(self.tmp.name)
  except OSError:pass
 def test_public_routes(self):
  for p in ['/','/stories','/story/test-story','/about','/contact','/privacy','/terms','/copyright','/sitemap.xml','/robots.txt']:self.assertEqual(self.client.get(p).status_code,200,p)
 def test_admin_login_and_story_creation(self):
  self.assertEqual(self.client.post('/admin/login',data={'username':'tester','password':'long-test-password'},follow_redirects=True).status_code,200)
  r=self.client.post('/admin/stories/new',data={'title':'New story','slug':'new-story','author':'Writer','genre':'Mystery','language':'Hinglish','tags':'clue','content':'A new story with enough words to be saved into the database.','status':'published','featured':'yes'},follow_redirects=True);self.assertEqual(r.status_code,200)
  with app.app_context():self.assertIsNotNone(Story.query.filter_by(slug='new-story').first())
 def test_public_submission_pending(self):
  r=self.client.post('/submit-story',data={'title':'Reader Story','pen_name':'Pen','genre':'Romance','language':'Hinglish','content':'This reader story has enough characters to pass the required minimum length and enter the moderation queue.','email':'','rights_confirmed':'yes'},follow_redirects=True);self.assertEqual(r.status_code,200)
  with app.app_context():s=Submission.query.filter_by(title='Reader Story').first();self.assertIsNotNone(s);self.assertEqual(s.status,'pending')
 def test_invalid_submission(self):self.assertEqual(self.client.post('/submit-story',data={'title':'','pen_name':'','genre':'bad','language':'xx','content':'tiny','rights_confirmed':'no'}).status_code,400)
 def test_admin_requires_login(self):self.assertEqual(self.client.get('/admin').status_code,302)
if __name__=='__main__':unittest.main()
