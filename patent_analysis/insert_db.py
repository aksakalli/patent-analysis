import pandas as pd
from pymongo import MongoClient, ASCENDING, DESCENDING
import os
from helper import db, log


def insert_file(file_path, strip_fields=[], decode_field=[]):
    log.info("inserting " + file_path)
    # insert everything as string! We don't need any numberic queries!
    df = pd.read_csv(file_path, sep='\t',iterator=True, chunksize=5000, dtype='str')
    collection = os.path.basename(file_path).split('.')[0]
    collection = db.get_collection(collection)
    for f in df:
        for field in strip_fields:
            try:
                f[field] = pd.core.strings.str_strip(f[field])
            except:
                # I'm a scatman :)
                pass

        for field in decode_field:
            try:
                f[field] = f[field].str.decode('unicode-escape').str.encode('utf8')
            except:
                # I'm a scatman :)
                pass

        collection.insert_many(f.to_dict('records'))


def define_indexes():
    log.info('defining indexes')
    db.wipo.create_index('field_id')
    db.wipo.create_index('patent_id')

    db.uspatentcitation.create_index('patent_id')
    db.uspatentcitation.create_index('citation_id')

    db.patent.create_index('id')
    db.patent.create_index('date')

    # db.series.create_index('node')
    # db.series.create_index('date')
    # db.series.create_index('measure')
    log.info('indexes defined!')


def main():
    define_indexes()
    insert_file('data/wipo_field.tsv', strip_fields=['id'])
    insert_file('data/wipo.tsv', strip_fields=['patent_id', 'field_id'])
    insert_file('data/patent.tsv', strip_fields=['id'])
    insert_file('data/uspatentcitation.tsv', strip_fields=['citation_id', 'patent_id'])

    # insert_file('data/assignee.tsv', decode_field=['name_first', 'name_last', 'organization'])
    # insert_file('data/patent_assignee.tsv')
    # insert_file('data/cpc_current.tsv')
    # insert_file('data/cpc_group.tsv')
    # insert_file('data/cpc_subgroup.tsv')
    # insert_file('data/cpc_subsection.tsv')



if __name__ == "__main__":
    main()
