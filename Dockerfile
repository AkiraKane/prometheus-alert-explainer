FROM python:3.12-slim
WORKDIR /app
COPY src/ .
EXPOSE 9100
CMD ["python", "main.py", "--webhook"]
