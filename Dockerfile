FROM endeeio/endee-server:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu --break-system-packages

RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

RUN chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]