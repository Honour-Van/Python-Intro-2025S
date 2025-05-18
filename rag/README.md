# Langchain 演示

## 环境准备

### 不使用 conda

更新 pip 环境
```
python -m pip install --upgrade pip
```

安装所需依赖
```
pip install -r requirements.txt
```

### 使用 conda

```
conda env create -f environment.yml
conda activate langchain-rag
```

## 本地部署

在 https://ollama.com/download 下载 ollama。

下载 ollama 之后，进入命令行（Windows：cmd，MacOS：Terminal）拉取对应模型：
```
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

## 运行程序
完成上述配置之后，程序即可正常运行

Windows注意修改程序中的Model参数，增加`base_url=http://localhost:11434`，参考程序中被注释掉的部分。