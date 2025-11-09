import subprocess
import dns.resolver
from dns.resolver import Resolver

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
    resolver = Resolver()
    resolver.nameservers = ['8.8.8.8']
    answer = dns.resolver.resolve(domain, record_type)[0].to_text() # type: ignore[reportUnknownMemberType]
    print(f"{record_type} record for {domain} from open resolver: {answer}")
    

def main() -> None:
    domain = input("Enter the domain to check DNS records for: ")
    found = check_dns_records(domain)
    if not found:
        print(f"No relevant DNS records found for {domain}.")
        query_dns_record_to_open_resolver(domain, "A")

if __name__ == "__main__":
    main()