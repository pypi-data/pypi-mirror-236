<p align='center'>
    <img src='https://iili.io/HIjPRS9.jpg' alt='Pyrubi Library 3.1.0' width='356' class="image">
</p>

<p align='center'>
    <a href='https://github.com/AliGanji1/pyrubi'>GitHub</a>
    •
    <a href='https://rubika.ir/pyrubi_documents'>Documents</a>
</p>


## Pyrubi 3.1.0
> Powerful, easy and modern Rubika API library for building self bots.

[![Downloads](https://static.pepy.tech/badge/pyrubi)](https://pepy.tech/project/pyrubi)


<hr>

### Install or Update:

``` bash
pip install -U pyrubi
```

<hr>

### Quick start:

``` python
from pyrubi import Client

client = Client(session="mySelf")

for message in client.on_message():
    print(message.text)

    if message.text == "hello":
        message.reply("**hello** __from__ ##pyrubi##")
```

also you can enter your session data manually:
```python
from pyrubi import Client

auth_key = "abcdefghijklnopkrstuvwxyzazxcqwe"
private_key = "-----BEGIN RSA PRIVATE KEY-----\n..."

client = Client(auth=auth_key, private=private_key)

for message in client.on_message():
    print(message.text)

    if message.text == "hello":
        message.reply("**hello** __from__ ##pyrubi##")
```

<hr>

### Features:
    
- **Fast** : *The requests are very fast and optimize.*

- **Easy** : *All methods and features are designed as easy and optimal as possible*

- **Powerful** : *While the library is simple, it has high speed and features that make your work easier and faster*


<hr>

### Social Media:
### <a href='https://rubika.ir/pyrubika'>Rubika</a>

<hr>

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AliGanji1/Pyrubi&type=Date)](https://star-history.com/#AliGanji1/Pyrubi&Date)