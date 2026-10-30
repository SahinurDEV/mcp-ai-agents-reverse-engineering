# Capstone Part C: the Section 9 token-gated HTTP server, packaged on the Section 12 base image.
FROM notes-mcp:1.0.0
USER root
COPY app /app
RUN chown -R root:root /app && chmod -R a-w /app
ENV NOTES_DIR=/data PYTHONUNBUFFERED=1
USER app
HEALTHCHECK NONE
ENTRYPOINT ["python", "/app/s09/http_notes.py"]
