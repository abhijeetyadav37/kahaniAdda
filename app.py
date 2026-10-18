import os,re,time
from datetime import datetime
from functools import wraps
from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import or_
BASE=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config.update(SECRET_KEY=os.getenv('SECRET_KEY','development-only-change-before-deploy'),SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL','sqlite:///'+os.path.join(BASE,'kahani_adda.db')).replace('postgres://','postgresql://',1),SQLALCHEMY_TRACK_MODIFICATIONS=False,SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',SESSION_COOKIE_SECURE=os.getenv('COOKIE_SECURE','0')=='1',MAX_CONTENT_LENGTH=1024*1024)
db=SQLAlchemy(app); csrf=CSRFProtect(app)
GENRES=['Romance','Horror','Thriller','Mystery','Comedy','Fantasy','Motivation','Emotional','Friendship','Life Stories','Crime Fiction']; LANGUAGES=['Hinglish','हिंदी','English']
class Admin(db.Model):
 id=db.Column(db.Integer,primary_key=True); username=db.Column(db.String(80),unique=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False)
class Story(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180),nullable=False); slug=db.Column(db.String(200),unique=True,nullable=False,index=True); author=db.Column(db.String(100),nullable=False); genre=db.Column(db.String(40),nullable=False); tags=db.Column(db.String(300),default=''); language=db.Column(db.String(20),nullable=False); content=db.Column(db.Text,nullable=False); status=db.Column(db.String(20),default='draft',index=True); featured=db.Column(db.Boolean,default=False); created_at=db.Column(db.DateTime,default=datetime.utcnow); translations=db.relationship('Translation',backref='story',cascade='all, delete-orphan')
 @property
 def reading_minutes(self): return max(1,round(len(self.content.split())/200+.49))
class Translation(db.Model):
 id=db.Column(db.Integer,primary_key=True); story_id=db.Column(db.Integer,db.ForeignKey('story.id'),nullable=False); language=db.Column(db.String(20),nullable=False); title=db.Column(db.String(180),nullable=False); content=db.Column(db.Text,nullable=False); __table_args__=(db.UniqueConstraint('story_id','language'),)
class Submission(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180),nullable=False); pen_name=db.Column(db.String(100),nullable=False); genre=db.Column(db.String(40),nullable=False); language=db.Column(db.String(20),nullable=False); content=db.Column(db.Text,nullable=False); email=db.Column(db.String(254),default=''); rights_confirmed=db.Column(db.Boolean,default=False); status=db.Column(db.String(24),default='pending',index=True); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Setting(db.Model): key=db.Column(db.String(80),primary_key=True); value=db.Column(db.String(500),default='')
def slugify(s): return (re.sub(r'[-\s]+','-',re.sub(r'[^\w\s-]','',s.lower(),flags=re.UNICODE)).strip('-') or 'story')[:190]
def admin_required(f):
 @wraps(f)
 def w(*a,**k):
  if not session.get('admin_id'): flash('Please sign in first.','error'); return redirect(url_for('admin_login'))
  return f(*a,**k)
 return w
@app.context_processor
def globals_for_templates():
 x=Setting.query.filter_by(key='ads_enabled').first()
 return dict(genres=GENRES,languages=LANGUAGES,is_admin=bool(session.get('admin_id')),ads_enabled=bool(x and x.value=='1'),site_url=os.getenv('SITE_URL',request.url_root.rstrip('/')))
@app.after_request
def headers(r):
 r.headers.setdefault('X-Content-Type-Options','nosniff'); r.headers.setdefault('X-Frame-Options','SAMEORIGIN'); r.headers.setdefault('Referrer-Policy','strict-origin-when-cross-origin'); r.headers.setdefault('Permissions-Policy','camera=(), microphone=(), geolocation=()'); r.headers.setdefault('Content-Security-Policy',"default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; img-src 'self' data:; frame-ancestors 'self'; base-uri 'self'; form-action 'self'")
 if request.is_secure:r.headers.setdefault('Strict-Transport-Security','max-age=31536000; includeSubDomains')
 return r
