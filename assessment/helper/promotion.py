# script.py
import argparse
import os
import sys

import my_connection as connection
import networkx as nx
import pyexcel as pe

# import matplotlib.pyplot as plt

DB_URL = None
global conn
conn = None
sheet = None

desg_ls_unit_promo = None
desg_ls_area_promo = None
unit_ls = None
sect_ls = None
xcd_desg_ls = None


def load_tables():
    # conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select dscd from desg where cadre<>'E' ")
    global desg_ls_unit_promo
    desg_ls_unit_promo = [x[0] for x in c.fetchall()]

    c.execute("select dscd from desg where cadre<>'E' and promotion='A' ")
    global desg_ls_area_promo
    desg_ls_area_promo = [x[0] for x in c.fetchall()]

    c.execute("select dscd from desg where cadre='XCD' ")
    global xcd_desg_ls
    xcd_desg_ls = [x[0] for x in c.fetchall()]


def validate_row(row, idx):
    # hold all error list
    err = []

    # check wrong codes
    if row['from'] not in desg_ls_unit_promo:
        err.append("err @row-" + str(idx) + " : from dscd(" + row['from'] + ") wrong")

    for to_desg in row['to'].split(","):
        to_desg = to_desg.strip()
        if (to_desg):
            if to_desg not in desg_ls_unit_promo:
                err.append("err @row-" + str(idx) + " : to dscd(" + to_desg + ") wrong")
            # check xcd in to desg
            if to_desg in xcd_desg_ls:
                err.append("err @row-" + str(idx) + " : to dscd(" + to_desg + ") not promotable")

    # return err list
    if not err:
        return None
    else:
        return err


def validate():
    try:
        xls_path = "./desg_mapping.xls"
        sheet_name = "map"
        sheet = pe.get_sheet(file_name=os.path.normpath(xls_path), sheet_name=sheet_name, name_columns_by_row=0)

    except ValueError as e:
        print("Sheet name not in excel file: {0}".format(e))
        sys.exit()
    except AttributeError as e:
        print("Sheet name not in excel file: {0}".format(e))
        sys.exit()
        # raise e
    except NotImplementedError as e:
        print("File not found or File not in proper format: {0}".format(e))
        sys.exit()
        # raise e

    records = sheet.get_records()
    error_ls = []

    for idx, record in enumerate(records):
        err_row = validate_row(record, idx)

        if err_row:
            error_ls.append(err_row)
            print(err_row)

    if error_ls:
        print('correct the above errors and upload')

    records = sheet.get_records()
    return records


def make_graph(desg_ls, mappings):
    G_to = nx.DiGraph()
    # G_from = nx.DiGraph()
    desg_to = {}
    desg_from = {}
    dummy_root_desg = "XXYYZZZ"

    # desg_ls.append(dummy_root_desg)

    # print(desg_ls)
    G_to.add_nodes_from(desg_ls)
    # G_from.add_nodes_from(desg_ls)

    G_to.add_node(dummy_root_desg)
    # G_from.add_node(dummy_root_desg)

    for row in mappings:
        # print(row)
        from_desg = row['from']
        if from_desg in desg_ls:
            for to_desg in row['to'].split(","):
                to_desg = to_desg.strip()
                if (to_desg):
                    G_to.add_edge(from_desg, to_desg)
                # G_from.add_edge(to_desg, from_desg)
                else:
                    G_to.add_edge(from_desg, dummy_root_desg)
                # G_from.add_edge(dummy_root_desg, from_desg)

    print("graph-->", G_to.number_of_edges())
    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    # red_edges = []
    # edge_colours = ['black' if not edge in red_edges else 'red'
    #             for edge in G_to.edges()]
    # black_edges = [edge for edge in G_to.edges() if edge not in red_edges]
    # pos = nx.spring_layout(G_to)
    # nx.draw_networkx_nodes(G_to, pos, cmap=plt.get_cmap('jet'),
    #                     node_size = 500)
    # nx.draw_networkx_labels(G_to, pos)
    # nx.draw_networkx_edges(G_to, pos, edgelist=black_edges, arrows=True)
    # plt.show()

    return G_to


def get_data(unit_filter):
    c = conn.cursor()
    c.execute('''select dscd, ifnull(sum(tot),0) ext, ifnull(sum(san),0) san 
        from unit_dscd_ers 
        where unit like ? 
        group by dscd''', (unit_filter,))
    ls = c.fetchall()
    data = {}
    data["XXYYZZZ"] = {"ext": 0, "san": 0, "promo": 0, "res_ext": 0}
    for row in ls:
        data[row[0]] = {"ext": row[1], "san": row[2], "promo": 0, "res_ext": row[1]}
    return data


