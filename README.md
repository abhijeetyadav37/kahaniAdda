# Kahani Adda 📚

**Stories that stay with you.**

Kahani Adda is a story-sharing and reading platform where readers can discover stories across genres and languages, while writers can submit their own stories for review and publication.

The application is built with Flask and PostgreSQL and deployed on Render with Neon PostgreSQL as the production database.

## 🌐 Live Website

- **Website:** https://kahaniadda.onrender.com
- **GitHub Repository:** https://github.com/abhijeetyadav37/kahaniAdda

## ✨ Features

### 📖 Reading Experience
- Explore published stories.
- Browse stories by genre.
- Search stories using available search filters.
- View individual story details.
- Read story descriptions and author information.
- View reading-time estimates.
- Responsive interface for different screen sizes.

### ✍️ Story Submission
- Submit stories through the website.
- Provide story details such as title, author, genre, language, and content.
- Support an administrator review workflow before publication.

### 🔐 Administration
- Administrator login.
- Admin dashboard for managing stories and submissions.
- Review submitted stories.
- Create, edit, and delete stories.
- Manage story translations.
- Configure available application settings.

### 🎨 User Interface
- Clean, reader-focused design.
- Genre-based story cards.
- Light and dark reading-mode controls.
- Language selection interface.
- Navigation links for informational and policy pages.

### 🔎 SEO and Website Policies
- Search-engine-friendly page titles and descriptions.
- Canonical URL metadata.
- Sitemap endpoint.
- `robots.txt` endpoint.
- About, contact, privacy, terms, and copyright-policy pages.

### 💰 Monetization
- Google AdSense integration preparation.
- AdSense verification code added to the shared HTML template.
- Ad serving and account approval remain subject to Google's review and policies.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Templates | Jinja2 |
| Database ORM | SQLAlchemy / Flask-SQLAlchemy |
| Production database | PostgreSQL on Neon |
| Local development database | SQLite, when configured as the application fallback |
| Web server | Gunicorn |
| Hosting | Render |
| Source control | Git and GitHub |
| Monetization | Google AdSense, subject to approval |

## 📁 Project Structure

The application uses Flask templates and static assets. The main files and directories include:

```text
Kahani_Adda/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── stories.html
│   ├── story_detail.html
│   └── partials/
│       └── story_card.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── site.js
├── .gitignore
└── README.md
```

*Note: This is a representative overview of the main application files, not an exhaustive listing of every file in the repository.*

## 🚀 Getting Started

### Prerequisites

Install the following tools:

- Python compatible with the project's dependencies.
- Git.
- A code editor such as Visual Studio Code.

### 1. Clone the repository

```bash
git clone https://github.com/abhijeetyadav37/kahaniAdda.git
cd kahaniAdda
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, you can invoke the environment's Python executable directly.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file only if the application uses `python-dotenv` to load it. Otherwise, configure the variables directly in your terminal.

Example configuration:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///kahani_adda.db
```

Use the actual variable names and database URI format expected by the application's configuration.

For PostgreSQL development, set `DATABASE_URL` to your own PostgreSQL connection string.

**Security:** Never commit `.env` files, passwords, database URLs containing credentials, administrator passwords, or private keys to GitHub.

### 5. Initialize the database

Initialize the database using the Flask CLI:

```bash
python -m flask --app app init-db
```

This command initializes the database using the application's existing initialization logic. It is not intended to replace an existing production database or erase existing records.

### 6. Seed initial data

If the application requires its initial seed data, run:

```bash
python -m flask --app app seed
```

The seed command should be used according to the application's implementation. Existing records should be preserved where the command supports that behavior.

### 7. Create an administrator

Run:

```bash
python -m flask --app app create-admin
```

Follow the prompts to create an administrator account if one does not already exist.

Use a strong, unique password and store it securely.

### 8. Start the development server

```bash
python -m flask --app app run --debug
```

Open:

http://127.0.0.1:5000