@app.cli.command('init-db')
def init_db():
 db.create_all()
 for k,v in [('ads_enabled','0'),('owner_name',''),('contact_email','')]:
  if not db.session.get(Setting,k):db.session.add(Setting(key=k,value=v))
 db.session.commit(); print('Database initialized; existing data preserved.')
@app.cli.command('create-admin')
def create_admin():
 import getpass
 u=(os.getenv('ADMIN_USERNAME') or input('Admin username: ')).strip(); p=os.getenv('ADMIN_PASSWORD') or getpass.getpass('Admin password (12+ characters): ')
 if len(p)<12: raise SystemExit('Password must contain at least 12 characters.')
 if Admin.query.filter_by(username=u).first():raise SystemExit('Admin already exists.')
 db.session.add(Admin(username=u,password_hash=generate_password_hash(p)));db.session.commit();print('Administrator created.')
@app.cli.command('seed')
def seed():
 samples=[('The Last Train Home','Aarohi','Emotional','Hinglish','Platform par sirf ek chai wala aur main bache the. Maa ka message ab bhi phone par khula tha: “Ghar jaldi aa jaana.” Train aayi, darwaze khule, par main wahi khada raha. Kabhi-kabhi safar ghar tak nahi, khud tak hota hai.\n\nMaine ticket fold ki, chai ka aakhri sip liya aur phone uthaya. “Maa, main aa raha hoon.” Us taraf se bas ek saans aur phir woh hansi, jiske liye poori duniya ka safar chhota pad jaata hai.'),('बारिश की आख़िरी बूंद','अनन्या','Romance','हिंदी','बारिश थम चुकी थी, लेकिन पुराने बरगद से बूंदें अब भी गिर रही थीं। मीरा ने छाता बंद किया तो सामने वही किताबों वाला लड़का खड़ा था।\n\n“आपकी किताब,” उसने कहा। किताब के अंदर एक छोटा-सा कागज़ था—“अगली बारिश में चाय?” मीरा मुस्कुराई। शहर वही था, रास्ता वही, मगर मौसम ने पहली बार कोई कहानी लिखी थी।'),('A Small Kind of Courage','Rohan Mehta','Motivation','English','Every morning, Kabir stood outside the interview room and found a reason to turn back. On the fifth day, he stopped trying to feel fearless. He simply walked in while his hands were still shaking.\n\nHe did not get the job. But he learned the difference between failure and retreat. A week later, he tried again. Courage, he discovered, was sometimes just one more knock on a closed door.'),('Room Number 13','Dev','Horror','Hinglish','Hotel ke corridor mein room 13 nahi tha. Receptionist ne kaha, “12 ke baad 14 hai.” Phir bhi raat ke 2:13 par phone par message aaya: ROOM 13 — PLEASE OPEN.\n\nDarwaze ke neeche se roshni aa rahi thi. Peephole se dekha—andar main hi khada tha, bas uski aankhon mein neend nahi thi. Phone phir vibrate hua: “Tum bahar kyun khade ho?”'),('The Missing Bookmark','Nisha','Mystery','English','When the old librarian vanished, every book on his desk was returned except one. It was a mystery novel with a blue bookmark pressed between two blank pages.\n\nDetective Rao noticed the bookmark’s stitching was uneven. Inside it, someone had hidden a tiny brass key. It opened a drawer beneath the catalogue—and a letter addressed to the person who would notice what was missing.')]
 for i,(t,a,g,l,c) in enumerate(samples):
  s=slugify(t)
  if not Story.query.filter_by(slug=s).first():db.session.add(Story(title=t,slug=s,author=a,genre=g,language=l,content=c,status='published',featured=i==0))
 db.session.commit();print('Seed complete; existing slugs skipped.')
