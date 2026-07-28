import 'package:flutter/material.dart';
import 'package:stock_app/detail_page.dart';
import 'package:stock_app/home_page.dart';
import 'package:stock_app/search_page.dart';

void main() {
  runApp(const StockApp());
}

class StockApp extends StatelessWidget {
  const StockApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stock App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0B0E13),
        fontFamily: 'Inter',
      ),
      initialRoute: '/',
      onGenerateRoute: _onGenerateRoute,
    );
  }

  Route<dynamic>? _onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const HomePage());
      case '/search':
        return MaterialPageRoute(builder: (_) => const SearchPage());
      case '/detail':
        final code = (settings.arguments as String?) ?? '005930';
        return MaterialPageRoute(builder: (_) => DetailPage(stockCode: code));
      default:
        return MaterialPageRoute(builder: (_) => const HomePage());
    }
  }
}
