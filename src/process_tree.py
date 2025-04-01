
import pandas as pd
import networkx as nx

# Constructs a directed graph from parent-child process relationships.
def build_process_tree(process_df: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for _, row in process_df.iterrows():
        G.add_node(row['process_id'], **row.to_dict())
        G.add_edge(row['parent_id'], row['process_id'])
    return G

# Extracts all file, network, and registry events linked to a given process ID.
def extract_events_for_pid(pid: int, file_df, net_df, reg_df):
    events = []
    for _, row in file_df[file_df['process_id'] == pid].iterrows():
        events.append(f"  - File Event: {row['timestamp']} | Operation: {row['operation']} | Path: {row['file_path']}")
    for _, row in net_df[net_df['process_id'] == pid].iterrows():
        events.append(f"  - Network Event: {row['timestamp']} | SrcIP: {row['src_ip']}:{row['src_port']} → DstIP: {row['dst_ip']}:{row['dst_port']}")
    for _, row in reg_df[reg_df['process_id'] == pid].iterrows():
        val_str = f" | Value: {row['value_name']} = {row['value_data']}" if pd.notnull(row['value_name']) else ""
        events.append(f"  - Registry Event: {row['timestamp']} | Operation: {row['operation']} | Key: {row['registry_key']}{val_str}")
    return events

# Recursively traverses the process tree from root_pid and writes a markdown report.
# Includes cycle detection to avoid infinite loops.
def write_process_tree_markdown_safe(graph: nx.DiGraph, root_pid: int, file_df, net_df, reg_df, output_path):
    visited = set()
    with open(output_path, "w", encoding="utf-8") as f:
        def dfs(pid: int, indent: int = 0):
            if pid in visited:
                f.write(f"{'  ' * indent}- process_id: {pid} (cycle detected, already visited)\n")
                return
            visited.add(pid)
            if pid not in graph.nodes:
                f.write(f"{'  ' * indent}- process_id: {pid} (not found in graph)\n")
                return
            node = graph.nodes[pid]
            indent_str = "  " * indent
            f.write(f"{indent_str}- process_id: {pid}, parent_id: {node['parent_id']}, executable_path: {node['executable_path']}, user: {node['user']}, start_time: {node['start_time']}\n")
            for event in extract_events_for_pid(pid, file_df, net_df, reg_df):
                f.write(f"{indent_str}{event}\n")
            for child_pid in list(graph.successors(pid)):
                dfs(child_pid, indent + 1)
        dfs(root_pid)
