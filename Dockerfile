FROM python:3.10-slim

RUN addgroup lift && adduser lift --ingroup lift --home /opt/lift && chown -R lift:lift /opt/lift

RUN pip3 install --no-cache-dir poetry

WORKDIR /opt/lift/src

RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

RUN poetry install

ENV PYTHONPATH /opt/lift/src

COPY --chown=lift . .

USER lift

CMD ["python", "-m", "src/prices.py"]
