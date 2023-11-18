import http.server
import yfinance as yf
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer
from xquantipy.stocks.ticker import Ticker


class StockDataHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == '/':
            query_params = parse_qs(parsed_url.query)
            stock_symbol = query_params.get('symbol')[0]
            stock = Ticker(stock_symbol).show_adj_close()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'r') as template_file:
                html_template = template_file.read()
            self.wfile.write(html_template.format(
                stock.to_html()
            ).encode())
        
        if parsed_url.path == '/ma':
            query_params = parse_qs(parsed_url.query)
            period = int(query_params.get('ma_period')[0])
            symbol = query_params.get('symbol')[0]
            ma_type = query_params.get('type')[0]
            ma = Ticker(symbol).show_moving_average(type=ma_type, period=[period])
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'r') as template_file:
                html_template = template_file.read()
            self.wfile.write(html_template.format(
                ma.to_html()
            ).encode())

    def get_stock_data(self, stock_symbol):
        stock = yf.download(stock_symbol)
        return stock

def main():
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, StockDataHandler)
    print("Server running on port : " + str(PORT))
    server.serve_forever()

if __name__ == '__main__':
    main()