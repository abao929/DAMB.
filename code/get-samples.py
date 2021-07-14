import os
from shutil import copyfile
import csv

os.makedirs(os.path.join('sample-data', 'images'), exist_ok=True)

with open(os.path.join('data', 'data-train-plus-color.csv'), newline='') as f:
    reader = csv.reader(f, delimiter=',')
    sample = [next(reader) for x in range(101)]
    for row in sample[1:]:

        cover_path = row[2]
        file_path_parts = cover_path.split(os.path.sep)
        train_path = os.path.join(file_path_parts[0], 'train', file_path_parts[1], file_path_parts[2])
        test_path = os.path.join(file_path_parts[0], 'test', file_path_parts[1], file_path_parts[2])
        if os.path.isfile(train_path):
            cover_path = train_path
        elif os.path.isfile(test_path):
            cover_path = test_path

        new_path = os.path.join('sample-data', 'images', cover_path.split('/')[3])
        copyfile(cover_path, new_path)
    
    with open(os.path.join('sample-data', 'data-train.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sample)

with open(os.path.join('data', 'data-test-plus-color.csv'), newline='') as f:
    reader = csv.reader(f, delimiter=',')
    sample = [next(reader) for x in range(11)]
    for row in sample[1:]:

        cover_path = row[2]
        file_path_parts = cover_path.split(os.path.sep)
        train_path = os.path.join(file_path_parts[0], 'train', file_path_parts[1], file_path_parts[2])
        test_path = os.path.join(file_path_parts[0], 'test', file_path_parts[1], file_path_parts[2])
        if os.path.isfile(train_path):
            cover_path = train_path
        elif os.path.isfile(test_path):
            cover_path = test_path

        new_path = os.path.join('sample-data', 'images', cover_path.split('/')[3])
        copyfile(cover_path, new_path)
    
    with open(os.path.join('sample-data', 'data-test.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sample)