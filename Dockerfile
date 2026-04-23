# Python'un hafif bir sürümünü kullanıyoruz
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Klasördeki her şeyi Docker içine kopyala
COPY . .

# Railway'in dinamik olarak atadığı PORT'u dinle (Varsayılan 8080)
ENV PORT 8080
EXPOSE 8080

# Sunucuyu çalıştır
CMD ["python", "update_server.py"]
