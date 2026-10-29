# notes-mcp image: build the wheel in one stage, run it as a non-root user in a slim one.
FROM python:3.13-slim AS build
WORKDIR /src
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir build==1.6.1 && python -m build --wheel --outdir /dist

FROM python:3.13-slim
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app \
 && mkdir /data && chown app /data
COPY --from=build /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl
ENV NOTES_DIR=/data NOTES_HOST=127.0.0.1 NOTES_PORT=8000 PYTHONUNBUFFERED=1
USER app
VOLUME /data
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)" || exit 1
ENTRYPOINT ["notes-mcp"]
CMD ["--http"]
