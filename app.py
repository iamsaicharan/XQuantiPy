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
            with open('server/templates/home.html', 'r', encoding='utf-8') as template_file:
                html_template = template_file.read()
            variables = {
                'stock': stock_symbol,
                'plot': stock.to_html(),
            }
            for variable, value in variables.items():
                placeholder = "{{" + variable + "}}"
                html_template = html_template.replace(placeholder, value)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_template.encode('utf-8'))
        
        if parsed_url.path == '/stocks':
            query_params = parse_qs(parsed_url.query)
            filter_type = query_params.get('indicators')
            symbol = query_params.get('symbol')[0]
            period = query_params.get('period')[0]
            print(query_params)
            if 'moving_average' in filter_type:
                ma_period = query_params.get('ma_period')
                period_list = []
                for item in ma_period:
                    if ',' in item:
                        period_list.extend(item.split(','))
                    else:
                        period_list.append(item)
                period_list = [int(item) for item in period_list]
                ma_type = query_params.get('type')[0]
                ma = Ticker(symbol, period=period).show_moving_average(type=ma_type, period=period_list)
                with open('server/templates/home.html', 'r') as template_file:
                    html_template = template_file.read()
                variables = {
                    'stock': symbol,
                    'plot': ma.to_html(),
                }
                for variable, value in variables.items():
                    placeholder = "{{" + variable + "}}"
                    html_template = html_template.replace(placeholder, value)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_template.encode('utf-8'))

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