Use the local website to test reading, searching, filtering, story submission, and administrative functionality.

## 🗄️ Database Configuration

Kahani Adda uses PostgreSQL on Neon for its deployed production environment.

### Production database

Configure the following environment variables in the Render dashboard:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret used by Flask for application security |

Other variables may be required depending on the application's configuration.

Keep database credentials in Render's environment-variable settings rather than in source code.

### Important database practices

- Never initialize or seed the production database unnecessarily.
- Do not run destructive database operations against production.
- Back up important data before making schema changes.
- Keep local and production database configurations separate.
- Never expose the Neon database password in public logs or repository files.

## ☁️ Deployment on Render

The website is deployed as a Python web service on Render.

### Build command

```bash
pip install -r requirements.txt
```

### Start command

```bash
gunicorn app:app --workers 2 --timeout 120
```

### Deployment process

1. Push the latest application changes to the connected GitHub branch.
2. Open the Render dashboard.
3. Select the `kahaniAdda` web service.
4. Check the latest deployment status and build logs.
5. Wait until the deployment is marked **Live**.
6. Open the public website and test the changed functionality.

Render can automatically deploy new commits when automatic deployments are enabled.

### Production troubleshooting

If a page returns HTTP 500:

1. Open the Render service logs.
2. Find the traceback corresponding to the failed request.
3. Identify the affected route or template.
4. Reproduce the problem locally where possible.
5. Apply and test the fix.
6. Commit and push the fix to GitHub.
7. Verify the new deployment.

For example, shared Jinja templates should not depend on loop variables unless those variables are explicitly available in the template context.

## 💵 Google AdSense

Kahani Adda is being prepared for monetization through Google AdSense.

### Current integration approach

The AdSense verification code belongs inside the HTML `<head>` section of:

```text
templates/base.html
```

Because other pages extend this shared template, the code can be included across the pages that use it.

### Verification and approval

1. Create or configure an AdSense account.
2. Add the correct verification code provided by Google.
3. Commit and deploy the updated template.
4. Confirm that the live page source contains the correct publisher ID.
5. Return to AdSense and complete the verification process.
6. Submit the website for review when prompted.
7. Follow Google's instructions for enabling ads after approval.

### Important considerations

- Adding the verification code does not guarantee approval.
- Verification and website approval are separate steps.
- The website must comply with AdSense content, privacy, and advertising policies.
- Publish useful, original content and provide clear navigation.
- Do not click your own advertisements or encourage others to click them.
- Do not place advertisements in ways that mislead users or cause accidental clicks.
- A free hosting subdomain may have eligibility limitations.

Official resource: https://support.google.com/adsense/

## 🔒 Security

- Keep secrets outside the Git repository.
- Use strong administrator credentials.
- Do not expose database connection strings.
- Use HTTPS for the public website.
- Validate and sanitize user-submitted content.
- Apply appropriate access controls to administrative routes.
- Keep application dependencies updated.
- Follow Google's policies when implementing advertisements.

## 🧪 Testing Checklist

Before deploying changes, verify the following:

- [ ] Homepage loads correctly.
- [ ] Published stories appear on the homepage.
- [ ] Story listing page loads correctly.
- [ ] Search and genre filters work.
- [ ] Individual story pages open correctly.
- [ ] Story submission works.
- [ ] Administrator login works.
- [ ] Story review and publishing work.
- [ ] Story editing and deletion work.
- [ ] Database records persist across deployments.
- [ ] Navigation and policy pages load.
- [ ] AdSense verification code is present on the live site when required.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application locally.
5. Commit your changes with a descriptive message.
6. Open a pull request describing the changes.

## 📄 License

No license has been specified in this README. Check the repository for an existing `LICENSE` file before reusing or redistributing the project's code.

## ❤️ Acknowledgements

Kahani Adda is built to provide a welcoming space for readers and writers to discover, share, and enjoy stories.

**Kahani Adda — Stories that stay with you.**
