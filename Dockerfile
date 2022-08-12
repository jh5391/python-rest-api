FROM python:3.9.7

ENV database_hostname ""
ENV database_port 3306
ENV database_password ""
ENV database_name ""
ENV database_username ""
ENV secret_key ""
ENV algorithm ""
ENV access_token_expire_minutes 30

WORKDIR /usr/src/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /usr/src/app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]