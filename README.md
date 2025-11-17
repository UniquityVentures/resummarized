# Resummarized

To init:

```bash
uv run manage.py tailwind install
uv run manage.py migrate
uv run manage.py createsuperuser
uvx --from huggingface_hub[cli] hf auth login
```

To create db:

```sql
CREATE DATABASE resummarized;
CREATE EXTENSION vector;
```

To run:

```bash
uv run manage.py tailwind dev
```


