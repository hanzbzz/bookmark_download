FROM python:3.10-alpine
WORKDIR /usr/app
COPY ./ /usr/app
RUN pip3 install -r requirements.txt
RUN apk add --update npm
RUN npm install
EXPOSE 8080
CMD ["flask", "--app", "downloader.app:create_app", "--debug", "run", "--port=8080"]
#CMD ["waitress-serve", "--call", "--port=8080", "downloader.app:create_app"]