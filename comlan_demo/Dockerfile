   # 使用 Python 3.9 作为基础镜像
   FROM python:3.9-slim

   # 设置工作目录
   WORKDIR /app

   # 复制依赖文件
   COPY requirements.txt .

   # 安装依赖
   RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir \
    --default-timeout=1000 \
    -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

   # 复制应用代码
   COPY . .

   # 暴露 Streamlit 默认端口
   EXPOSE 8501

   # 启动命令
   ENTRYPOINT ["streamlit", "run", "Comlan_Demo.py", "--server.address=0.0.0.0"]
