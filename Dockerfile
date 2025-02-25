# pakai python terbaru
FROM python:3.10

# set workdir
WORKDIR /app

# copy semua file ke dalam container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port huggingface
EXPOSE 7860

# jalankan server
CMD ["python", "main.py"] to
