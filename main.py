# import subprocess

# subprocess.run('ipconfig /displaydns > "C:\\Users\\Krish Vij\\dns.txt"', text=True, shell = True)

def check_dns_records() -> None:
    
    with open ("C:\\Users\\Krish Vij\\dns.txt", "r") as file:
        content = file.readlines()
        for line in content:
            if "www.google.com" in line:
                print("Found www.google.com DNS record")

def main() -> None:
    check_dns_records()

if __name__ == "__main__":
    main()