import 'package:http/http.dart' as http;
import 'package:xml/xml.dart';

/// 검색어로 뉴스 RSS 최신 5건을 가져옵니다.
///
/// 1) Google News RSS → 403 등 실패 시 2) Bing News RSS로 재시도합니다.
/// 두 소스 모두 브라우저와 유사한 `User-Agent`를 사용합니다.
class StockNewsApi {
  static const _browserUa =
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

  static Map<String, String> get _headers => {
    'User-Agent': _browserUa,
    'Accept': 'application/rss+xml, application/xml, text/xml, */*;q=0.8',
  };

  static Future<List<NewsItem>> fetch(String query) async {
    final q = query.trim();
    if (q.isEmpty) return [];

    final fromGoogle = await _itemsFromRss(_googleRssUri(q));
    if (fromGoogle.isNotEmpty) return fromGoogle.take(5).toList();

    final fromBing = await _itemsFromRss(_bingRssUri(q));
    return fromBing.take(5).toList();
  }

  static Uri _googleRssUri(String query) => Uri.parse(
    'https://news.google.com/rss/search'
    '?q=${Uri.encodeComponent(query)}&hl=ko&gl=KR&ceid=KR:ko',
  );

  static Uri _bingRssUri(String query) => Uri.parse(
    'https://www.bing.com/news/search?q=${Uri.encodeComponent(query)}&format=rss',
  );

  static Future<List<NewsItem>> _itemsFromRss(Uri url) async {
    try {
      final response = await http.get(url, headers: _headers);
      if (response.statusCode != 200) return [];
      final document = XmlDocument.parse(response.body);
      return document
          .findAllElements('item')
          .map(NewsItem.fromXml)
          .where((e) => e.title.isNotEmpty && e.link.isNotEmpty)
          .toList();
    } on Object {
      return [];
    }
  }
}

class NewsItem {
  NewsItem({
    required this.title,
    required this.link,
    required this.source,
    required this.publishedAt,
  });

  final String title;
  final String link;
  final String source;
  final DateTime publishedAt;

  factory NewsItem.fromXml(XmlElement element) {
    final pubDate = element.getElement('pubDate')?.innerText;
    return NewsItem(
      title: element.getElement('title')?.innerText ?? '',
      link: element.getElement('link')?.innerText ?? '',
      source: _sourceFromItem(element),
      publishedAt: pubDate != null ? (DateTime.tryParse(pubDate) ?? DateTime.now()) : DateTime.now(),
    );
  }

  /// Google은 `<source>`, Bing은 `<News:Source>` 등 로컬 이름이 `source`인 요소를 씁니다.
  static String _sourceFromItem(XmlElement item) {
    for (final child in item.childElements) {
      if (child.name.local.toLowerCase() == 'source') {
        return child.innerText;
      }
    }
    return '';
  }
}
