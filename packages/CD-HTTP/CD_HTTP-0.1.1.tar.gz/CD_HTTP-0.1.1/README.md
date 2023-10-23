# HTTP Class

The `HTTP` class provides a simplified interface for making HTTP requests using the popular `requests` library. It supports various functionalities like setting a custom user agent, using proxies, and handling proxy authentication.

## Features

- Simple methods for common HTTP requests (`GET`, `POST`, etc.)
- Customizable user agent
- Proxy support
- Proxy authentication
- Persistent sessions

## Installation

Before using the `HTTP` class, ensure you have the `requests` library installed:

```bash
pip install CD-HTTP=0.1.1
```

## Usage

### Initialization

To start using the `HTTP` class, first create an instance:

```python
from http_class import HTTP

http_client = HTTP()
```

### Making a GET Request

```python
response = http_client.get("https://www.example.com")
```

### Making a POST Request

```python
data = {"key": "value"}
response = http_client.post("https://api.example.com", json=data)
```

### Using a Custom User Agent

```python
response = http_client.get("https://www.example.com", user_agent="MyCustomUserAgent/1.0")
```

### Using a Proxy

```python
response = http_client.get("https://www.example.com", proxy="http://my-proxy.com:8080")
```

### Using Proxy Authentication

```python
response = http_client.get("https://www.example.com", proxy="http://my-proxy.com:8080", proxy_username="username", proxy_password="password")
```

### Passing Additional Headers

```python
headers = {
    "Authorization": "Bearer YOUR_TOKEN_HERE",
    "Custom-Header": "CustomValue"
}
response = http_client.get("https://www.example.com", headers=headers)
```

### Persistent Sessions

To start a persistent session:

```python
http_client.start_session()
```
Your code goes between start_session() and close_session()
To close the session:

```python
http_client.close_session()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

More documentation at:
[Code Docta](https://codedocta.com "My Website")
