# Backend (Django)
## How to run/install


### 1. create python enviroment in backend directory.
```python
python -m venv .venv 
```

".venv" is environment directory name.


### 2. activate environment in terminal.
```python
.\.venv\Scripts\activate
```
in command prompt  
"(.venv) PS D:\directory>" should show up like this.


### 3. get into backend directory.
```python
cd backend
```


### 4. install the requirements.
```python
pip install -r .\requirements.txt
```

if some still missing after try running server, use this.

```python
python -m pip install ...
```


### 5. Configure Environment Variables (Optional)
Create a `.env` file in the backend directory or set environment variables:

**Option 1: Using .env file (requires python-dotenv)**
```bash
pip install python-dotenv
```
Then create `.env` file:
```bash
# For Suno API integration
SUNO_API_TOKEN=your_actual_suno_api_token_here

# For strategy selection (default: 'mock')
GENERATOR_STRATEGY=suno  # or 'mock'
```

**Option 2: Set environment variables directly**
```bash
# Windows PowerShell
$env:SUNO_API_TOKEN="your_token_here"
$env:GENERATOR_STRATEGY="suno"

# Windows Command Prompt
set SUNO_API_TOKEN=your_token_here
set GENERATOR_STRATEGY=suno
```

**Note:** The frontend can override the default strategy by specifying `strategy` parameter in API requests.

### 6. migrate the sqlite3.
make tables for sqlite3.
```bash
python manage.py migrate 
```


### 7. run the testing server.
make sure you're in the same directory as manage.py, in this case is backend.
```bash
python manage.py runserver 
```


## Demo Screenshots

Inserting Data into Tables
![Adding Tables](Demo/Adding_Tables.png)

User Tables
![Users](Demo/Users.png)

Library Tables
![Library User1](Demo/Library_User1.png)

Song Tables
![Songs](Demo/Songs.png)


$${\color{white}End}$$