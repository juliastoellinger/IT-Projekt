import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('myOutFile.csv', sep=";")
    df = df.drop_duplicates(subset=['number', 'date'], keep='first')
    print(df)
