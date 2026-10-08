# HELP

use virtual environment :
```bash
# activate
>$ source .venv/bin/activate

# deactivate
>$ deactivate
```

run the live server :
```bash
>$ uv run fastapi dev
```

## Docker

build image : `docker image build -t <TAG> .`
run container : `docker container run -p80:80 -v $(pwd)/data:/code/data <TAG>`
