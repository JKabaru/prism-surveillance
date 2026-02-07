import pandas as pd
import io
from src.data.data_generator import PRISMDataGenerator

class PRISMDataLoader:
    def __init__(self):
        self.generator = PRISMDataGenerator()

    def load_synthetic(self, num_partners=5, subs_per_partner=3, clients_per_sub=10):
        """Generates synthetic data using PRISMDataGenerator."""
        partners, subs, clients = self.generator.generate_hierarchy(
            num_partners=num_partners, 
            subs_per_partner=subs_per_partner, 
            clients_per_sub=clients_per_sub
        )
        trades = self.generator.generate_trades(clients, subs)
        return partners, subs, clients, trades

    def get_required_columns(self):
        """Returns the mandatory columns for each PRISM table."""
        return {
            "Partners": ["partner_id", "name"],
            "Sub-Affiliates": ["sub_affiliate_id", "parent_partner_id"],
            "Clients": ["client_id", "parent_sub_id"],
            "Trades": ["trade_id", "client_id", "entry_time", "symbol", "direction", "volume"]
        }

    def load_from_files(self, partners_file, subs_file, clients_file, trades_file, column_mapping=None):
        """
        Loads data from file objects with optional column mapping.
        column_mapping: dict of {table_name: {user_col: prism_col}}
        """
        try:
            # Read files
            p_df = pd.read_csv(partners_file)
            s_df = pd.read_csv(subs_file)
            c_df = pd.read_csv(clients_file)
            t_df = pd.read_csv(trades_file)
            
            # Apply mappings if provided
            if column_mapping:
                if "Partners" in column_mapping: p_df = p_df.rename(columns=column_mapping["Partners"])
                if "Sub-Affiliates" in column_mapping: s_df = s_df.rename(columns=column_mapping["Sub-Affiliates"])
                if "Clients" in column_mapping: c_df = c_df.rename(columns=column_mapping["Clients"])
                if "Trades" in column_mapping: t_df = t_df.rename(columns=column_mapping["Trades"])

            # Validate
            req = self.get_required_columns()
            self._validate_columns(p_df, req["Partners"])
            self._validate_columns(s_df, req["Sub-Affiliates"])
            self._validate_columns(c_df, req["Clients"])
            self._validate_columns(t_df, req["Trades"])
            
            # Conversions
            for df in [t_df]:
                if 'entry_time' in df.columns: df['entry_time'] = pd.to_datetime(df['entry_time'])
                if 'exit_time' in df.columns: df['exit_time'] = pd.to_datetime(df['exit_time'])

            return p_df, s_df, c_df, t_df
        except Exception as e:
            raise ValueError(f"Ingestion failed: {str(e)}")


    def load_from_db(self, connection_string):
        """
        Mock implementation for Database connection.
        In a real app, this would use SQLAlchemy or similar.
        """
        # Simulate connection check
        if "mock" in connection_string.lower():
            return True, "Connected to Mock Database (Success)"
        else:
            return False, "Database connection failed: Invalid credentials"

    def _validate_columns(self, df, required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
