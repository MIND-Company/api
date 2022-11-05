FROM python
WORKDIR /parking
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install --no-cache-dir -r parking/requirements.txt