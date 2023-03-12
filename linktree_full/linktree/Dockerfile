FROM python:3.9

WORKDIR .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 1st flag spark{FAKEPASSWORD}
RUN sed -i 's|<password>REDACTED</password>|<password>FAKEPU71N</password>|g' users.xml

# 2nd flag spark{FAKE_FLAG}
ENV FLAG=FAKE_FLAG 

EXPOSE 1337
RUN python ssoUpdater.py
CMD ["python", "app.py"]
