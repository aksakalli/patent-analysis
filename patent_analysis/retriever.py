import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from helper import db, log

def plot_node_count_per_year():
    pipeline = [
        {'$match': {'date': {'$lt': '2017'}}},
        {'$group': {
            '_id': {'$substr': ['$date', 0, 4]},
            'count': {'$sum': 1}}
        },
        {'$project': {
            '_id': 0,
            'year': '$_id',
            'count': 1}
        },
        {'$sort': {'year': 1}}
    ]

    nodes_per_year = db.patent.aggregate(pipeline)

    x = []
    y = []
    for item in nodes_per_year:
        x.append(int(item['year']))
        y.append(item['count'])

    p = np.poly1d(np.polyfit(x, y, 3))
    xp = np.linspace(x[0], x[-1], len(x))

    plt.plot(x, y, '--o', xp, p(xp), '-')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Number of patents per year')
    plt.grid(True)
    plt.show()


def plot_edge_count_per_year(avg=False):
    operand = '$sum'
    title = 'Number of edges per year'
    if avg:
        operand = '$avg'
        title= 'Number of average edges per year'

    pipeline = [
        {'$match': {'date': {'$lt': '2017'}}},
        {
            '$lookup': {
                'from': 'uspatentcitation',
                'localField': 'id',
                'foreignField': 'patent_id',
                'as': 'cites'
            },
        },
        { '$group': {
            '_id': {'$substr': ['$date', 0, 4]},
            'count': {operand: { '$size': '$cites' }}}
        },
        { '$project': {
            '_id': 0,
            'year': '$_id',
            'count': 1 }
        },
        {
            '$sort': {'year': 1}
        }
    ]

    edges_per_year = db.patent.aggregate(pipeline)
    x = []
    y = []
    for item in edges_per_year:
        x.append(int(item['year']))
        y.append(item['count'])

    p = np.poly1d(np.polyfit(x, y, 2))
    xp = np.linspace(x[0], x[-1], len(x))

    plt.plot(x, y, '--o', xp, p(xp),'-')

    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title(title)
    plt.grid(True)
    plt.show()


def plot_degree_distro():

    pipeline = [
        {'$group': {
            '_id': '$citation_id',
            'in_degree': {'$sum': 1}}
        },
        {'$group': {
            '_id': '$in_degree',
            'count': {'$sum': 1}}
        },
        {'$project': {
            '_id': 0,
            'degree': '$_id',
            'count': 1}
        },
        {'$sort': {'degree': 1}}
    ]

    in_degrees = db.uspatentcitation.aggregate(pipeline, allowDiskUse=True)


    degree = []
    node_count = []
    for item in in_degrees:
        degree.append(item['degree'])
        node_count.append(item['count'])

    plt.xlabel('In Degree')
    plt.ylabel('Count')
    plt.yscale('log')
    plt.xscale('log')
    plt.title('Number of nodes per in-degree')
    plt.plot(degree, node_count)



def plot_nodes_to_edges_count():
    pipeline = [
        {'$match': {'date': {'$lt': '2017'}}},
        {'$lookup': {
            'from': 'uspatentcitation',
            'localField': 'id',
            'foreignField': 'patent_id',
            'as': 'cites' }
        },
        {'$group': {
            '_id': {'$substr': ['$date', 0, 4]},
            'nodes': {'$sum': 1},
            'edges': {'$sum': {'$size': '$cites'}}}
        },
        {'$project': {
            '_id': 0,
            'year': '$_id',
            'nodes': 1,
            'edges': 1}
        },
        {'$sort': {'year': 1}}
    ]

    edges_to_nodes = db.patent.aggregate(pipeline)

    x = []
    y = []
    x_count = 0
    y_count = 0
    for item in edges_to_nodes:
        x_count = x_count + item['nodes']
        y_count = y_count + item['edges']
        x.append(x_count)
        y.append(y_count)

    plt.plot(x, y, '--o')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Number of nodes')
    plt.ylabel('Number of edges')
    plt.grid(True)
    plt.show()

# db.getCollection('patent').aggregate([{
#         '$lookup': {
#             'from': 'uspatentcitation',
#             'localField': 'id',
#             'foreignField': 'patent_id',
#             'as': 'cites'
#         },
#     }
# ])

# db.getCollection('patent').aggregate([{
#         '$lookup': {
#             'from': 'uspatentcitation',
#             'localField': 'id',
#             'foreignField': 'citation_id',
#             'as': 'cited_by'
#         },
#
#     }
# ])
