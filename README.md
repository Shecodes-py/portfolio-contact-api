Portfolio Contact API 🚀
A robust Django REST Framework (DRF) service that powers the contact form on my portfolio. It captures potential leads, persists them in a PostgreSQL database, and triggers real-time email notifications via SendGrid.

🛠️ Tech Stack
Backend: Python 3.12+, Django 6.0

API: Django REST Framework (DRF)

Email Service: SendGrid SDK

Database: PostgreSQL (deployed via Render)

Infrastructure: Render (Web Service + Managed DB)

🏗️ Architecture
The API follows a "Fail-Safe" logic:

Validation: Incoming data is validated via ContactEmailSerializer.

Persistence: Data is saved to the database before attempting to send an email. This ensures that even if the email provider is down, the message is never lost.

Notification: The perform_create hook triggers the SendGrid SDK to dispatch a notification to my personal inbox.

🚀 API Endpoints
Send a Message
POST /api/contact/

Request Body:

JSON

{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "I'd love to discuss a backend collaboration!"
}
Responses:

201 Created: Message saved and email queued.

400 Bad Request: Validation failed (e.g., invalid email format).

500 Internal Server Error: Unexpected server-side failure.

⚙️ Installation & Local Setup
Clone the repository:

Bash

git clone https://github.com/your-username/portfolio-backend.git
cd portfolio-backend
Set up Virtual Environment:

Bash

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Environment Variables (.env): Create a .env file in the root directory:

Code snippet

DEBUG=True
SECRET_KEY=your_secret_key
DB_URL=your_postgres_url
SENDGRID_API_KEY=SG.your_key
VERIFIED_SENDER_EMAIL=your@email.com
Run Migrations & Start Server:

Bash

python manage.py migrate
python manage.py runserver
🔒 Security Features
CORS Configuration: Strictly limited to authorized frontend origins.

Environment Safety: All sensitive credentials (API keys, DB URLs) are managed via environment variables and excluded from version control.

Data Sanitization: DRF serializers protect against common injection vulnerabilities.

👨‍💻 Author
Peace Udotong

LinkedIn: in/peaceudotong

Location: Lagos, Nigeria 🇳🇬