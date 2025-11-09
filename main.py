import subprocess
# import dns.resolver
import dns.message
import dns.flags
import dns.query
# from dns.resolver import Resolver

def check_dns_records(domain:str) -> bool:
    """Check DNS records for a given domain in the local DNS cache."""
    subprocess.run('ipconfig /displaydns > "C:\\Users\\Krish Vij\\dns.txt"', text=True, shell = True)
    with open ("C:\\Users\\Krish Vij\\dns.txt", "r") as file:
        content = file.readlines()
        print("Checking DNS records in local cache...")
        for line in content:
            if domain in line:
                print(f"Found {domain} DNS record")
                if "A" in content[content.index(line) + 15]:
                    print(f"Record type A found for {domain}")
                    print(content[content.index(line) + 15])
                    return True
                else:
                    print(f"No A record found for {domain}")
                    
    return False

def query_dns_record_to_open_resolver(domain: str, record_type: str) -> None:
    query = dns.message.make_query(domain, record_type)
    query.flags &= ~dns.flags.RD  # Recursion Not Desired
    response = dns.query.udp(query, '8.8.8.8', timeout = 3)
    print(f"Response from open resolver for {domain} ({record_type}):")
    print(response)
    

def main() -> None:
    domain = input("Enter the domain to check DNS records for: ")
    found = check_dns_records(domain)
    if not found:
        print(f"No relevant DNS records found for {domain}.")
        query_dns_record_to_open_resolver(domain, "A")

if __name__ == "__main__":
    main()