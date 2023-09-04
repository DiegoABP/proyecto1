FROM python3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requriements.txt
COPY tokenizer.pkl .
COPY model.h5 .
COPY pulsares.py .
ENTRYPOINT [ "python","pulsares.py" ]