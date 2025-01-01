from flask import Flask, render_template, request, send_file, session
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use sessions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    date = request.form['date']
    time = request.form['time']
    name = request.form['name']

    clean_bin = request.form.getlist('clean_bin[]')
    clean_gross_weight = request.form.getlist('clean_gross_weight[]')
    clean_tare_weight = request.form.getlist('clean_tare_weight[]')

    soil_bin = request.form.getlist('soil_bin[]')
    soil_gross_weight = request.form.getlist('soil_gross_weight[]')
    soil_tare_weight = request.form.getlist('soil_tare_weight[]')

    # Create DataFrames
    clean_df = pd.DataFrame({
        'Bin #': clean_bin,
        'Gross Weight': clean_gross_weight,
        'Tare Weight': clean_tare_weight
    })

    soil_df = pd.DataFrame({
        'Bin #': soil_bin,
        'Gross Weight': soil_gross_weight,
        'Tare Weight': soil_tare_weight
    })

    # Store the data in the session for later retrieval
    session['clean_df'] = clean_df.to_dict()
    session['soil_df'] = soil_df.to_dict()

    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    # Retrieve the data from the session
    clean_df = pd.DataFrame(session.get('clean_df'))
    soil_df = pd.DataFrame(session.get('soil_df'))

    # Create a bytes buffer for the Excel writer
    buffer = io.BytesIO()

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        clean_df.to_excel(writer, sheet_name='Clean Scale Weights', index=False)
        soil_df.to_excel(writer, sheet_name='Soil Scale Weights', index=False)

    # Set the buffer position to the beginning
    buffer.seek(0)

    # Send the excel file
    return send_file(buffer, as_attachment=True, download_name='data.xlsx')

if __name__ == '__main__':
    app.run(debug=True)
