import subprocess

def check_dns_records(domain:str) -> None:
    subprocess.run('ipconfig /displaydns > "C:\\Users\\Krish Vij\\dns.txt"', text=True, shell = True)
    found = False
    with open ("C:\\Users\\Krish Vij\\dns.txt", "r") as file:
        content = file.readlines()
        print("Checking DNS records in local cache...")
        for line in content:
            if domain in line:
                print(f"Found {domain} DNS record")
                if "A" in content[content.index(line) + 15]:
                    print(f"Record type A found for {domain}")
                    print(content[content.index(line) + 15])
                    found = True
                    break
                else:
                    print(f"No A record found for {domain}")
                    break

def main() -> None:
    domain = input("Enter the domain to check DNS records for: ")
    check_dns_records(domain)

if __name__ == "__main__":
    main()