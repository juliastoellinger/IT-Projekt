import pandas as pd
# Since the headers are missing in the csv file, explicitly passing the field names in the program
csv_file = pd.DataFrame(pd.read_csv("aerodata_flughafen_amsterdam.csv", sep = ";", index_col = False))
csv_file.to_json("data.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)