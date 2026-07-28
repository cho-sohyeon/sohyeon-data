import 'dart:convert';
import 'package:http/http.dart' as http;

// `StockQuoteApi.fetch(code)`를 통해 종목코드(6자리)로 현재가 정보를 가져옵니다.
class StockQuoteApi {
  static Future<StockQuote> fetch(String code) async {
    final url = Uri.parse(
      'https://polling.finance.naver.com/api/realtime/domestic/stock/$code',
    );
    final response = await http.get(url);
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    final item = (data['datas'] as List).first as Map<String, dynamic>;
    return StockQuote.fromJson(item);
  }
}

class StockQuote {
  StockQuote({
    required this.code,
    required this.name,
    required this.market,
    required this.price,
    required this.diff,
    required this.diffSign,
    required this.diffRate,
  });

  final String code;
  final String name;
  final String market;
  final int price;
  final int diff;
  final String diffSign;
  final double diffRate;

  factory StockQuote.fromJson(Map<String, dynamic> json) {
    final exchange = json['stockExchangeType'] as Map<String, dynamic>;
    final compare = json['compareToPreviousPrice'] as Map<String, dynamic>;
    return StockQuote(
      code: json['itemCode'] as String,
      name: json['stockName'] as String,
      market: exchange['name'] as String,
      price: int.parse(json['closePriceRaw'] as String),
      diff: int.parse(json['compareToPreviousClosePriceRaw'] as String),
      diffSign: compare['code'] as String,
      diffRate: double.parse(json['fluctuationsRatioRaw'] as String),
    );
  }

  bool get isUp => diffSign == '1' || diffSign == '2';
  bool get isDown => diffSign == '4' || diffSign == '5';
}
