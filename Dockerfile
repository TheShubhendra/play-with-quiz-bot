FROM python:3.9.13-alpine3.15
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY bot.py ./
CMD ["python", "bot.py"]