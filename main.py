import dns.resolver

ip_address = dns.resolver.resolve('chatgpt.com', 'A')[0].to_text()
print(ip_address)

