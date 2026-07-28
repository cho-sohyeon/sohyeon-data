import 'dart:convert';
import 'package:http/http.dart' as http;

// `StockSearchApi.search(query)`를 통해 검색어로 KOSPI / 코스닥 종목 리스트를 가져옵니다.
class StockSearchApi {
  static Future<List<StockSearchResult>> search(String query) async {
    if (query.isEmpty) return [];
    final url = Uri.parse(
      'https://stock.naver.com/api/autocomplete/search/autoComplete'
      '?query=${Uri.encodeComponent(query)}&target=stock',
    );
    final response = await http.get(url);
    final body = utf8.decode(response.bodyBytes);
    final data = jsonDecode(body) as Map<String, dynamic>;
    final items = (data['result']?['items'] as List?) ?? [];
    return items
        .cast<Map<String, dynamic>>()
        .where((e) => e['nationCode'] == 'KOR' && e['category'] == 'stock')
        .map(StockSearchResult.fromJson)
        .toList();
  }
}

class StockSearchResult {
  StockSearchResult({
    required this.code,
    required this.name,
    required this.market,
  });

  final String code;
  final String name;
  final String market;

  factory StockSearchResult.fromJson(Map<String, dynamic> json) {
    return StockSearchResult(
      code: json['code'] as String,
      name: json['name'] as String,
      market: json['typeName'] as String? ?? '',
    );
  }
}
