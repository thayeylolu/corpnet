from src.neo4j_handler import Neo4jHandler

from dotenv import load_dotenv
import os
from src.api_client import OpenCorporatesClient
from src.graph_builder import CorpGraphBuilder
import networkx as nx

# Load .env credentials
load_dotenv()

def main():
    query = "Nestle"  # You can update this with user input or CLI args
    num_companies = 3

    client = OpenCorporatesClient()
    graph_builder = CorpGraphBuilder()

    print(f"🔍 Searching for companies matching: {query}")
    results = client.search_companies(query, per_page=num_companies)
    companies = results.get("results", {}).get("companies", [])

    if not companies:
        print("❌ No companies found.")
        return

    for c in companies:
        company = c["company"]
        print(f"\n🏢 Processing {company['name']} ({company['jurisdiction_code']}/{company['company_number']})")

        try:
            company_details = client.get_company(company["jurisdiction_code"], company["company_number"])
            officers = client.get_officers(company["jurisdiction_code"], company["company_number"])

            graph_builder.add_company(company_details["results"]["company"])
            graph_builder.add_officers(company_details["results"]["company"], officers)

        except Exception as e:
            print(f"⚠️ Skipping {company['name']} due to error: {e}")

    G = graph_builder.get_graph()
    print(f"\n✅ Finished. Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # (Optional) Save to GraphML
    nx.write_graphml(G, "output/corpnet.graphml")
    print("📤 Graph exported to output/corpnet.graphml")




# Push to Neo4j
neo4j = Neo4jHandler(
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD")
)

neo4j.clear_database()
neo4j.create_graph(G)
neo4j.close()
if __name__ == "__main__":
    main()
