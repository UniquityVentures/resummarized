# Resummarized

To create db:

```sql
CREATE DATABASE resummarized;
CREATE EXTENSION vector;
```

To init:

```bash
uv run manage.py tailwind install
uv run manage.py migrate
uv run manage.py createsuperuser
uvx --from huggingface_hub[cli] hf auth login
```

To run:

```bash
uv run manage.py tailwind dev
```


To format:

```bash
uv tool run djlint . --reformat
uv tool run djhtml .
```
