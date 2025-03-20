# Online Food

## Run this project on your machine

1. Clone the repository:
   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```

2. Set up a virtual environment:
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment (Windows)
   venv\Scripts\activate
   
   # Activate the virtual environment (macOS/Linux)
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (if needed):
   ```bash
   # Copy the example environment file
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux

   # Edit the environment file with your settings
   ```

5. Set up the database:
   ```bash
   # Run migrations
   python manage.py migrate

   # Create a superuser for the admin panel
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

   The site should now be available at http://127.0.0.1:8000/

7. Accessing the admin panel:
   
   After creating a superuser, you can access the admin panel at:
   http://127.0.0.1:8000/admin/

## Common Issues and Solutions

### Package Installation Problems

If you encounter issues installing packages:

```bash
# Try installing packages one by one
pip install django
pip install psycopg2-binary
pip install python-decouple
pip install [package_name]
```

### Database Connection Issues

If using PostgreSQL or MySQL, ensure:
- The database service is running
- PostgreSQL is properly installed on your system
- Your connection settings in settings.py or .env file are correct
- The specified database exists (you may need to create it first)

```bash
# Example for creating a PostgreSQL database
# Connect to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE django_todo_db;

# Exit
\q
```

### Missing Static Files

If static files aren't loading properly:

```bash
# Collect static files
python manage.py collectstatic
```

### File Upload Issues

If you're having issues with file uploads:

1. Check MEDIA_ROOT and MEDIA_URL settings
2. Ensure the form has `enctype="multipart/form-data"`
3. Verify that Pillow is installed (`pip install Pillow`)
4. Ensure the upload directory exists and is writable
5. Check file size limits in your Django settings:

```python
# Add to settings.py to increase upload limit
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

## Additional Commands

```bash
# Run tests
python manage.py test

# Create a new Django app
python manage.py startapp [app_name]

# Generate requirements.txt file
pip freeze > requirements.txt

# Install dependencies:
pip install -r requirements.txt
```

## Generating Requirements File

To create a requirements.txt file that lists all the Python packages installed in your virtual environment:

```bash
# Make sure your virtual environment is activated, then run:
pip freeze > requirements.txt
```

This file is essential when sharing your project with others or deploying it to a production server. It allows others to install the exact same package versions you used.

Be sure to include the following essential packages in your requirements.txt:
```
Django==4.2.x  # Or your current version
psycopg2-binary==2.9.x  # For PostgreSQL support
python-decouple==3.8  # For environment variables
Pillow==10.x.x  # For image processing
```

## Deactivating the Virtual Environment

When you're done working on the project:

```bash
deactivate
```

---

<div align="center">
<h1> Dabananda Mitra </h1>
</div>

<div align="center">
  <img src="https://res.cloudinary.com/djz3p8sux/image/upload/v1742125099/dabananda_mitra_formal_Small_1x1_o8uxit.png" width="250" height="250" style="border-radius: 50%">
</div>

<h3 align="center">Software Engineer | Problem Solver | Open Source Enthusiast</h3>

---

### 🌐 Connect with Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dabananda) [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dabananda) [![Twitter](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/dabanandamitra) [![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.om/imdmitra/) [![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/8801304080014) [![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordapp.com/users/dabanandamitra)

---

### 💻 Online Judge Profiles

[![LeetCode](https://img.shields.io/badge/-LeetCode-FFA116?style=for-the-badge)](https://leetcode.com/u/dabananda/) [![Codeforces](https://img.shields.io/badge/-Codeforces-1F8ACB?style=for-the-badge)](https://codeforces.com/profile/dabananda) [![CodeChef](https://img.shields.io/badge/-CodeChef-5B4638?style=for-the-badge)](https://www.codechef.com/users/dabananda) [![HackerRank](https://img.shields.io/badge/-HackerRank-00EA64?style=for-the-badge)](https://www.hackerrank.com/profile/dabananda) [![CodingNinjas](https://img.shields.io/badge/-Coding_Ninjas-FFA500?style=for-the-badge)](https://www.naukri.com/code360/profile/48a35475-0af2-4d4e-8f26-2d793b64843a) [![UVa](https://img.shields.io/badge/-UVa-00B388?style=for-the-badge)](https://uhunt.onlinejudge.org/id/1167157) [![Beecrowd](https://img.shields.io/badge/-Beecrowd-009688?style=for-the-badge)](https://judge.beecrowd.com/en/profile/467832) [![Vjudge](https://img.shields.io/badge/-Vjudge-8A2BE2?style=for-the-badge)](https://vjudge.net/user/dabanandamitra)