import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
CHART_FOLDER = 'static/charts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

# Redirect root route to the login page
@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html')

# Sample hardcoded credentials (use actual validation in production)
valid_username = "admin"
valid_password = "password123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Add your authentication logic here
        if username == valid_username and password == valid_password:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    # Your search logic here (e.g., search a database or a list of items)
    # For demonstration purposes, we’ll just return the query.
    
    # You can display the query results or handle it in any way you need.
    return render_template('search_results.html', query=query)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Read the Excel file, skip first row and column
        df = pd.read_excel(filepath, skiprows=1)

        # Exclude the first column from the dataframe if it exists
        if not df.empty:
            df = df.loc[:, df.columns[1:]]

        # Replace NaN values with empty strings
        df.fillna("", inplace=True)

        # Handle plotting for numeric data
        plt.figure(figsize=(8, 5))
        x_values = df.iloc[:, 0].astype(str)  # First column as x-axis
        for column in df.columns[1:]:
            if pd.api.types.is_numeric_dtype(df[column]):
                plt.plot(x_values, df[column], label=column)

        plt.legend()
        plt.title("Excel Data Plot")
        plt.xlabel(df.columns[0])
        plt.ylabel("Values")
        chart_path = os.path.join(CHART_FOLDER, "chart.png")
        plt.savefig(chart_path)
        plt.close()

        # Handle 'At Risk' column as a checklist
        at_risk_checklist = []
        if "At Risk" in df.columns:
            at_risk_checklist = [{"value": val, "checked": bool(val)} for val in df["At Risk"]]

        # Prepare cleaned-up table data
        table_data = df.values.tolist()
        columns = df.columns.tolist()

        return render_template('index.html',
                               table={"columns": columns, "values": table_data},
                               chart_url=f"/{chart_path}",
                               at_risk_checklist=at_risk_checklist)
    
    else:
        return 'Invalid file type. Please upload an Excel file.'

if __name__ == '__main__':
    app.run(debug=True)
