import subprocess
import dns.message
import dns.flags
import dns.query
import dns.rdatatype
import dns.resolver

root_servers = [
    "198.41.0.4",
    "170.247.170.2",
    "192.33.4.12",
    ]

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
        ask_resolver_to_iterate_until_found(domain, record_type)
    else:
        print("MISS: Not found in cache")
    print(f"Response from open resolver for {domain} ({record_type}):")
    print(response)
    print(response.answer)
    print(response.authority)

def ask_resolver_to_iterate_until_found(domain: str, record_type: str) -> None:
    current_server = root_servers

    while current_server:
        if not current_server:
            print(f"Could not resolve {domain} further.")
            return
        
        query = dns.message.make_query(domain, record_type)
        query.flags &= ~dns.flags.RD  # Recursion Not Desired

        for server in current_server:
            response = dns.query.udp(query, server, timeout=3)

            if response.answer:
                print("HIT: Found in cache")
                print(f"Response from {server} for {domain} ({record_type}):")
                print(response)
                return
            elif response.authority:
                ns_servers_name = []
                ns_servers_ip = []
                for rrset in response.authority:
                    if rrset.rdtype == dns.rdatatype.NS:
                        for rr in rrset:
                            ns_name = rr.target.to_text()
                            ns_servers_name.append(ns_name)
                for ns_name in ns_servers_name:
                            try:
                                ns_ip = dns.resolver.resolve(ns_name, 'A')[0].to_text()
                                ns_servers_ip.append(ns_ip)
                            except Exception as e:
                                print(f"Could not resolve NS {ns_name}: {e}")
                                continue
                if not ns_servers_name:
                    print("No NS records found in authority section.")
                    return
                # current_server = ns_servers_ip
                # query = dns.message.make_query(domain, record_type)
                # query.flags &= ~dns.flags.RD  # Recursion Not Desired
                # for ns_server in ns_servers_ip:
                #     response = dns.query.udp(query, ns_server, timeout=3)
                #     if response.answer:
                #         print("HIT: Found in cache")
                #         print(f"Response from {server} for {domain} ({record_type}):")
                #         print(response)
                #         return
                #     elif response.authority:
                #         print("Continuing to next level of authority...")
                #     else:
                #         print("MISS: Not found in cache")
                if not ns_servers_ip:
                    print(f"Could not resolve {domain} further.")
                    return
                current_server = ns_servers_ip


def main() -> None:
    domain = input("Enter the domain to check DNS records for: ")
    foundInCache = check_dns_records(domain)
    if not foundInCache:
        print(f"No relevant DNS records found for {domain}.")
        query_dns_record_to_open_resolver(domain, "A")

if __name__ == "__main__":
    main()
