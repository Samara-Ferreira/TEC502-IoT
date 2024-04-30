# versão da imagem
FROM python:3.12-slim

# criação do diretório de trabalho
WORKDIR /app

# copia o arquivo de dependências para o diretório de trabalho
COPY . .

# instala as dependências
RUN pip install requests

# expõe a porta
EXPOSE 5555

# executa a aplicação
CMD ["python", "app.py"]