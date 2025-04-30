# scripts/demo.py

from src.api_client import OpenCorporatesClient

def main():
    client = OpenCorporatesClient()

    # Search companies matching a keyword
    print("🔍 Searching for companies matching 'Nestle'...")
    search_results = client.search_companies("Nestle", per_page=3)

    companies = search_results.get('results', {}).get('companies', [])
    if not companies:
        print("❌ No companies found.")
        return

    for i, c in enumerate(companies, 1):
        company = c['company']
        print(f"{i}. {company['name']} — {company['jurisdiction_code']} / {company['company_number']}")

    # Pick the first result for demo
    selected = companies[0]['company']
    jurisdiction = selected['jurisdiction_code']
    company_number = selected['company_number']

    print(f"\n📄 Fetching company details for: {selected['name']}")
    details = client.get_company(jurisdiction, company_number)
    print(details['results']['company'])

    print(f"\n👤 Fetching officers for: {selected['name']}")
    officers = client.get_officers(jurisdiction, company_number)
    for officer in officers['results']['officers']:
        print(f"- {officer['officer']['name']} ({officer['officer']['position']})")

if __name__ == "__main__":
    main()
