## TO RUN THIS CODE WITH DOCKER YOU NEED TO:

#### 1. Turn .env.example into .env and fill in the available constants 
#### 2. Make a docker image or otherwise build:
```
docker build -t rsibot .  
```
#### 3. Run container with your image:
```
docker run rsibot  
```

## TO RUN THIS CODE WITHOUT DOCKER YOU NEED TO:
#### 1. Turn .env.example into .env and fill in the available constants 
#### 2. Install dependencies:
```
 pip install -r requirements.txt
```
#### 3. Run code:
```
python bot/bot_rsi.py
```
