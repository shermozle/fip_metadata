FROM python:3.9
ADD main.py .
RUN pip install requests
CMD ["python", "./main.py"]