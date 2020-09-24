FROM python:3.8

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

RUN pip install -r requirements.txt

# This is only for deployment on GCP, not related to the task.
RUN wget https://github.com/nomeaning777/exec-with-secret/releases/download/v0.1.2/exec-with-secret-amd64 -O /bin/exec-with-secret && chmod +x /bin/exec-with-secret

USER nobody:nogroup
ENTRYPOINT [ "/bin/exec-with-secret", "functions-framework", "--target", "index" ]
