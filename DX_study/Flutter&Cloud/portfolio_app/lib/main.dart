import 'package:flutter/material.dart';
import 'package:flutter_web_plugins/flutter_web_plugins.dart';
import 'package:portfolio_app/contact_page.dart';
import 'package:portfolio_app/home_page.dart';
import 'package:portfolio_app/projects_page.dart';

void main() {
  usePathUrlStrategy();
  runApp(PortfolioApp());
}

class PortfolioApp extends StatelessWidget {
  const PortfolioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(fontFamily: "ProductSans"),
      initialRoute: "/",
      onGenerateRoute: (routeSettings) {
        final Uri uri = Uri.parse(routeSettings.name ?? "");
        final String path = uri.path;

        // 유저가 어느 페이지로 이동할지 알려주는 변수
        Widget page;

        // path 값에 따라서 page 변수를 완성(지정)해준다.
        if (path == "/") {
          page = HomePage();
        } else if (path == "/projects") {
          page = ProjectsPage();
        } else if (path == "/contact") {
          page = ContactPage();
        } else {
          page = HomePage();
        }

        return PageRouteBuilder(
          pageBuilder: (_, __, ___) {
            return page;
          },
          settings: routeSettings,
        );
      },
      debugShowCheckedModeBanner: false,
    );
  }
}
