from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import pandas as pd
import pymongo
from ArcGIS_API.coordinates_calc import get_coordinates_info, combinations_points

app = Flask(__name__)
app.config["CSVsUPLOADS"] = r"C:\python_projects\GpsApi\CSVs"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Database"
mongo = PyMongo(app)
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["Database"]
mycol = mydb["SampleCollection"]

POINTS = 'points'
LINKS = 'links'
ID = "result_id"

data = []


@app.route("/")
def home_page():
    return render_template("upload_file.html")


@app.route("/api/getAddresses", methods=["GET", "POST"])
def upload_file():
    ''' POST or GET request
     GET: HTML page for uploading a csv file
     POST: Upload a new csv file using Curl cmd or by the html page
     '''
    CONST__LAT_STR = "Latitude"
    CONST_LONG_STR = "Longitude"

    if request.method == "POST":
        if request.files:
            print(request)
            tmp_data = {POINTS: [],
                        LINKS: [],
                        ID: ""}
            my_file = request.files["file"]
            df_data = pd.read_csv(my_file, index_col=0)  # set the point column to be the index col
            for index, row in df_data.iterrows():
                point_info = {'name': index}
                point_info.update(get_coordinates_info(lon=row[CONST_LONG_STR], lat=row[CONST__LAT_STR]))
                tmp_data[POINTS].append(point_info)
            tmp_data[LINKS].append(list(combinations_points(df_data, 2)))
            try:
                tmp_data[ID] = max([i[ID] for i in data]) + 1
            except ValueError:
                tmp_data[ID] = 1

            data.append(tmp_data)
            mycol.insert_one(tmp_data)
            tmp_data['_id'] = tmp_data['result_id']
            return jsonify(tmp_data), 201
    return render_template("upload_file.html")


@app.route('/api/getResult', methods=['GET'])
def get_all():
    all_data = []
    for data in mycol.find():
        data['_id'] = str(data['_id'])
        all_data.append(data)
    return jsonify(all_data), 200


# Route to filter by id
@app.route('/api/getResult/<id>', methods=['GET'])
def devs_per_id(id):
    for data in mycol.find():
        if data['result_id'] == id or str(data['_id']) == id:
            data['_id'] = str(data['_id'])
            return jsonify(data), 200
    return jsonify({'error': 'not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