def get_data_area(area_filter):
    c = conn.cursor()
    c.execute('''select dscd, ifnull(sum(unit_promo)+sum(res_ext),0) ext, ifnull(sum(san),0) san 
        from promo 
        where substr(unit,2,2) = ? 
        group by dscd''', (area_filter,))
    ls = c.fetchall()
    data = {}
    data["XXYYZZZ"] = {"ext": 0, "san": 0, "promo": 0, "res_ext": 0}
    for row in ls:
        data[row[0]] = {"ext": row[1], "san": row[2], "promo": 0, "res_ext": row[1]}
    return data


def calc_promo(data, to_graph):
    # data in the format of {dscd:{ext:ext,san:san}}
    ls = list(reversed(list(nx.topological_sort(to_graph))))
    # print(ls)
    for curr in ls:
        if curr not in data:
            data[curr] = {"ext": 0, "san": 0, "promo": 0, "res_ext": 0}

    # ls = [i for i in ls if "SCSEC" in i] # to comment out
    # print(ls)
    for curr in ls:
        data[curr] = data[curr]

        # succ = to_graph.succ[curr]
        # succ_promo = 0
        # for key in succ.items():
        #     succ_promo = succ_promo + data[key][promo]

        pred = to_graph.pred[curr]
        pred_ext = 0
        # print(pred)
        for key in pred:
            pred_ext = pred_ext + int(data[key]["res_ext"])
            # print(pred_ext, data[curr]["res_ext"])

        possible_promo = 0
        if data[curr]["san"] > data[curr]["res_ext"]:
            # print(pred_ext,data[curr]["san"] - data[curr]["res_ext"])
            possible_promo = min(pred_ext, data[curr]["san"] - data[curr]["res_ext"])

        if possible_promo > 0:
            while possible_promo > 0:
                for pred_item in pred:
                    if data[pred_item]["res_ext"] > 0:
                        to_promote = min(data[pred_item]["res_ext"], possible_promo)
                        # reduce existing in lower grade
                        data[pred_item]["res_ext"] = data[pred_item]["res_ext"] - to_promote
                        possible_promo = possible_promo - to_promote
                        # add promotion count in current grade
                        data[curr]["promo"] = data[curr]["promo"] + to_promote

        # print("dscd = {} pred.ext={} possible_promo={}".format(curr, pred_ext, possible_promo))

    # return [(i, data[i]) for i in data if data[i]["promo"]>0]
    return [(i, data[i]) for i in data if data[i]["promo"] + data[i]["san"] + data[i]["res_ext"] + data[i]["ext"] > 0]


def promo_sync(ls, unit):
    c = conn.cursor()
    c.execute('delete from promo where unit=?', (unit,))
    c.executemany('''insert into promo
        values(?,?,?,?,?,?,?)''', ls)
    conn.commit()
    print('--->{0} records inserted sucessfully'.format(len(ls)))


def get_valid_units():
    c = conn.cursor()
    c.execute("select distinct unit from unit_dscd_ers")
    return [x[0] for x in c.fetchall()]


def get_valid_areas():
    c = conn.cursor()
    c.execute("select distinct substr(unit,2,2) from unit_dscd_ers")
    return [x[0] for x in c.fetchall()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'filename', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='give a file name')
    parser.add_argument("-f", '--filter', help='enter unit_code full/partial to filter')

    # read_config()
    conn = connection.get_connection()
    load_tables()

    mappings = validate()

    # to_graph_unit_promo = make_graph(desg_ls_unit_promo, mappings)
    # valid_units = get_valid_units()
    # # valid_units = ["C08SEC"]
    # for unit in valid_units:
    #     data = get_data(unit)
    #     # print(data)
    #     promo = calc_promo(data, to_graph_unit_promo)
    #     promo = [(unit, i[0], i[1]["res_ext"],i[1]["promo"],0,0,i[1]["san"]) for i in promo]
    #     promo_sync(promo, unit)

    to_graph_area_promo = make_graph(desg_ls_area_promo, mappings)
    valid_areas = get_valid_areas()
    for area in valid_areas:
        data = get_data_area(area)
        promo = calc_promo(data, to_graph_area_promo)
        promo = [("X" + area, i[0], i[1]["res_ext"], i[1]["promo"], 0, 0, i[1]["san"]) for i in promo]
        promo_sync(promo, "X" + area)

    # print(promo)
