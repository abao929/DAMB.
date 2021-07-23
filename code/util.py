import csv

def drop_csv_col(source_file, result_file, idx):
    with open(source_file, 'r') as source:
        reader = csv.reader( source )
        with open(result_file, 'w') as result:
            writer = csv.writer(result)
            for row in reader:
                del row[idx]
                writer.writerow(row)


def main():
    drop_csv_col('../data/data-train-plus-color.csv', '../data/data-train-final.csv', 9)
    drop_csv_col('../data/data-test-plus-color.csv', '../data/data-test-final.csv', 9)

if __name__ == "__main__":
    main()