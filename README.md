# MBTL Matchup Note Taking App

A web app for managing character matchup notes for Melty Blood: Type Lumina. Track general and matchup-specific notes for each character, filter moves, and quickly reference information from a spreadsheet-based workflow.

## Features
- CRUD Notes: Add, edit, and delete general and matchup-specific notes.
- Dynamic Character Data: Loads moves and info from JSON files exported from spreadsheets.
- Character Filtering: Filter moves by name or notes presence.
- Images: Displays character portraits dynamically.
- Spreadsheet → JSON Workflow: Easily manage and update move data in Excel or Google Sheets.
- Responsive UI: Clean interface using Flask templates and CSS.

## Live Demo
[Deployed on Heroku](https://mbtlnotetakingapp-7d6abf9393e8.herokuapp.com/)

## Getting Started (Local)
1. Clone the repository:
```bash
git clone https://github.com/Patdabaker/MBTLFrameData.git
cd mbtl-notes-app
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the Flask app:
```bash
flask run
```
5. Open `http://127.0.0.1:5000` in your browser.

## File Structure
```bash
/app.py                  # Flask application
/templates               # HTML templates
/static                  # CSS and character images
/data/characters         # Character JSON files
/convert.py              # Spreadsheet → JSON converter
requirements.txt         # Python dependencies
moves.xlsx               # Move data spreadsheet
```

## Adding / Updating Characters & Images
1. Update Spreadsheet: Add or modify moves, notes, or character info in your Excel/Google Sheets file.
2. Convert to JSON: Run convert.py to generate updated JSON files in /data/characters.
3. Add Character Images: Place images in static/images/characters/ using the convention:
- File name = first name, all lowercase (e.g., arcueid.png for “Arcueid Brunestud”).
4. Refresh App: Visit the page to see the updated data and images.

## License
MIT License
