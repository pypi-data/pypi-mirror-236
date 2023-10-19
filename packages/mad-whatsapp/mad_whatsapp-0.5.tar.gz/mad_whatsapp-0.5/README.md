# MA-D 2023 - WhatsApp Conversation Parser
Parses a whatsapp conversation export into an array of messages in the form of:

```json
{
  "timestamp": "15/3/23 23:23",
  "author": "Jane Doe",
  "message": "Hello world!"
}
```

## Build

```bash
python setup.py sdist bdist_wheel
```

## Publish

```bash
twine upload dist/*
```
