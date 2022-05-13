# QA service


## Run service inside docker

```bash
docker compose up
```
---

## Examples


### Request
```bash
curl -X POST http://127.0.0.1:8888/ -H 'Content-Type: application/json' -d '{"question": "What is the capital of Great Britain?"}'
```

```python
> import requests
> res = requests.post('http://127.0.0.1:8888/', json={"question": "What is the capital of Great Britain?"})
> print(res.json())
```

### Expected result:

```json
{"answer":"London"}
```