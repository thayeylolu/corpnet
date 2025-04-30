# src/graph_builder.py

import networkx as nx

class CorpGraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def add_company(self, company_data):
        company_id = self._get_company_id(company_data)
        self.graph.add_node(company_id, 
                            type="company",
                            name=company_data.get("name"),
                            jurisdiction=company_data.get("jurisdiction_code"),
                            company_number=company_data.get("company_number"))
        return company_id

    def add_officers(self, company_data, officers_data):
        company_id = self._get_company_id(company_data)

        for officer_entry in officers_data.get('results', {}).get('officers', []):
            officer = officer_entry.get("officer", {})
            officer_name = officer.get("name")
            if not officer_name:
                continue

            officer_id = f"officer::{officer_name.lower().replace(' ', '_')}"
            self.graph.add_node(officer_id, type="officer", name=officer_name)

            # Edge between officer and company
            self.graph.add_edge(officer_id, company_id, role=officer.get("position"))

    def _get_company_id(self, company_data):
        return f"company::{company_data['jurisdiction_code']}::{company_data['company_number']}"

    def get_graph(self):
        return self.graph
