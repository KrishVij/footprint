import subprocess

subprocess.run('ipconfig /displaydns > "C:\\Users\\Krish Vij\\dns.txt"', text=True, shell = True)

def check_dns_records() -> None:
    with open ("C:\\Users\\Krish Vij\\dns.txt", "r") as file:
        contents = file.read()
        for line in contents.splitlines():
            if "Record Name . . . . . : google.com" in line :
                print("Found google.com DNS record")
    print(contents)

def main() -> None:
    check_dns_records()

if __name__ == "__main__":
    main()