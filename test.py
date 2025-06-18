from urllib.parse import parse_qs, urlparse

# Example URL
url = "https://example.com?key=value&key2=value2"

# Parse query string
query_string = urlparse(url).query
decoded = parse_qs(query_string)

print(decoded)  # Output: {'key': ['value'], 'key2': ['value2']}