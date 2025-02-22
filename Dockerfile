FROM python:3.10-slim

RUN addgroup lift && adduser lift --ingroup lift --home /opt/lift && chown -R lift:lift /opt/lift

RUN pip3 install --no-cache-dir poetry

WORKDIR /opt/lift/src

RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

RUN poetry install --no-root

ENV PYTHONPATH /opt/lift/src

ENV PYTHONDONTWRITEBYTECODE 1

COPY --chown=lift . .

USER lift

EXPOSE 5000

CMD ["flask","--app", "src.main", "run", "--host", "0.0.0.0", "--port", "5000"]
