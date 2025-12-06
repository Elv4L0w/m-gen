FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#ostanek kode kopira v container
COPY . .


RUN mkdir -p /app/static/uploads

#opciono pac pomembno je otpreti port 500
ENV PORT=5000
EXPOSE 5000


CMD [ "python", "app.py" ]
