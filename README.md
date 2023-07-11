# Stock Screener
This project implements a stock screener using FastAPI, a modern web framework for building APIs with Python. The stock screener allows users to filter stocks based on various criteria such as forward P/E ratio, dividend yield, and moving averages.
## Installation
Clone this repo: git clone https://github.com/Yashiiti/Screener.git
Change to the project directory: cd stock-screener
Install dependencies: pip install -r requirements.txt
Set up the database:
Modify the database.py file to configure the database connection. By default, it uses SQLite.
Run the following command to create the database tables: python -m models
Run the application: uvicorn main:app --reload

## Usage
The Stock Screener provides a web-based interface to filter stocks based on certain criteria. Here's how to use the application:

Access the homepage: Open your web browser and navigate to http://localhost:8000.

Filter stocks: On the homepage, you can specify filter criteria such as forward P/E ratio, dividend yield, and moving averages. Enter the desired values in the corresponding fields and click the "Filter" button.

View filtered stocks: The application will display a list of stocks that match the specified filter criteria. The stock data includes symbols, forward P/E ratios, dividend yields, and moving averages.

Create a new stock: To add a new stock to the database, click the "Create Stock" button on the homepage. Enter the stock symbol and submit the form. The application will initiate a background task to fetch additional data for the stock using the Yahoo Finance API.

## Architecture
The Stock Screener application follows the following architectural pattern:

Model-View-Controller (MVC): The project structure separates concerns into models, views (templates), and controllers (routes and background tasks). This pattern provides a clear separation of responsibilities and promotes maintainability.
The main components of the project are as follows:

main.py: This file contains the FastAPI application setup, including route definitions and database configuration. It serves as the entry point for running the Stock Screener.

models.py: This file defines the SQLAlchemy database models used to store stock data. It includes the Stock model with attributes such as symbol, forward P/E ratio, dividend yield, and moving averages.

database.py: This file configures the database connection and provides an SQLAlchemy SessionLocal dependency that can be used to access the database within route functions.

templates/: This directory contains Jinja2 templates used for rendering HTML pages. The home.html template is used for the homepage, which displays the filtered stock data.
