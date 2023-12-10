FROM python:3.9.9-alpine
WORKDIR /app
ENV FLASK_APP=app.py \
  FLASK_RUN_HOST=0.0.0.0 \
  PYTHONDONTWRITEBYTECODE=1 \
  TEMPLATES_AUTO_RELOAD:='True' \
  FLASK_ENV=development
RUN apk add --no-cache gcc musl-dev linux-headers ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
#CMD ["flask", "run"]
CMD ["flask", "run", "--reload"]
