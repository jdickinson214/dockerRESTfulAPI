FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENV GOOGLE_APPLICATION_CREDENTIALS='./hw8-dickinsj-user.json'
ENV PORT=8000
EXPOSE ${PORT}
CMD [ "python", "./main.py"]