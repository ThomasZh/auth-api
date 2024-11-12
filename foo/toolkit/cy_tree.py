#!/usr/bin/env python
# _*_ coding: utf-8_*_


def remove_empty_systree_nodes(nodes):
    leaf_nodes = set()
    systree_nodes = set()
    systree_with_leaf = set()  # 辅助集合

    for node in nodes:
        if node["type"] == "leaf":
            leaf_nodes.add(node["id"])
            systree_nodes.add(node["pid"])
            systree_with_leaf.add(node["pid"])  # 添加关联了type=leaf节点的type=systree节点的id
        elif node["type"] == "systree":
            systree_nodes.add(node["id"])

    new_nodes = []
    for node in nodes:
        if node["type"] == "leaf" or (node["type"] == "systree" and (node["id"] in systree_with_leaf or node["id"] in systree_nodes)):
            new_nodes.append(node)

    # Remove parent nodes that do not have any leaf nodes associated with them
    final_nodes = []
    for node in new_nodes:
        if node["type"] == "leaf" or node["id"] in systree_with_leaf:
            final_nodes.append(node)

    return final_nodes


def build_tree(data, parent_id=None):
    tree = []

    for item in data:
        if item["type"] == "systree":
            node = {"id": item["id"], "pid": item["pid"],
                "label": item["title"], "value": item["title"],
                "isLeaf": False, "selectable": False, "disabled": True,
                "depth": item["depth"], "children": []}
            if item["depth"] == 0:
                tree.append(node)
            else:
                parent_node = find_node(tree, item["depth"] - 1, item["pid"])
                if parent_node:
                    parent_node["children"].append(node)
        elif item["type"] == "leaf":
            node = {"id": item["id"], "pid": item["pid"],
                "label": item["title"] + ": " + item["_tablename"], "value": item["_tablename"],
                "isLeaf": True, "selectable": True, "disabled": False,
                "depth": item["depth"], "children": []}
            parent_node = find_node(tree, item["depth"] - 1, item["pid"])
            if parent_node:
                parent_node["children"].append(node)

    return tree


def find_node(tree, depth, parent_id):
    for node in tree:
        print(node)
        if node["depth"] == depth and node["id"] == parent_id:
            return node
        else:
            child_node = find_node(node["children"], depth, parent_id)
            if child_node is not None:
                return child_node
