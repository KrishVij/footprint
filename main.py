import dns.resolver
from dns.resolver import get_default_resolver

ip_address = dns.resolver.resolve('chatgpt.com', 'A')[0].to_text()
resolver = get_default_resolver()
print("Default DNS Resolver:", resolver)
print("Ip Address:", ip_address)



