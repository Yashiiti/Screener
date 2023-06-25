from fastapi import FastAPI, Request, Depends, BackgroundTasks
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Stock
import yfinance

app= FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
class StockRequest(BaseModel):
    symbol: str
def get_db():
    
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
@app.get("/")
def home(request: Request,forward_pe=None,dividend_yield=None,ma50=None,ma200=None,db: Session=Depends(get_db)):
    ''' This is the homepage of the dashboard '''
    stocks = db.query(Stock)
    # for stock in stocks:
    # print(stocks)
    
    #     background_tasks.add_task(fetch_stock_data, stock.id)
    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)
        # print(stocks)
    if dividend_yield:
        stocks = stocks.filter(Stock.dividend_yield > dividend_yield)
        # print(stocks)
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    if ma200:
        stocks = stocks.filter(Stock.price > Stock.ma200)

    return templates.TemplateResponse("home.html", {"request": request, "stocks": stocks,"dividend_yield":dividend_yield,"ma50":ma50,"ma200":ma200})

async def fetch_stock_data(id: int):
    db=SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    yahoo_data = yfinance.Ticker(stock.symbol)
    # print(yahoo_data.info['twoHundredDayAverage'])

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    if 'dividendYield' in yahoo_data.info:
        stock.dividend_yield = yahoo_data.info['dividendYield'] *100
    

    db.add(stock)
    db.commit()



@app.post("/stock")
def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks,db: Session=Depends(get_db)):

    ''' creates and stores a stock in database   '''
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()
    background_tasks.add_task(fetch_stock_data, stock.id)


    return {"code": "success", "message": "stock created"}


