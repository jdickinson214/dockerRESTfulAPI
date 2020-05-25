FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS='./hw8-dickinsj-user.json'
EXPOSE ${PORT}
CMD [ "python", "./main.py"]