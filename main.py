import dns.resolver

def dns_lookup(domain: str, record_type: str) -> list[str]:
    
    resolver = dns.resolver.get_default_resolver()
    answers = resolver.resolve(domain, record_type)
    return [answer.to_text() for answer in answers]

def main() -> None:
    domain = 'google.com'
    record_type = 'A'
    try:
        results = dns_lookup(domain, record_type)
        print(f'{record_type} records for {domain}:')
        for result in results:
            print(result)
    except Exception as e:
        print(f'Error occurred: {e}')

if __name__ == '__main__':
    main()
