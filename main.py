import subprocess
import dns.message
import dns.flags
import dns.query

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
    """Query an open DNS resolver for a specific DNS record type.
    Creates a DNS query message for the specified domain and record type, 
    sends it to Google's public DNS server with recursion disabled,
    and prints the response."""
    query = dns.message.make_query(domain, record_type)
    query.flags &= ~dns.flags.RD  # Recursion Not Desired
    response = dns.query.udp(query, '8.8.8.8', timeout = 3)
    if response.answer:
        print("HIT: Found in cache")
    elif response.authority:
        ask_resolver_to_iterate_until_found(domain, "NS")
    else:
        print("MISS: Not found in cache")
    print(f"Response from open resolver for {domain} ({record_type}):")
    print(response)

# def ask_resolver_to_iterate_until_found(domain: str, record_type: str) -> None:


def main() -> None:
    domain = input("Enter the domain to check DNS records for: ")
    foundInCache = check_dns_records(domain)
    if not foundInCache:
        print(f"No relevant DNS records found for {domain}.")
        query_dns_record_to_open_resolver(domain, "A")

if __name__ == "__main__":
    main()