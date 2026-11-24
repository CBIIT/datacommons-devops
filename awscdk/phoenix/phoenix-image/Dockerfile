FROM python:3.11-slim AS builder

# Install aioboto3 into an isolated prefix we can copy out
RUN pip install --no-cache-dir --target=/deps aioboto3

FROM arizephoenix/phoenix:latest

# Copy the installed packages into the site-packages path Phoenix's Python uses.
COPY --from=builder /deps /opt/extra-deps
ENV PYTHONPATH=/phoenix/.venv/lib/python3.13/site-packages:/opt/extra-deps