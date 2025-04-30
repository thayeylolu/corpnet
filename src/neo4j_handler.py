# src/neo4j_handler.py

from neo4j import GraphDatabase
import os

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🧹 Database cleared.")

    def create_graph(self, graph):
        with self.driver.session() as session:
            for node, attrs in graph.nodes(data=True):
                if attrs["type"] == "company":
                    session.run(
                        """
                        MERGE (c:Company {id: $id})
                        SET c.name = $name,
                            c.jurisdiction = $jurisdiction,
                            c.company_number = $company_number
                        """,
                        id=node,
                        name=attrs.get("name"),
                        jurisdiction=attrs.get("jurisdiction"),
                        company_number=attrs.get("company_number")
                    )
                elif attrs["type"] == "officer":
                    session.run(
                        """
                        MERGE (o:Officer {id: $id})
                        SET o.name = $name
                        """,
                        id=node,
                        name=attrs.get("name")
                    )

            for source, target, edge_attrs in graph.edges(data=True):
                if graph.nodes[source]["type"] == "officer":
                    officer_id, company_id = source, target
                else:
                    officer_id, company_id = target, source

                session.run(
                    """
                    MATCH (o:Officer {id: $officer_id})
                    MATCH (c:Company {id: $company_id})
                    MERGE (o)-[r:SERVES_AS]->(c)
                    SET r.role = $role
                    """,
                    officer_id=officer_id,
                    company_id=company_id,
                    role=edge_attrs.get("role")
                )

            print("✅ Graph pushed to Neo4j.")

