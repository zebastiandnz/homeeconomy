# Home Economy

A simple Flask webapp to track your monthly bills and payments.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialize the database:
   ```bash
   flask --app app.py db_init
   ```
3. Run the development server:
   ```bash
   flask --app app.py run -h 0.0.0.0 -p 5000
   ```

Visit `http://localhost:5000` to see the app.

## Monthly reset
Run the following command at the start of each month to create payment rows for recurring bills:
```bash
flask --app app.py db_init
```
You can automate this with cron or any task scheduler.
