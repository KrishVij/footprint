import dns.resolver
# from dns.resolver import get_default_resolver
from dns.resolver import CacheBase

resolver = dns.resolver.get_default_resolver()
CacheBase = CacheBase()
how_many_hits = CacheBase.hits()

ip_address = dns.resolver.resolve('google.com', 'A')[0].to_text()

print("Cache Hits:", how_many_hits)
print("IP Address:", ip_address)


