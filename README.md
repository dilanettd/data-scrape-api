# LinkedIn Activity Scraper API

This project is a Flask API that retrieves recent activity (latest 20-30 posts) from a LinkedIn user by their LinkedIn ID and fetches the engagement data (likers) of each post, including their IDs, names, and titles.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**
   \```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   \```

2. **Install dependencies**
   Make sure you have Python and pip installed.
   \```bash
   pip install -r requirements.txt
   \```

3. **Set up environment variables**
   Create a .env file at the root of the project with the following details:
   \```plaintext

   # LinkedIn credentials

   LINKEDIN_EMAIL=your_linkedin_email@example.com
   LINKEDIN_PASSWORD=your_linkedin_password

   - BROWSER=your_browser(edge, chrome, firefox, default=edge)
     \```

4. **Run the application**
   \```bash
   flask run
   \```

## Usage

Once the application is running, you can access the API to retrieve LinkedIn activity data. The API documentation is available at: http://127.0.0.1:5000/docs#/

Endpoint: /scrape/<linkedin_user_id>
HTTP Method: GET
URL Parameters: <linkedin_user_id> is the LinkedIn ID of the target user.
Example usage with cURL:
\```bash
curl -X GET http://127.0.0.1:5000/api/linkedin/activity/<linkedin_user_id>
\```

## Response

The API returns a JSON object containing LinkedIn activity data:
\```json
[
{
"post_id": "urn:li:activity:123456789",
"likers": [
{
"id": "12345678",
"name": "John Doe",
"title": "Software Engineer"
},
{
"id": "87654321",
"name": "Jane Smith",
"title": "Product Manager"
}
]
},
{
"post_id": "urn:li:activity:987654321",
"likers": [
{
"id": "56789012",
"name": "Michael Brown",
"title": "Data Scientist"
}
]
}
]
\```

## Important Notes

**Security**: Make sure not to share your LinkedIn credentials in a production environment or outside of a secure .env file.

## Author

DilaneTTD

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
