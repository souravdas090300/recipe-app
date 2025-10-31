# Recipe App - Django Full-Stack Web Application

A comprehensive recipe management and discovery platform built with Django, featuring user authentication, advanced search, data visualization, and a modern responsive UI.

## 🚀 Live Demo
[View Live Application](https://your-app-name.herokuapp.com) *(Update with your Heroku URL)*

## 📋 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **User Authentication**: Secure login/logout system with protected views
- **Recipe Management**: Create, read, update, and delete recipes (CRUD operations)
- **Advanced Search**: 
  - Partial/wildcard recipe name matching (case-insensitive)
  - Filter by difficulty level (Easy, Medium, Intermediate, Hard)
  - Show all recipes option
- **Data Visualization**: Interactive charts using matplotlib
  - Bar Chart: Cooking time by recipe
  - Pie Chart: Recipe distribution by difficulty
  - Line Chart: Cooking time trends
- **Responsive Design**: Mobile-friendly UI with modern styling
- **Admin Panel**: Custom Django admin interface with enhanced features

### Additional Features
- Computed difficulty ratings based on cooking time and ingredients
- Recipe detail pages with complete information
- Navigation menu with category dropdowns
- About Me page with developer information
- Search results displayed as formatted tables
- Professional styling with CSS gradients and animations

## 🛠️ Technologies Used

- **Backend**: Python 3.14, Django 5.2.7
- **Database**: SQLite (development), PostgreSQL (production via Heroku)
- **Data Analysis**: pandas 2.3.3, matplotlib 3.10.7
- **Deployment**: Heroku, Gunicorn 23.0.0, WhiteNoise 6.11.0
- **Frontend**: HTML5, CSS3, Django Templates
- **Testing**: Django TestCase (39 tests with 100% pass rate)
- **Version Control**: Git, GitHub

## 📦 Installation

### Prerequisites
- Python 3.14 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/souravdas090300/recipe-app.git
cd recipe-app/recipe_project
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv web-dev
web-dev\Scripts\activate

# macOS/Linux
python3 -m venv web-dev
source web-dev/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Homepage: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## 🎯 Usage

### For Users
1. **Homepage**: Browse featured recipes and navigate through categories
2. **Login**: Click "Log In" button and enter credentials
3. **Search Recipes**: 
   - Navigate to the Recipes page
   - Enter search criteria (name, difficulty)
   - Select chart type (Bar, Pie, Line)
   - Click "Search" to view results and visualization
4. **View Recipe Details**: Click on any recipe name to see full details
5. **Logout**: Click the "Logout" button when finished

### For Administrators
1. Access the admin panel at `/admin/`
2. Add/edit/delete recipes
3. Manage users and permissions
4. View all database records

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run with verbosity
python manage.py test -v 2

# Run specific test file
python manage.py test recipe.tests.test_forms
```

**Test Coverage**: 39 tests covering:
- Models (8 tests)
- Views (15 tests)
- Forms (8 tests)
- Search functionality (13 tests)
- Authentication (5 tests)

## 🌐 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
cd recipe_project
heroku create your-app-name
```

4. **Set environment variables**
```bash
heroku config:set DJANGO_SECRET_KEY="your-secret-key-here"
heroku config:set DJANGO_DEBUG="false"
heroku config:set DJANGO_ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

5. **Deploy**
```bash
git push heroku main
```

6. **Run migrations**
```bash
heroku run python manage.py migrate
```

7. **Create superuser**
```bash
heroku run python manage.py createsuperuser
```

8. **Open application**
```bash
heroku open
```

### Required Files for Deployment
- `Procfile`: Defines process type (web: gunicorn)
- `runtime.txt`: Specifies Python version
- `requirements.txt`: Lists all dependencies
- `.gitignore`: Excludes sensitive files

## 📁 Project Structure

```
recipe-app/
├── recipe_project/                 # Django project root
│   ├── recipe/                     # Main recipe app
│   │   ├── migrations/             # Database migrations
│   │   ├── templates/recipe/       # HTML templates
│   │   │   ├── recipes_home.html   # Homepage with navigation
│   │   │   ├── recipes_list.html   # Search and list view
│   │   │   ├── recipe_detail.html  # Individual recipe page
│   │   │   └── about.html          # About page
│   │   ├── tests/                  # Test files
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   ├── test_forms.py
│   │   │   └── test_recipes_views.py
│   │   ├── admin.py                # Admin configuration
│   │   ├── forms.py                # RecipeSearchForm
│   │   ├── models.py               # Recipe model
│   │   ├── urls.py                 # App URL patterns
│   │   ├── utils.py                # Chart generation utilities
│   │   └── views.py                # View functions
│   ├── recipe_project/             # Project settings
│   │   ├── settings.py             # Production settings
│   │   ├── settings_local.py       # Development settings
│   │   ├── urls.py                 # Project URL configuration
│   │   └── wsgi.py                 # WSGI configuration
│   ├── templates/                  # Project-level templates
│   │   ├── auth/                   # Authentication templates
│   │   │   ├── login.html
│   │   │   └── success.html
│   │   ├── admin/                  # Admin customization
│   │   │   └── base_site.html
│   │   ├── media/                  # User-uploaded files
│   │   └── static/                 # Static files
│   ├── manage.py                   # Django management script
│   ├── Procfile                    # Heroku process file
│   ├── runtime.txt                 # Python version
│   ├── requirements.txt            # Dependencies
│   └── db.sqlite3                  # SQLite database (dev only)
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 📸 Screenshots

*(Add screenshots of your application here)*

### Homepage
![Homepage](screenshots/homepage.png)

### Recipe Search
![Search Results](screenshots/search-results.png)

### Data Visualization
![Charts](screenshots/charts.png)

### Recipe Detail
![Recipe Detail](screenshots/recipe-detail.png)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project was created as part of CareerFoundry's Full-Stack Web Development Program (Achievement 2).

## 👤 Author

**Sourav Das**
- GitHub: [@souravdas090300](https://github.com/souravdas090300)
- Repository: [recipe-app](https://github.com/souravdas090300/recipe-app)

## 🙏 Acknowledgments

- CareerFoundry for the project structure and guidance
- Django documentation and community
- All open-source contributors

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainer.

---

**Note**: This application is a learning project and may not be suitable for production use without further security enhancements and optimizations.