@app.route('/')
def home():return render_template('home.html',latest=Story.query.filter_by(status='published').order_by(Story.created_at.desc()).limit(6).all(),popular=Story.query.filter_by(status='published').order_by(Story.featured.desc(),Story.created_at.desc()).limit(4).all())
@app.route('/stories')
def stories():
 q=request.args.get('q','').strip()[:100];g=request.args.get('genre','');page=max(1,request.args.get('page',1,type=int));x=Story.query.filter_by(status='published')
 if q:x=x.filter(or_(Story.title.ilike(f'%{q}%'),Story.author.ilike(f'%{q}%'),Story.content.ilike(f'%{q}%'),Story.tags.ilike(f'%{q}%')))
 if g in GENRES:x=x.filter_by(genre=g)
 return render_template('stories.html',pagination=x.order_by(Story.created_at.desc()).paginate(page=page,per_page=6,error_out=False),q=q,selected_genre=g)
@app.route('/story/<slug>')
def story_detail(slug):
 s=Story.query.filter_by(slug=slug,status='published').first_or_404();lang=request.args.get('lang',s.language);t=next((x for x in s.translations if x.language==lang),None)
 if lang!=s.language and not t:flash(f'No {lang} translation is available yet; showing the original.','info');lang=s.language
 return render_template('story.html',story=s,translation=t if lang!=s.language else None,display_language=lang)
