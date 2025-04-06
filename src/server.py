import uvicorn
from fastapi import FastAPI
from route import user, admin

app = FastAPI()
app.include_router(user.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "hello world"}

if __name__ == '__main__':
    uvicorn.run(app="server:app", host="127.0.0.1", port=8080)