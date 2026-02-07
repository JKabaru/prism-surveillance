import networkx as nx
import pandas as pd

class PRISMNetworkMapper:
    def __init__(self, clients_df, subs_df, partners_df):
        self.clients_df = clients_df
        self.subs_df = subs_df
        self.partners_df = partners_df
        
    def build_hierarchy_graph(self, client_ids):
        """
        Builds a NetworkX graph showing the relationship between clients, subs, and partners.
        """
        G = nx.DiGraph()
        
        relevant_clients = self.clients_df[self.clients_df['client_id'].isin(client_ids)]
        
        for _, client in relevant_clients.iterrows():
            c_node = f"C:{client['client_id']}"
            s_node = f"S:{client['parent_sub_id']}"
            p_node = f"P:{client['master_partner_id']}"
            
            # Add nodes with attributes
            G.add_node(c_node, type='client', label=client['name'])
            G.add_node(s_node, type='sub', label=client['parent_sub_id'])
            G.add_node(p_node, type='partner', label=client['master_partner_id'])
            
            # Add edges (bottom up for detection attribution)
            G.add_edge(c_node, s_node)
            G.add_edge(s_node, p_node)
            
        return G

    def build_filtered_graph(self, client_ids, trades_df, filters=None):
        """
        Builds a graph highlighting clients who participated in specific trades.
        Filters: {'min_volume': 5.0, 'symbol': 'EURUSD', 'direction': 'Buy'}
        """
        G = self.build_hierarchy_graph(client_ids)
        
        if not filters:
            return G
            
        # Filter trades
        filtered_trades = trades_df[trades_df['client_id'].isin(client_ids)]
        
        if 'symbol' in filters and filters['symbol']:
            filtered_trades = filtered_trades[filtered_trades['symbol'] == filters['symbol']]
        if 'direction' in filters and filters['direction']:
             filtered_trades = filtered_trades[filtered_trades['direction'] == filters['direction']]
        if 'min_volume' in filters and filters['min_volume']:
             filtered_trades = filtered_trades[filtered_trades['volume'] >= filters['min_volume']]
             
        active_clients = filtered_trades['client_id'].unique().tolist()
        
        # Mark nodes as active/inactive based on filter
        for node in G.nodes():
            if G.nodes[node]['type'] == 'client':
                start_node = node.split(":")[1]
                if start_node in active_clients:
                    G.nodes[node]['status'] = 'active'
                else:
                    G.nodes[node]['status'] = 'inactive'
            else:
                 G.nodes[node]['status'] = 'active' # Partners/Subs always visible for context
                 
        return G

    def get_attribution(self, client_ids):
        """
        Identifies common partners or sub-affiliates for a group of clients.
        """
        relevant_clients = self.clients_df[self.clients_df['client_id'].isin(client_ids)]
        
        partner_counts = relevant_clients['master_partner_id'].value_counts().to_dict()
        sub_counts = relevant_clients['parent_sub_id'].value_counts().to_dict()
        
        return {
            "top_partners": partner_counts,
            "top_subs": sub_counts,
            "is_cross_partner": len(partner_counts) > 1,
            "is_cross_sub": len(sub_counts) > 1
        }