@app.route('/submit-story',methods=['GET','POST'])
def submit_story():
 if request.method=='POST':
  if time.time()-session.get('last_submission',0)<8:flash('Please wait a few seconds before submitting again.','error');return redirect(url_for('submit_story'))
  d={k:request.form.get(k,'').strip() for k in ['title','pen_name','genre','language','content','email']};errors=[]
  if not d['title'] or len(d['title'])>180:errors.append('Title is required (maximum 180 characters).')
  if not d['pen_name'] or len(d['pen_name'])>100:errors.append('Pen name is required (maximum 100 characters).')
  if d['genre'] not in GENRES:errors.append('Choose a valid genre.')
  if d['language'] not in LANGUAGES:errors.append('Choose a valid language.')
  if not 50<=len(d['content'])<=30000:errors.append('Story content must be 50–30,000 characters.')
  if d['email'] and (len(d['email'])>254 or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$',d['email'])):errors.append('Enter a valid email or leave it blank.')
  if request.form.get('rights_confirmed')!='yes':errors.append('Confirm that you own the work or have permission.')
  if errors:
   for e in errors:flash(e,'error')
   return render_template('submit.html',form=request.form),400
  db.session.add(Submission(title=d['title'],pen_name=d['pen_name'],genre=d['genre'],language=d['language'],content=d['content'],email=d['email'],rights_confirmed=True));db.session.commit();session['last_submission']=time.time();return render_template('submit_success.html')
 return render_template('submit.html',form={})
def simple_page(title,description,body,**kw):return render_template('page.html',page_title=title,page_description=description,body=body,**kw)
@app.route('/about')
def about():return simple_page('About Kahani Adda','A welcoming adda for stories in Hindi, Hinglish and English.','Kahani Adda is a home for stories in Hindi, Hinglish and English. We celebrate imagination, everyday courage, and the voices that make stories worth sharing. Reader submissions are reviewed before publication.')
@app.route('/contact')
def contact():
 o=db.session.get(Setting,'owner_name');e=db.session.get(Setting,'contact_email');return simple_page('Contact','Contact the Kahani Adda team.','For editorial questions, corrections, or copyright concerns, use the configured contact email shown below. If no email is configured, contact details have not yet been published.',contact_owner=o.value if o else '',contact_email=e.value if e else '')
@app.route('/privacy')
def privacy():return simple_page('Privacy Policy','How Kahani Adda handles information.','We collect information you choose to provide in a story submission, including pen name, story text, and optional contact email. Submissions remain unpublished until approved. Hosting providers may process standard server logs. Adapt this starter policy to your actual operations, analytics, advertising and jurisdiction before launch.')
@app.route('/terms')
def terms():return simple_page('Terms of Use','Terms for using Kahani Adda.','Submit only work you own or have permission to share. Do not submit unlawful, abusive, defamatory, infringing, or harmful content. Submission does not guarantee publication. Editors may revise, reject or remove content. Replace this starter text with terms reviewed for your actual service.')
@app.route('/copyright')
def copyright_policy():return simple_page('Copyright & Takedown','Copyright and takedown policy.','If you believe material published here infringes your rights, contact the site owner using configured contact details and include the URL, identification of the work, your contact details and a good-faith explanation. We review credible notices and may temporarily remove disputed content. Publish a verified contact channel before accepting submissions.')
@app.route('/sitemap.xml')
def sitemap():
 from xml.sax.saxutils import escape
 urls=[url_for(x,_external=True) for x in ['home','stories','submit_story','about','contact','privacy','terms','copyright_policy']]+[url_for('story_detail',slug=s.slug,_external=True) for s in Story.query.filter_by(status='published').all()]
 return app.response_class('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(u)+'</loc></url>' for u in urls)+'</urlset>',mimetype='application/xml')
@app.route('/robots.txt')
def robots():return app.response_class(f'User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: {os.getenv("SITE_URL",request.url_root.rstrip("/"))}/sitemap.xml\n',mimetype='text/plain')
@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
 if request.method=='POST':
  u=Admin.query.filter_by(username=request.form.get('username','').strip()).first();attempts=session.get('attempts',0)
  if attempts>=5 and time.time()-session.get('attempt_time',0)<300:flash('Too many attempts. Wait five minutes.','error')
  elif u and check_password_hash(u.password_hash,request.form.get('password','')):session.clear();session['admin_id']=u.id;session['admin_name']=u.username;return redirect(url_for('admin_dashboard'))
  else:session['attempts']=attempts+1;session['attempt_time']=time.time();flash('Invalid username or password.','error')
 return render_template('admin/login.html')
@app.route('/admin/logout',methods=['POST'])
@admin_required
def admin_logout():session.clear();flash('Signed out.','success');return redirect(url_for('home'))
@app.route('/admin')
@admin_required
def admin_dashboard():return render_template('admin/dashboard.html',published=Story.query.filter_by(status='published').count(),drafts=Story.query.filter_by(status='draft').count(),pending=Submission.query.filter_by(status='pending').count(),stories=Story.query.order_by(Story.created_at.desc()).limit(20).all())
def story_data(s=None):return {k:request.form.get(k,getattr(s,k,'') if s else default) for k,default in [('title',''),('slug',''),('author',''),('genre','Life Stories'),('tags',''),('language','Hinglish'),('content',''),('status','draft')]} | {'featured':request.form.get('featured')=='yes' if request.method=='POST' else bool(s and s.featured)}
def validate_story(d):
 e=[]
 if not d['title'] or len(d['title'])>180:e.append('Title is required (max 180 characters).')
 if not d['author'] or len(d['author'])>100:e.append('Author is required (max 100 characters).')
 if d['genre'] not in GENRES:e.append('Choose a valid genre.')
 if d['language'] not in LANGUAGES:e.append('Choose a valid language.')
 if d['status'] not in ['draft','published']:e.append('Invalid status.')
 if not d['content'] or len(d['content'])>50000:e.append('Content is required (max 50,000 characters).')
 return e
def save_story(s,d):
 slug=slugify(d['slug'] or d['title']);other=Story.query.filter(Story.slug==slug,Story.id!=getattr(s,'id',None)).first()
 if other:return 'That URL slug is already in use.'
 for k in ['title','author','genre','language','content','status','featured']:setattr(s,k,d[k])
 s.slug=slug;s.tags=d['tags'][:300];return None
@app.route('/admin/stories/new',methods=['GET','POST'])
@admin_required
def admin_story_new():
 d=story_data()
 if request.method=='POST':
  errs=validate_story(d)
  if not errs:
   s=Story();err=save_story(s,d)
   if err:errs.append(err)
   else:db.session.add(s);db.session.commit();flash('Story saved.','success');return redirect(url_for('admin_dashboard'))
  for e in errs:flash(e,'error')
 return render_template('admin/story_form.html',data=d,heading='Create story')
@app.route('/admin/stories/<int:sid>/edit',methods=['GET','POST'])
@admin_required
def admin_story_edit(sid):
 s=Story.query.get_or_404(sid);d=story_data(s)
 if request.method=='POST':
  errs=validate_story(d)
  if not errs:
   err=save_story(s,d)
   if err:errs.append(err)
   else:db.session.commit();flash('Story updated.','success');return redirect(url_for('admin_dashboard'))
  for e in errs:flash(e,'error')
 return render_template('admin/story_form.html',data=d,heading='Edit story',story=s)
@app.route('/admin/stories/<int:sid>/delete',methods=['POST'])
@admin_required
def admin_story_delete(sid):s=Story.query.get_or_404(sid);db.session.delete(s);db.session.commit();flash('Story deleted.','success');return redirect(url_for('admin_dashboard'))
@app.route('/admin/submissions')
@admin_required
def admin_submissions():return render_template('admin/submissions.html',submissions=Submission.query.order_by(Submission.created_at.desc()).all())
@app.route('/admin/submissions/<int:sid>',methods=['GET','POST'])
@admin_required
def admin_review(sid):
 s=Submission.query.get_or_404(sid)
 if request.method=='POST':
  action=request.form.get('action')
  if action=='publish':
   d={k:request.form.get(k,'').strip() for k in ['title','author','genre','language','content']};d.update(status='published',tags='',slug='');errs=validate_story(d)
   if errs:
    for e in errs:flash(e,'error')
   else:
    slug=slugify(d['title']);
    if Story.query.filter_by(slug=slug).first():slug+=f'-{int(time.time())}'
    db.session.add(Story(title=d['title'],slug=slug,author=d['author'],genre=d['genre'],language=d['language'],content=d['content'],status='published'));s.status='approved';db.session.commit();flash('Submission published.','success');return redirect(url_for('admin_submissions'))
  elif action in ['reject','changes']:s.status='rejected' if action=='reject' else 'changes_requested';db.session.commit();flash('Submission status updated.','success');return redirect(url_for('admin_submissions'))
 return render_template('admin/review.html',sub=s)
@app.route('/admin/stories/<int:sid>/translations',methods=['GET','POST'])
@admin_required
def admin_translations(sid):
 s=Story.query.get_or_404(sid)
 if request.method=='POST':
  lang=request.form.get('language','');title=request.form.get('title','').strip();content=request.form.get('content','').strip()
  if lang not in LANGUAGES or lang==s.language or not title or len(title)>180 or not content or len(content)>50000:flash('Choose another supported language and provide a title and content.','error')
  else:
   t=Translation.query.filter_by(story_id=s.id,language=lang).first()
   if not t:t=Translation(story_id=s.id,language=lang,title=title,content=content);db.session.add(t)
   else:t.title=title;t.content=content
   db.session.commit();flash('Translation saved.','success');return redirect(url_for('admin_translations',sid=s.id))
 return render_template('admin/translations.html',story=s)
@app.route('/admin/settings',methods=['GET','POST'])
@admin_required
def admin_settings():
 keys=['ads_enabled','owner_name','contact_email']
 if request.method=='POST':
  for k in keys:
   v=request.form.get(k,'').strip()[:500];x=db.session.get(Setting,k)
   if not x:x=Setting(key=k);db.session.add(x)
   x.value=('1' if v=='1' else '0') if k=='ads_enabled' else v
  db.session.commit();flash('Settings saved. This does not activate live ads.','success');return redirect(url_for('admin_settings'))
 return render_template('admin/settings.html',settings={x.key:x.value for x in Setting.query.filter(Setting.key.in_(keys)).all()})
@app.errorhandler(404)
def missing(e):return render_template('errors/404.html'),404
@app.errorhandler(500)
def error(e):db.session.rollback();return render_template('errors/500.html'),500
if __name__=='__main__':app.run(host='127.0.0.1',port=int(os.getenv('PORT',5000)),debug=os.getenv('FLASK_DEBUG')=='1')
